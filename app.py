import streamlit as st
import os
import google.generativeai as genai
from data_engine import get_comprehensive_data, get_exchange_rate
from analytics import generate_prompt_data_pack

st.set_page_config(page_title="Wonju AI Quant Lab V7.1", layout="wide")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.title("📈 Wonju AI Quant Lab V7.1")

with st.sidebar:
    st.header("💱 실시간 환율")
    rate = get_exchange_rate()
    st.metric("USD/KRW", f"{rate} 원")

ticker = st.text_input("종목 티커 입력 (예: NVDA, 005930.KS)", value="NVDA").upper()

if st.button("데이터 분석 실행"):
    with st.spinner("퀀트 데이터를 추출 중..."):
        full_data = get_comprehensive_data(ticker)
        
        if "error" in full_data:
            st.error(full_data["error"])
        else:
            f = full_data["fundamentals"]
            t = full_data["technicals"]
            
            # 메트릭 UI를 2줄로 배치하여 가독성 확보
            col1, col2, col3 = st.columns(3)
            col1.metric("현재가", f.get("current_price"))
            col2.metric("PER", f.get("per"))
            col3.metric("ROE", f"{f.get('roe')}%")
            
            col4, col5, col6, col7 = st.columns(4)
            col4.metric("RSI (14일)", t.get("rsi"))
            col5.metric("MDD (1년)", f"{t.get('mdd')}%")
            col6.metric("MA20", t.get("ma20"))
            col7.metric("MA60", t.get("ma60"))

            st.divider()
            st.subheader("🚀 Gemini용 데이터팩")
            data_pack_str = generate_prompt_data_pack(ticker, full_data, rate)
            st.code(data_pack_str, language='markdown')
            
            st.session_state['current_data_pack'] = data_pack_str

if st.button("Gemini에게 즉시 분석 요청"):
    if not GEMINI_API_KEY:
        st.error("API Key가 설정되지 않았습니다.")
    elif 'current_data_pack' not in st.session_state:
        st.warning("먼저 '데이터 분석 실행' 버튼을 눌러주세요.")
    else:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-pro')
            with st.spinner("AI 분석 리포트 생성 중..."):
                response = model.generate_content(st.session_state['current_data_pack'])
                st.markdown("### 📄 AI 투자 전략 리포트")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"AI 호출 오류: {e}")
