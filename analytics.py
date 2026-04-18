def generate_prompt_data_pack(ticker: str, data: dict, exchange_rate: float | str) -> str:
    """
    MA와 MDD를 포함하여 AI에게 전달할 데이터팩을 생성합니다.
    """
    f = data.get("fundamentals", {})
    t = data.get("technicals", {})

    # 골든크로스/데드크로스 여부 판별 (단순화된 컨텍스트 주입)
    ma_status = "판별 불가"
    if isinstance(t.get('ma20'), (int, float)) and isinstance(t.get('ma60'), (int, float)):
        if t['ma20'] > t['ma60']: ma_status = "정배열 (상승 추세)"
        elif t['ma20'] < t['ma60']: ma_status = "역배열 (하락 추세)"

    data_pack = f"""### [Header]
- **종목명**: {f.get('name', 'N/A')} ({ticker})
- **기준 환율**: {exchange_rate} KRW/USD

### [Fundamentals]
- **현재가**: {f.get('current_price', 'N/A')}
- **PER/PBR**: {f.get('per', 'N/A')} / {f.get('pbr', 'N/A')}
- **ROE**: {f.get('roe', 'N/A')}%

### [Technicals]
- **RSI (14일)**: {t.get('rsi', 'N/A')}
- **MDD (1년 최고점 대비)**: {t.get('mdd', 'N/A')}%
- **MA20 (20일 선)**: {t.get('ma20', 'N/A')}
- **MA60 (60일 선)**: {t.get('ma60', 'N/A')} ({ma_status})

### [Mission]
위 데이터를 바탕으로 다음을 수행하세요:
1. 펀더멘털(PER, ROE) 대비 현재가 밸류에이션 평가.
2. 기술적 지표(RSI, MDD, MA 정/역배열)를 종합한 단기 진입 타점 분석.
3. 매수/관망/매도 최종 의견 및 1차 목표가 제시.
"""
    return data_pack
