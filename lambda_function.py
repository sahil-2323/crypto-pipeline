import json
import requests
import pandas as pd
from datetime import datetime
import urllib.parse
from sqlalchemy import create_engine

# 1. Clear config block
RAW_PASSWORD = "YOUR_SUPABASE_PASSWORD_HERE"  # Clean password, no colons or project IDs here!
SAFE_PASSWORD = urllib.parse.quote_plus(RAW_PASSWORD)

# 2. The explicit project-mapped pooler URL string
# Notice the project ID 'tddwqyyepoadjpofpweg' is natively the sub-domain prefix!
DATABASE_URL = f"postgresql://postgres.tddwqyyepoadjpofpweg:{SAFE_PASSWORD}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"


def lambda_handler(event, context):
    print("AWS lambda triggered. Starting cryto ingestion.....")

    #fetching data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    print("Fetching data from CoinGecko API......")
    response= requests.get(url,params=params)

    if response.status_code == 200:
        data = response.json()

        processed_data = []
        for coin in data:
            processed_data.append({
                "timestamp": datetime.utcnow(),
                "coin_id": coin["id"],
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "current_price_usd": float(coin["current_price"]),
                "market_cap_usd": float(coin["market_cap"]),
                "total_volume_usd": float(coin["total_volume"]),
                "price_change_percentage_24h": float(coin["price_change_percentage_24h"]) if coin["price_change_percentage_24h"] else 0.0
            })

        df= pd.DataFrame(processed_data)
        
        #saving to cloud DB
        try:
            print("Connecting to Supabase PostgreSQl from AWS.....")
            engine = create_engine(DATABASE_URL)
            df.to_sql('crypto_prices', con=engine, if_exists='append', index= False)
            print("AWS pipeline execution successful..!!!!!")

            return {
                'statusCode': 200,
                'body': json.dumps('Data ingestion successful from AWS Lambda')
            }
        except Exception as e:
            print(f"Database error: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Database error: {str(e)}')
            }
    else:
        print(f"API Failure. Status Code: {response.status_code}")
        return {
            'statusCode': response.status_code,
            'body': json.dumps('Failed to fetch data from CoinGecko')
        }