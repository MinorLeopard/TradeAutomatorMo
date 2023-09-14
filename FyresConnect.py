from fyers_api import accessToken
from selenium import webdriver
from selenium.webdriver.common.by import By

token_path="FyresAuth.txt"
key_secret = open(token_path,'r').read().split()
client_id = key_secret[0]
secret_key = key_secret[1]
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"

session=accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri, 
    response_type=response_type
)

response = session.generate_authcode()
print(response)
