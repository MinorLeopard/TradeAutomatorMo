import openpyxl
from openpyxl import Workbook
import os
import csv
from fyers_api import accessToken
from fyers_api import fyersModel
import pandas as pd
import json
from flask import Flask, request
import time


# Initialize your Flask app
app = Flask(__name__)

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


def square_off_opposite_positions(date, order_type, symbol):
    print(f"Square off opposite positions for {date} {order_type} {symbol}")
    positions_response = fyers.positions()
    print(positions_response)
    if positions_response['s'] == 'ok':
        positions = positions_response['netPositions']
        for position in positions:
            if position['symbol'] == symbol:
                    # Check if position is closed
                    if position['sellQty'] > 0:
                        print(f"Position for symbol {symbol} is closed.")
                        # Update the CSV file with sell and other values
                        update_buy_price_and_timestamp(date,symbol,positions_response)
                        #CHECK FOR CORRECTION

         
    # Check if the CSV file for the day exists




    csv_file_name = f"TradeBook/Positions/{date}.csv"
    if not os.path.exists(csv_file_name):
        print(f"CSV file for {date} does not exist.")
        return

    # Read the CSV file    
    
    with open(csv_file_name, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows_to_square = []
        print("Rows to square off:")
        for row in csvreader:
            if row[2] == symbol and row[3] != order_type and row[7] == '' and row[8] == '':
                rows_to_square.append(row)
        for row in rows_to_square:
            print(f"Squaring off position: {row}")
            # Get the order ID of the position to square off
            position_order_id = {"id":row[5]}
            
            # Fetch the order details using FYERS API
            order_details = fyers.orderbook(data=position_order_id)
            print("Order details:", order_details)
            if order_details['orderBook'][0]['status'] == 2:
                # Place a square off order using FYERS API
                square_off_data = {
                    "id": order_details['orderBook'][0]['symbol'],
            
                }
                square_off_response = fyers.exit_positions(data=square_off_data)
                print("Square off response:", square_off_response)
                
                # Update the buy price and timestamp in the row
                square_off_buy_price = "0"
                t = time.localtime()
                #time in format 24-Aug-2023
                square_off_timestamp =time.strftime("%d-%b-%Y %H:%M:%S", t)
                update_buy_price_and_timestamp(date, order_details['orderBook'][0]['symbol'], square_off_response)
            else:
                print(f"Position {position_order_id} not filled, skipping square off")






# Create a CSV file for the day if it doesn't exist
def create_csv_for_day(date):
    csv_file_name = f"TradeBook/Positions/{date}.csv"
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date', 'Symbol','OptionName', 'OrderType', 'Quantity', 'EntryPrice', 'OrderId', 'ExitPrice', 'Timestamp','RealizedProfit','UnrealizedProfit','TotalProfit','TotalProfit%'])

# Write order details and response to CSV file
def write_order_to_csv(date, order_details,orderType, order_response,symbol):
    csv_file_name = f"TradeBook/Positions/{date}.csv"
    with open(csv_file_name, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            date, symbol,order_details['symbol'], orderType, 
            order_details['qty'], order_response['orderBook'][0]['tradedPrice'], 
            order_response['orderBook'][0]['id'], '', ''
        ])

# Update buy price and timestamp in CSV file
def update_buy_price_and_timestamp(date, id,order_symbol, response):
    csv_file_name = f"TradeBook/Positions/{date}.csv"
    temp_file_name = f"temp_{date}.csv"
    response = fyers.positions()
    print(response)

    # Check if the response is successful
    if response['s'] == 'ok':
        positions = response['netPositions']# CSV file to update
        with open(csv_file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            rows = list(csvreader)
        
        for position in positions:
            symbol = position['symbol']
            sell_avg = position['sellAvg']
            sell_qty = position['sellQty']
            realized_profit = position['realized_profit']
            
            for row in rows:
                if len(row) >= 3 and row[2] == symbol:
                    row[7] = str(sell_avg)
                    row[8] = str(sell_qty)
                    row[9] = str(realized_profit)
                # Update the CSV file
        with open(csv_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows)
        print("CSV file updated successfully.")
    else:
        print("Error fetching positions.")
t = time.localtime()
#time in format 24-Aug-2023
current_time = time.strftime("%d-%b-%Y", t)

create_csv_for_day(current_time)


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
        timeframe=data['timeframe']
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
        # Square off opposite type positions before placing new order
        t = time.localtime()
        #time in format 24-Aug-2023
        current_time = time.strftime("%d-%b-%Y", t)
        if order_type == 'CE':
            opp='PE'
        else:
            opp='CE'
        square_off_opposite_positions(current_time, order_type, get_current_expiry(symbol, opp,price))
        
        option_contract = get_current_expiry(symbol, order_type,price)
        # Calculate stop loss and take profit
        vo=fyers.quotes(data={"symbols": option_contract})
        print(vo)
        ltp=vo['d'][0]['v']['lp']
        stop_loss = (0.10 * ltp)
        print(stop_loss)
        take_profit = (0.20 * ltp)#variable as per risk appetite
        if timeframe==15:
            take_profit=(1 * ltp)
        print(take_profit)
        data = {
              "symbol":str(get_current_expiry(symbol,order_type,price)),
              "qty":quantity,
              "type":2,
              "side":1,
              "productType":"BO",#Margin orders dont allow stop loss and take profit
              "limitPrice":0,
              "stopPrice":0,
              "validity":"DAY",
              "disclosedQty":0,
              "stopLoss":round(stop_loss,1),
              "takeProfit":round(take_profit,1),
              "offlineOrder":"False",
              }
        #UPDATED WITH STOP LOSS AND TAKE PROFIT, MOVE TOWARDS BOLLINGER BAND CALCULATION
        response = fyers.place_order(data=data)
        print(response)
        # Get buy price and timestamp from response using FYERS API
        order_id = {"id":response['id']}
        buy_response = fyers.orderbook(data=order_id)
        print(buy_response)
        buy_price = buy_response['orderBook'][0]['tradedPrice']
        timestamp = buy_response['orderBook'][0]['orderDateTime']
        
        # Get current date
        current_date = timestamp.split()[0]
        
        # Create or update CSV file for the day
        create_csv_for_day(current_time)
        write_order_to_csv(current_time, data,order_type, buy_response,symbol)
        update_buy_price_and_timestamp(current_time, order_id, buy_price, timestamp)
        print("Current Option Contract:", option_contract)
        return 'success', 200
    except Exception as e:
        print("Error:", e)
        return 'Error processing order', 500

if __name__ == '__main__':
    app.run()


