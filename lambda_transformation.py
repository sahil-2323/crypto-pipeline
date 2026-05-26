import json
import urllib.request
from datetime import datetime

# --- Configuration ---
# 🔗 Grab your Supabase URL and Project API Key from your Supabase Dashboard Project Settings
SUPABASE_URL = "https://tddwqyyepoadjpofpweg.supabase.co" 
SUPABASE_KEY = "YOUR_SUPABASE_API_KEY" 

def lambda_handler(event, context):
    print("AWS Lambda triggered. Starting Layerless Crypto ETL...")
    
    # 1. EXTRACT: Fetch data from CoinGecko API
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,cardano,solana,ripple&order=market_cap_desc"
    
    try:
        # Use native urllib to fetch market metrics (no requests library needed!)
        with urllib.request.urlopen(url) as response:
            raw_data = json.loads(response.read().decode())
        
        transformed_records = []
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        usd_to_inr_rate = 83.5
        
        # 2. TRANSFORM: Feature Engineering
        print("Starting data transformation...")
        for coin in raw_data:
            high_24h = coin.get('high_24h', 0) or 0
            low_24h = coin.get('low_24h', 0) or 0
            current_price = coin.get('current_price', 0) or 0
            
            volatility_spread_pct = (((high_24h - low_24h) / low_24h) * 100) if low_24h > 0 else 0.0
            price_inr = current_price * usd_to_inr_rate
            
            clean_record = {
                "id": coin.get('id'),
                "symbol": coin.get('symbol'),
                "name": coin.get('name'),
                "current_price": float(current_price),
                "market_cap": coin.get('market_cap'),
                "high_24h": float(high_24h),
                "low_24h": float(low_24h),
                "price_change_percentage_24h": coin.get('price_change_percentage_24h'),
                "volatility_spread_pct": round(volatility_spread_pct, 2),
                "price_inr": round(price_inr, 2),
                "extracted_at": current_time
            }
            transformed_records.append(clean_record)
            
        # 3. LOAD: Ingest data into Supabase via their native REST API endpoint
        print("Sending data payload straight to Supabase REST Endpoint...")
        supabase_endpoint = f"{SUPABASE_URL}/rest/v1/transformed_crypto_prices"
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"  # Upsert data if records match
        }
        
        # Format payload and trigger a direct HTTP POST request
        data_payload = json.dumps(transformed_records).encode('utf-8')
        req = urllib.request.Request(supabase_endpoint, data=data_payload, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as resp:
            print(f"Supabase Response Status Code: {resp.getcode()}")
            
        print("ETL Pipeline completed successfully with Zero Layers!")
        return {
            "statusCode": 200,
            "body": json.dumps("ETL Pipeline run successful!")
        }
        
    except Exception as e:
        print(f"Pipeline error: {str(e)}")
        raise e