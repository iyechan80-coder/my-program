import streamlit as st
import google.generativeai as genai
from data_engine import get_stock_data, get_exchange_rate
from analytics import generate_analysis_prompt

# 페이지 기본 설정
st.set_page_config(page_title="Wonju AI Quant Lab V7.0", layout="wide")

st.title("📈 Wonju AI Quant Lab V7.0")
st.markdown("모듈화된 데이터 엔진과 Gemini AI를 결합한 심층 퀀트 투자 분석 시스템")

# 사이드바: 설정 및 환율 정보
with st.sidebar:
    st.header("⚙️ 시스템 설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.divider()
    
    st.header("💱 실시간 거시 지표")
    exchange_rate = get_exchange_rate()
    st.metric(label="USD/KRW 환율", value=f"{exchange_rate} 원")

# 메인 화면: 티커 입력
ticker_input = st.text_input("분석할 종목 티커를 입력하세요 (예: NVDA, 005930.KS)", value="NVDA").upper()

if st.button("데이터 수집 및 메트릭 확인"):
    with st.spinner("데이터를 불러오는 중입니다..."):
        stock_data = get_stock_data(ticker_input)
        
        if "error" in stock_data:
            st.error(stock_data["error"])
        else:
            st.success("데이터 수집 완료!")
            
            # 메트릭 카드 레이아웃 구성
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("현재가", f"{stock_data.get('current_price', 'N/A')}")
            col2.metric("PER", f"{stock_data.get('per', 'N/A')}")
            col3.metric("PBR", f"{stock_data.get('pbr', 'N/A')}")
            col4.metric("ROE", f"{stock_data.get('roe', 'N/A')} %")
            
            # 데이터를 세션 스테이트에 저장하여 AI 분석 시 활용
            st.session_state['stock_data'] = stock_data
            st.session_state['ticker'] = ticker_input

st.divider()

# AI 분석 섹션
st.subheader("🤖 Gemini 심층 투자 리포트")

if st.button("Gemini 분석 실행"):
    if not api_key:
        st.warning("사이드바에 Gemini API Key를 입력해 주세요.")
    elif 'stock_data' not in st.session_state:
        st.warning("먼저 '데이터 수집 및 메트릭 확인' 버튼을 눌러 데이터를 확보해 주세요.")
    else:
        with st.spinner("Wonju AI Quant Lab 모델이 분석을 진행 중입니다..."):
            try:
                # Gemini API 설정
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-pro') # V7.0 성능을 위해 Pro 모델 권장
                
                # 프롬프트 생성 및 호출
                prompt = generate_analysis_prompt(
                    st.session_state['ticker'], 
                    st.session_state['stock_data'], 
                    exchange_rate
                )
                
                response = model.generate_content(prompt)
                
                # 결과 출력
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"AI 분석 중 오류가 발생했습니다: {str(e)}")
