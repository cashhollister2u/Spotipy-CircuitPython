# conventional 
from os import getenv
from components.network_connect import requests

# stocks
STOCK = getenv("STOCK")
TWELVE_API_KEY = getenv("TWELVE_API_KEY")

#collects financial data from twelve data api
def getStockInstance(): 
    STOCK_URL = f"https://api.twelvedata.com/quote?symbol={STOCK}&apikey={TWELVE_API_KEY}"

    try:
        print("Loading...")
        with requests.get(STOCK_URL) as response:
            print("---Done---")
            return response.json()
    
    except Exception as e:
        print("Error instance stock data :", e)

def getStockDataGraph(output_size): 
    STOCK_URL = f"https://api.twelvedata.com/time_series?symbol={STOCK}&interval=5min&outputsize={output_size}&apikey={TWELVE_API_KEY}"

    try:
        print("Loading...")
        with requests.get(STOCK_URL) as response:
            print("---Done---")
            return response.json()
    
    except Exception as e:
        print("Error stock graph data:", e)