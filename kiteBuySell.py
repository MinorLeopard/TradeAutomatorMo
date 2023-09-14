from kiteconnect import KiteConnect
import json
from flask import Flask, request
import pandas as pd

# Initialize your Flask app
app = Flask(__name__)


api_key = '389m4rmjkmdp05p1'
api_secret = 'YOUR_API_SECRET'
redirect_url = 'https://google.com/'
request_token=open("request_token.txt",'r').read()
kite = KiteConnect(api_key=api_key)
data = kite.generate_session(request_token)
with open("access_token.txt",'w') as file:
    file.write(data["access_token"])
print("Login Successful")
token_path="access_token.txt"
key_secret = open(token_path,'r').read().split()

kite.set_access_token(access_token=key_secret[0])  # Set your access token

# Define your webhook endpoint to receive TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data)
        
        # Extract parameters from the TradingView alert
        symbol = data['reference'] 
        order_type = data['orderType']  # 'buy' or 'sell'
        quantity = data['contractAmount']  # Number of contracts/lots
        print(symbol, order_type, quantity)
        
        # Function to get current option contract for given index/stock
        def get_current_option_contract(index_symbol, option_type):
            # Get list of all NFO instruments
            instruments_df = pd.DataFrame(kite.instruments("NFO"))
            # Filter by index_symbol and option_type
            df = instruments_df[(instruments_df['tradingsymbol'].str.contains(index_symbol)) & (instruments_df['instrument_type'] == 'OPTIDX') & (instruments_df['segment'] == 'NFO-OPT')]
            # Sort by expiry date
            df = df.sort_values(['expiry'])
            # Get the nearest expiry
            nearest_expiry = df['expiry'].iloc[0]
            # Get the current option contract
            instrument_token = df[(df['expiry'] == nearest_expiry) & (df['tradingsymbol'].str.contains(option_type))]['instrument_token'].iloc[0]
            return instrument_token

        # Example usage
        index_symbol = "NIFTY"  # Replace with your index/stock symbol
        option_type = "CE"      # "CE" for call option, "PE" for put option
        option_contract = get_current_option_contract(index_symbol, option_type)

        print("Current Option Contract:", option_contract)

        # Place an order using the Kite Connect API
        if order_type == 'buy':
            order_response = kite.place_order(
                tradingsymbol=symbol,
                exchange=kite.EXCHANGE_NFO,
                transaction_type=kite.TRANSACTION_TYPE_BUY,
                quantity=quantity,
                order_type=kite.ORDER_TYPE_MARKET,
                product=kite.PRODUCT_NRML
            )
            
            print("Buy Order Placed:", order_response)
        elif order_type == 'sell':
            order_response = kite.place_order(
                tradingsymbol=symbol,
                exchange=kite.EXCHANGE_NFO,
                transaction_type=kite.TRANSACTION_TYPE_SELL,
                quantity=quantity,
                order_type=kite.ORDER_TYPE_MARKET,
                product=kite.PRODUCT_NRML
            )
            print("Sell Order Placed:", order_response)
            
        return 'Order placed successfully', 200
    except Exception as e:
        print("Error:", e)
        return 'Error processing order', 500

if __name__ == '__main__':
    app.run()
