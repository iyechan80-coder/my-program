import streamlit as st
import os
import google.generativeai as genai
from data_engine import get_comprehensive_data, get_exchange_rate
from analytics import generate_prompt_data_pack

# 페이지 설정
st.set_page_config(page_title="Wonju AI Quant Lab V7.0", layout="wide")

# [보안 강화] API 키 로드 (UI 입력칸 제거)
# 로컬 테스트 시에는 .env 파일이나 OS 환경 변수를 설정하세요.
# Streamlit Cloud에서는 Settings > Secrets에 GEMINI_API_KEY를 등록하세요.
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.title("📈 Wonju AI Quant Lab V7.0")
st.info("보안 정책에 따라 API Key는 시스템 내부에서 안전하게 관리됩니다.")

# 사이드바: 환율 정보
with st.sidebar:
    st.header("💱 실시간 환율")
    rate = get_exchange_rate()
    st.metric("USD/KRW", f"{rate} 원")

# 메인 UI
ticker = st.text_input("종목 티커 입력 (예: NVDA, 005930.KS)", value="NVDA").upper()

if st.button("데이터 분석 실행"):
    with st.spinner("퀀트 데이터를 추출 중..."):
        full_data = get_comprehensive_data(ticker)
        
        if "error" in full_data:
            st.error(full_data["error"])
        else:
            # 1. 주요 지표 요약 (Metrics)
            f = full_data["fundamentals"]
            t = full_data["technicals"]
            
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("현재가", f.get("current_price"))
            c2.metric("PER", f.get("per"))
            c3.metric("ROE", f"{f.get('roe')}%")
            c4.metric("RSI", t.get("rsi"))
            c5.metric("MDD", f"{t.get('mdd')}%")

            # 2. [핵심 기능] 프롬프트 데이터팩 섹션
            st.divider()
            st.subheader("🚀 Gemini용 데이터팩 (Prompt Data Pack)")
            st.write("아래 코드를 복사하여 Gemini 창에 붙여넣거나, 하단 버튼을 눌러 즉시 분석하세요.")
            
            data_pack_str = generate_prompt_data_pack(ticker, full_data, rate)
            st.code(data_pack_str, language='markdown')
            
            # 세션 스테이트 저장
            st.session_state['current_data_pack'] = data_pack_str

# 3. 인앱 Gemini 분석
if st.button("Gemini에게 즉시 분석 요청"):
    if not GEMINI_API_KEY:
        st.error("API Key가 설정되지 않았습니다. 관리자에게 문의하세요.")
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
