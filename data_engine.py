import yfinance as yf
import pandas as pd

def get_stock_data(ticker_symbol: str) -> dict:
    """
    주어진 종목 코드의 현재가, PER, PBR, ROE, 거래량 데이터를 수집합니다.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # yfinance 데이터 누락 대비 기본값(N/A) 처리
        data = {
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "per": info.get("trailingPE", "N/A"),
            "pbr": info.get("priceToBook", "N/A"),
            "roe": info.get("returnOnEquity", "N/A"),
            "volume": info.get("volume", "N/A"),
            "name": info.get("shortName", ticker_symbol)
        }
        
        # ROE의 경우 백분율로 변환 (데이터가 존재할 경우)
        if isinstance(data["roe"], (int, float)):
            data["roe"] = round(data["roe"] * 100, 2)
            
        return data
        
    except Exception as e:
        # 에러 발생 시 시스템 중단 방지 및 로그 반환
        return {"error": f"데이터 수집 실패: {str(e)}"}

def get_exchange_rate() -> float | str:
    """
    실시간 원/달러(USD/KRW) 환율을 조회합니다.
    """
    try:
        fx = yf.Ticker("USDKRW=X")
        current_rate = fx.info.get("regularMarketPrice", None)
        
        if not current_rate:
            # history 데이터로 대체 조회 (info 딕셔너리가 비어있을 경우)
            hist = fx.history(period="1d")
            if not hist.empty:
                current_rate = hist['Close'].iloc[-1]
            else:
                return "데이터 없음"
                
        return round(current_rate, 2)
        
    except Exception as e:
        return f"조회 오류"
