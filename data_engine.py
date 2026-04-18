import yfinance as yf
import pandas as pd
import numpy as np

def get_comprehensive_data(ticker_symbol: str) -> dict:
    """
    재무 지표(Fundamentals)와 기술적 지표(Technicals)를 통합 수집합니다.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        hist = ticker.history(period="1y") # 기술적 지표용 1년 데이터

        # 1. 재무 데이터 (Fundamentals)
        fundamentals = {
            "name": info.get("shortName", ticker_symbol),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "per": info.get("trailingPE", "N/A"),
            "pbr": info.get("priceToBook", "N/A"),
            "roe": info.get("returnOnEquity", "N/A"),
        }
        if isinstance(fundamentals["roe"], (int, float)):
            fundamentals["roe"] = round(fundamentals["roe"] * 100, 2)

        # 2. 기술적 지표 (Technicals) - RSI & MDD
        if not hist.empty:
            # RSI (14일 기준)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = round(rsi.iloc[-1], 2)

            # MDD (최대 낙폭)
            rolling_max = hist['Close'].cummax()
            drawdown = (hist['Close'] - rolling_max) / rolling_max
            mdd = round(drawdown.min() * 100, 2)
            
            technicals = {"rsi": current_rsi, "mdd": mdd}
        else:
            technicals = {"rsi": "N/A", "mdd": "N/A"}

        return {"fundamentals": fundamentals, "technicals": technicals}

    except Exception as e:
        return {"error": f"데이터 로드 실패: {str(e)}"}

def get_exchange_rate():
    try:
        fx = yf.Ticker("USDKRW=X")
        rate = fx.history(period="1d")['Close'].iloc[-1]
        return round(rate, 2)
    except:
        return "N/A"
