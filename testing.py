
import os
from fyers_api import accessToken
from fyers_api import fyersModel
import pandas as pd
import json
from flask import Flask, request
import time



#historical data test
token_path="FyresAuth.txt"
key_secret = open(token_path,'r').read().split()
client_id = key_secret[0]
secret_key = key_secret[1]
appIDhash=key_secret[2]
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"
key_secret2 = open("FyresAPI.txt",'r').read().split()
auth_code = key_secret2[0]

session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)
session.set_token(auth_code)
response = session.generate_token()
print(response)
# write the access token to file
access_token =response['access_token']#"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTIzNDQyMTAsImV4cCI6MTY5MjQwNTA1MCwibmJmIjoxNjkyMzQ0MjEwLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazN4LVNPZENYaDZTemJueVE1UE4wZUNYN3VjLWxQWlk1VlRuRzE3Umhma1E2UTdXWHpYaXh3QzBrWHhQcGtxS0NzNkxrU1BkME51ckh5RkhVX0VCWUFRVTFJdGlOamtFMG11b3VTcTFuV19CWVllVT0iLCJkaXNwbGF5X25hbWUiOiJTQU1FRVIgU1lFRCIsIm9tcyI6IksxIiwiaHNtX2tleSI6IjNhY2VkNzIxZWVmODAwMTRlNGMxYmMzNTdiOGQ5YTQ1M2EwNGRlZjJjNzQ3ZGU4MzBjOWU5NWRiIiwiZnlfaWQiOiJYUzExODQ3IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.8ayAYZBnLPWVHmpf51chNOonOfVwosBQPoLNo2ii2d8', 'refresh_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTIzNDQyMTAsImV4cCI6MTY5MzYxNDY1MCwibmJmIjoxNjkyMzQ0MjEwLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6InJlZnJlc2hfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQmszeC1TT2RDWGg2U3pibnlRNVBOMGVDWDd1Yy1sUFpZNVZUbkcxN1JoZmtRNlE3V1h6WGl4d0Mwa1h4UHBrcUtDczZMa1NQZDBOdXJIeUZIVV9FQllBUVUxSXRpTmprRTBtdW91U3ExbldfQllZZVU9IiwiZGlzcGxheV9uYW1lIjoiU0FNRUVSIFNZRUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIzYWNlZDcyMWVlZjgwMDE0ZTRjMWJjMzU3YjhkOWE0NTNhMDRkZWYyYzc0N2RlODMwYzllOTVkYiIsImZ5X2lkIjoiWFMxMTg0NyIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.1zvCaG6PmEUgJ2sHYPKaZv_ivQn2cpI-9ekBFJQFeQE" #response["access_token"]
print(access_token)
# Initialize the fyersModel class
print(access_token)
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="logs")
print(fyers.get_profile())
print(fyers.client_id)

# Define the symbol for the specific option contract (expiry contract)
symbol = "NSE:NIFTY2391419950PE"  # Change this to the correct symbol

print(fyers.quotes(data={"symbols": symbol}))

data = {
    "symbol": symbol,
    "resolution": "D",  # Daily resolution
    "date_format": "0",
    "range_from": "1679241600",  # Unix timestamp for 18-08-2023
    "range_to": "1679846400",    # Unix timestamp for 24-08-2023
    "cont_flag": "1"
}

response = fyers.history(data=data)

# Process response and create DataFrame
candles = response.get("candles", [])
columns = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.DataFrame(candles, columns=columns)

# Convert Unix timestamps to human-readable dates
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# Save DataFrame to CSV
csv_filename = f"{symbol}_weekly_data.csv"
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")

#BN44000CE PE
#BN44500CE PE
#NIFTY 19500CE PE
#NIFTY 19250CE PE
# D 5 15 1 


symbol=[""]



#### STARTING OF COLLECTION OF DATA FOR OPTION CHAIN
# BN 44000 CE PE
# Define the symbol for the specific option contract (expiry contract)
#symbol = "NSE:BANKNIFTY23AUG4000CE"  # Change this to the correct symbol
#format="D"
#data = {
#    "symbol": symbol,
#    "resolution": format,  # Daily resolution
#    "date_format": "0",
#    "range_from": "1690861500",  # Unix timestamp for 18-08-2023
#    "range_to": "1693431900",    # Unix timestamp for 24-08-2023
#    "cont_flag": "1"
#}
#
#response = fyers.history(data=data)
#
## Process response and create DataFrame
#candles = response.get("candles", [])
#columns = ["timestamp", "open", "high", "low", "close", "volume"]
#df = pd.DataFrame(candles, columns=columns)
#
## Convert Unix timestamps to human-readable dates
#df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
#
## Save DataFrame to CSV
#csv_filename = f"{symbol}_{format}_testdata.csv"
#df.to_csv(csv_filename, index=False)
#
#print(f"Data saved to {csv_filename}")
###BN 44000

symbol_prefix = "BANKNIFTY23913"
strike_prices = range(44000, 46001, 100)  # Generate strike prices from 19800 to 20600 with a step of 100

call_option_symbols = [f"{symbol_prefix}{strike}CE" for strike in strike_prices]
put_option_symbols = [f"{symbol_prefix}{strike}PE" for strike in strike_prices]

# Combine both call and put options
symbols = call_option_symbols + put_option_symbols

# Now, all_option_symbols contains the list of FINNIFTY option symbols you requested
print(symbols)

formats = ["D", "1", "5", "15", "60"]

for symbol in symbols:
    for format in formats:
        full_symbol = f"NSE:{symbol}"
        data = {
            "symbol": full_symbol,
            "resolution": format,
            "date_format": "1",
            "range_from": "2023-09-07",
            "range_to": "2023-09-13",
            "cont_flag": "1"
        }
        
        response = fyers.history(data=data)

        # Process response and create DataFrame
        candles = response.get("candles", [])
        columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame(candles, columns=columns)

        # Convert Unix timestamps to human-readable dates
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

        # Save DataFrame to CSV
        output_folder = "Option data/Sep/BANKNIFTY"
        csv_filename = os.path.join(output_folder, f"{symbol}_{format}_data.csv")
        df.to_csv(csv_filename, index=False)

        print(f"Data saved to {csv_filename}")







##3## END OF DATA COLLECTION FOR OPTION CHAIN


# URL of the CSV file
csv_url = "https://public.fyers.in/sym_details/NSE_FO.csv"
t = time.localtime()
        #time in format 24-Aug-2023
current_time = time.strftime("%d-%b-%Y", t)

print(current_time)
# Read the CSV file into a DataFrame
df = pd.read_csv(csv_url, header=None)
# Replace this with the symbol you are interested in
target_symbol = "NIFTY"
# Current strike price (replace with your actual value)
current_strike_price = 19334
option_type = "PE"      # "CE" for call option, "PE" for put option
# Filter rows containing the target symbol
symbol_filtered_rows = df[df[13]==target_symbol]
print(symbol_filtered_rows)
symbol_filtered_rows["StrikeDiff"] = abs(symbol_filtered_rows[15].astype(int) - current_strike_price)

# Find the two rows with the nearest strike prices
nearest_rows = symbol_filtered_rows.nsmallest(2, "StrikeDiff")
# Extract the value from the 10th column (index 9)
nearest_values = nearest_rows[9].to_list()
# Find the first value in the list that contains the desired symbol
matching_value = next((value for value in nearest_values if option_type in value), None)

print("Nearest Value:", matching_value)

# Initialize your Flask app
app = Flask(__name__)



fyers = fyersModel.FyersModel(client_id="g", token="g", log_path="logs")



@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.data)
    try:
        data = json.loads(request.data)
        
        # Extract parameters from the TradingView alert
        symbol = data['reference'] 
        order_type = data['orderType']  # 'buy' or 'sell'
        quantity = data['contractAmount']  # Number of contracts/lots
        price=data['price']
        print(symbol, order_type, quantity,price)
        
        # Function to get current option contract for given index/stock
        def get_current_expiry(symbol,option_type,price):
              # URL of the CSV file
              csv_url = "https://public.fyers.in/sym_details/NSE_FO.csv"# Read the CSV file into a DataFrame
              df = pd.read_csv(csv_url, header=None)# Replace this with the symbol you are interested in
              # Current strike price (replace with your actual value)
              current_strike_price = price# Filter rows containing the target symbol
              symbol_filtered_rows = df[df[13]==symbol]
              print(symbol_filtered_rows)# Calculate the absolute difference between strike prices and the current_strike_price
              symbol_filtered_rows["StrikeDiff"] = abs(symbol_filtered_rows[15].astype(int) - current_strike_price)# Find the two rows with the nearest strike prices
              nearest_rows = symbol_filtered_rows.nsmallest(2, "StrikeDiff")
              # Extract the value from the 10th column (index 9)
              nearest_values = nearest_rows[9].to_list()# Find the first value in the list that contains the desired symbol
              matching_value = next((value for value in nearest_values if option_type in value), None)
              print("Nearest Value:", matching_value)
              return matching_value

        
        # Get current option contract
        
        index_symbol = "NIFTY"  # Replace with your index/stock symbol
        option_type = "CE"      # "CE" for call option, "PE" for put option
        
        option_contract = get_current_expiry(symbol, order_type,price)
        data = {
              "symbol":str(option_contract),
              "qty":quantity,
              "type":2,
              "side":1,
              "productType":"MARGIN",
              "limitPrice":0,
              "stopPrice":0,
              "validity":"DAY",
              
              "offlineOrder":"False",
              }
        response = fyers.place_order(data=data)
        print("Order placed successfully:",response)

       

        print("Current Option Contract:", option_contract)
        return 'Success', 200
    except Exception as e:
        print("Error:", e)
        return 'Error processing order', 500

if __name__ == '__main__':
    app.run()





