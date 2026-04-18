def generate_analysis_prompt(ticker: str, stock_data: dict, exchange_rate: float | str) -> str:
    """
    수집된 퀀트 데이터를 바탕으로 Gemini API에 전송할 심층 분석 프롬프트를 생성합니다.
    """
    if "error" in stock_data:
        return f"데이터를 불러오지 못해 프롬프트를 생성할 수 없습니다: {stock_data['error']}"

    # 데이터 추출 (누락 시 'N/A' 처리)
    name = stock_data.get("name", ticker)
    price = stock_data.get("current_price", "N/A")
    per = stock_data.get("per", "N/A")
    pbr = stock_data.get("pbr", "N/A")
    roe = stock_data.get("roe", "N/A")
    volume = stock_data.get("volume", "N/A")

    # 체계적인 분석을 위한 Tree of Thoughts 및 페르소나 부여
    prompt = f"""
당신은 'Wonju AI Quant Lab V7.0'의 수석 퀀트 애널리스트입니다.
아래 제공된 {name} ({ticker})의 핵심 펀더멘털 데이터를 바탕으로 심층 투자 리포트를 작성해 주세요.

[정량적 지표]
- 현재가: {price}
- PER (주가수익비율): {per}
- PBR (주가순자산비율): {pbr}
- ROE (자기자본이익률): {roe}%
- 최근 거래량: {volume}
- 현재 원/달러 환율: {exchange_rate} 원

[분석 지침]
1. 위 지표들을 종합하여 현재 주가의 고평가/저평가 여부를 진단하세요. (RSI, 볼린저 밴드 등 기술적 지표와의 결합 필요성도 언급할 것)
2. 토스증권 등 모바일 플랫폼을 활용한 소수점 적립식 매수(예: 2주 단위 분할 매수) 전략의 유효성을 평가하세요.
3. 이 종목을 중장기적 관점에서 ISA(개인종합자산관리계좌)에 편입하여 10년 이상 복리 효과를 노릴 때의 세제 혜택 시너지와 리스크(MDD 등)를 분석하세요.
4. 결론적으로 매수, 보류, 매도 중 하나의 의견을 제시하고, 1차 목표가를 논리적으로 산출해 주세요.

답변은 마크다운 형식으로, 서론 없이 본론(분석 내용)부터 전문적이고 간결하게 작성해 주십시오.
"""
    return prompt
