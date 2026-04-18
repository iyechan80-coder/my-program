def generate_prompt_data_pack(ticker: str, data: dict, exchange_rate: float) -> str:
    """
    모든 지표를 통합하여 복사 가능한 마크다운 데이터팩을 생성합니다.
    """
    f = data.get("fundamentals", {})
    t = data.get("technicals", {})

    # RSI 상태 해석
    rsi_val = t.get("rsi", 50)
    rsi_status = "과매매 신호 없음"
    if isinstance(rsi_val, (int, float)):
        if rsi_val >= 70: rsi_status = "과매수(Overbought) 주의"
        elif rsi_val <= 30: rsi_status = "과매도(Oversold) 기회"

    data_pack = f"""### [Header]
- **종목명**: {f.get('name', 'N/A')}
- **티커**: {ticker}
- **기준 환율**: {exchange_rate} KRW/USD

### [Fundamentals]
- **현재가**: {f.get('current_price', 'N/A')}
- **PER**: {f.get('per', 'N/A')}
- **PBR**: {f.get('pbr', 'N/A')}
- **ROE**: {f.get('roe', 'N/A')}%

### [Technicals]
- **RSI (14일)**: {t.get('rsi', 'N/A')} ({rsi_status})
- **MDD (1년 최고점 대비)**: {t.get('mdd', 'N/A')}%

### [Mission]
당신은 대한민국 원주시에 본사를 둔 'Wonju AI Quant Lab'의 수석 퀀트 분석가입니다. 
위 제공된 데이터팩의 수치를 정밀 분석하여 다음을 수행하세요:
1. 해당 종목의 현재 밸류에이션(저평가/적정/고평가)을 확정하십시오.
2. RSI와 MDD를 통해 진입 시점(Timing)의 적절성을 평가하십시오.
3. 한국 투자자 관점에서 ISA 계좌를 활용한 장기 보유 가치와 리스크를 도출하십시오.
4. 최종 의견(매수/관망/매도)과 함께 목표가(Target Price)를 제시하십시오.
"""
    return data_pack
