import yfinance as yf
import pandas as pd
import os

def update():
    tickers = ["WALMEX.MX", "FEMSAUBD.MX", "GMEXICOB.MX"]
    os.makedirs('data', exist_ok=True)
    
    try:
        df = yf.download(tickers, period="1y", interval="1d")['Close']
        df.to_csv('data/market_data.csv')
        print("✅ Datos guardados en data/market_data.csv")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update()