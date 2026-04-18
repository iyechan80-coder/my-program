import yfinance as yf
import pandas as pd
import numpy as np

def get_comprehensive_data(ticker_symbol: str) -> dict:
    """
    재무 지표, RSI, MDD 및 이동평균선(MA20, MA60)을 통합 수집합니다.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        # 기술적 지표 계산을 위해 충분한 과거 데이터(1년) 로드
        hist = ticker.history(period="1y") 

        # 1. 펀더멘털 데이터 (Fundamentals)
        fundamentals = {
            "name": info.get("shortName", ticker_symbol),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "per": info.get("trailingPE", "N/A"),
            "pbr": info.get("priceToBook", "N/A"),
            "roe": info.get("returnOnEquity", "N/A"),
        }
        if isinstance(fundamentals["roe"], (int, float)):
            fundamentals["roe"] = round(fundamentals["roe"] * 100, 2)

        # 2. 기술적 지표 (Technicals)
        if not hist.empty and len(hist) >= 60:
            # RSI (14일 기준)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = round(rsi.iloc[-1], 2)

            # MDD (최대 낙폭, 1년 기준)
            rolling_max = hist['Close'].cummax()
            drawdown = (hist['Close'] - rolling_max) / rolling_max
            mdd = round(drawdown.min() * 100, 2)
            
            # MA (이동평균선 20일, 60일)
            ma20 = round(hist['Close'].rolling(window=20).mean().iloc[-1], 2)
            ma60 = round(hist['Close'].rolling(window=60).mean().iloc[-1], 2)
            
            technicals = {
                "rsi": current_rsi, 
                "mdd": mdd, 
                "ma20": ma20, 
                "ma60": ma60
            }
        else:
            # 상장된 지 얼마 안 된 종목 등 데이터 부족 시 예외 처리
            technicals = {"rsi": "N/A", "mdd": "N/A", "ma20": "N/A", "ma60": "N/A"}

        return {"fundamentals": fundamentals, "technicals": technicals}

    except Exception as e:
        # 에러 발생 시 앱 중단 방지
        return {"error": f"데이터 로드 실패: {str(e)}"}

def get_exchange_rate() -> float | str:
    """환율 데이터 로드 (결측치 방지 로직 포함)"""
    try:
        fx = yf.Ticker("USDKRW=X")
        hist = fx.history(period="1d")
        if not hist.empty:
            return round(hist['Close'].iloc[-1], 2)
        return "N/A"
    except:
        return "N/A"
