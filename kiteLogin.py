from kiteconnect import KiteConnect
from selenium import webdriver
from pyotp import TOTP
from kiteconnect import KiteTicker
import pandas as pd
import time
from selenium.webdriver.common.by import By


def autologin():
    # Login URL
    token_path="api_key.txt"
    key_secret = open(token_path,'r').read().split()
    kite=KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver-win64/chromedriver')
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options= options.to_capabilities()
    driver = webdriver.Chrome()
    driver.get(kite.login_url())
    print(driver.current_url)
    username=driver.find_element(By.XPATH,"//input[@id='userid']")
    password=driver.find_element(By.XPATH,"//input[@id='password']")
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    driver.find_element(By.XPATH,"//button[@class='button-orange wide']").click()
    pin=driver.find_element(By.XPATH,'//input[@id="pin"]')
    totp = TOTP(key_secret[4]).now()
    pin.send_keys(totp)
    driver.find_element(By.XPATH,"//button[@class='button-orange wide']").click()
    time.sleep(2)
    request_token=driver.current_url.split('request_token')[1][:32]
    with open("request_token.txt",'w') as file:
        file.write(request_token)
    driver.quit()
    request_token=open("request_token.txt",'r').read()
    key_secret=open("key_secret.txt",'r').read().split()
    kite=KiteConnect(api_key=key_secret[0])
    data = kite.generate_session(request_token, api_secret=key_secret[1])
    with open("access_token.txt",'w') as file:
        file.write(data["access_token"])
    print("Login Successful")
    


if __name__ == '__main__':
   
    autologin()
    access_token=open("access_token.txt",'r').read()
    key_secret = open("key_secret.txt",'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    kite.set_access_token(access_token)
    print("Kite Session Login successful")

    instrument_dump=kite.instruments("NSE")
    instrument_df=pd.DataFrame(instrument_dump)
    print(instrument_df)

    #Auto Buy
    
    #steps
    #1. upload webhook url of your server// send params
    #2. using flask and ngrok make you r local machine online
    #3. trigger buy and short NFO based on conditions// params:Exchange,(NIfty/Banknifty),CE/PE,Strike Price,Quantity 


    # Fetch quote details
    quote=kite.quote("NSE:INFY")
    print(quote)