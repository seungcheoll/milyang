import streamlit as st
from openai import OpenAI

# API 키 로드
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI 자동 작성기", layout="wide")

# 사이드바 선택
option = st.sidebar.radio("🧭 생성기 선택", ["🎤 인사말씀 생성기", "📰 보도자료 생성기"])
# ✅ 페이지별 동적 타이틀
if option == "🎤 인사말씀 생성기":
    st.title("🎤 GPT 자동 연설문 작성 서비스")
elif option == "📰 보도자료 생성기":
    st.title("📰 GPT 자동 보도자료 작성 서비스")
# 좌우 컬럼 구성
col1, col2 = st.columns([1, 1])

# ========== 1. 인사말씀 생성기 ==========
if option == "🎤 인사말씀 생성기":
    with col2:
        st.header("🎤 연설문 생성 옵션")

        title = st.text_input("인사말 제목", value="시민과 함께하는 봄맞이 행사")

        greeting = st.selectbox("인사말 성격", ["대중적", "축제행사", "위원회", "명정"])
        speaker = st.selectbox("연설자 선택", ["밀양시장", "시의회 의장", "국장", "위원장"])
        audience1 = st.selectbox("청중 선택 1", ["밀양시민", "관광객", "공직자", "개별위원"])
        audience2 = st.selectbox("청중 선택 2", ["없음", "청년", "장애인", "여성단체"])
        season = st.selectbox("계절 선택", ["봄", "여름", "가을", "겨울"])
        quote = st.selectbox("인용구 선택", ["없음", "감정이입", "사자성어", "속담", "영어격언"])
        disaster = st.selectbox("재난 상황", ["없음", "재난피해", "재난복구"])

        parts = []
        parts.append(f"『{title}』의 성격은 {greeting}입니다.")
        parts.append(f"{speaker} ~님의 인사말씀은 {audience1}과(와) {audience2}를 청중으로 작성해야 합니다.")
        parts.append(f"계절적 요소인 {season}에 어울리며,")

        if quote != "없음":
            parts.append({
                "감정이입": "감정을 이입할 수 있는 문장을 1회 언급하며,",
                "사자성어": "적절한 사자성어를 1회 인용하고,",
                "속담": "속담을 활용하여 표현을 풍부하게 하며,",
                "영어격언": "영어 격언을 통해 인상 깊게 전달합니다."
            }[quote])
        else:
            parts.append("인용 없이 간결하게 구성됩니다.")

        if disaster == "재난피해":
            parts.append("최근 재난피해를 고려하여 위로와 공감을 담고,")
        elif disaster == "재난복구":
            parts.append("복구 현황과 감사 인사를 포함하며,")
        else:
            parts.append("재난 관련 내용은 포함되지 않습니다.")

        parts.append("이와 같이 전체 인사말씀은 풍부하고 품격 있게 구성되어야 합니다.")
        generated_text = " ".join(parts)

        prompt = st.text_area("✏️ 생성된 연설문 (수정 가능)", value=generated_text, height=200)

        if st.button("🎯 GPT로 생성"):
            with st.spinner("GPT 연설문 생성 중..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "당신은 연설문 작성 전문가입니다. 아래 연설문 가이드를 참고해 실제 연설문을 작성해주세요."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )
                    gpt_output = response.choices[0].message.content
                    st.session_state['speech_result'] = gpt_output
                except Exception as e:
                    st.error(f"⚠️ GPT 호출 실패: {str(e)}")

    with col1:
        st.header("📄 GPT 결과")
        speech_result = st.session_state.get('speech_result', "아직 생성된 연설문이 없습니다.")
        st.text_area("📝 GPT가 작성한 연설문", value=speech_result, height=500, key="speech_display", disabled=True)

# ========== 2. 보도자료 생성기 ==========
elif option == "📰 보도자료 생성기":
    with col2:
        st.header("🛠️ 보도자료 입력 정보")

        title = st.text_input("1. 보도자료 초안 제목", value="2025년 밀양 봄꽃축제 개최 안내")
        person = st.text_input("2. 담당자", value="홍길동")
        contact = st.text_input("3. 연락처", value="010-1234-5678")
        content = st.text_area("4. 보도자료 핵심 내용", height=300, placeholder="예: 밀양시는 오는 4월 10일부터 봄꽃축제를 개최합니다...")

        if st.button("🎯 GPT로 보도자료 생성"):
            with st.spinner("GPT가 보도자료 제목 5개와 전문을 작성 중입니다..."):
                try:
                    prompt = f"""
다음 정보를 참고하여,
제목(초안): {title}
담당자: {person}
연락처: {contact}

핵심 내용:
{content}

[출력 형식]
1. 보도자료에 적합한 제목 5개를 제안합니다.
2. 위에 제시된 정보를 기반으로 실제 언론에 배포 가능한 보도자료 전문을 작성해 주세요.  
뉴스 기사 스타일로 문장을 구성하고, 리드문(핵심요약) → 본문 내용 → 인용문 → 마무리 순으로 구성해주세요. 

[출력 예시]
보도자료 추천 제목
1, 
2, 
3, 
4,
5,

보도자료 내용
...

"""
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "당신은 보도자료 작성 전문가입니다. 포맷과 문체를 전문적으로 구성해 주세요."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )
                    gpt_output = response.choices[0].message.content
                    st.session_state['press_result'] = gpt_output
                except Exception as e:
                    st.error(f"⚠️ GPT 호출 실패: {str(e)}")

    with col1:
        st.header("📄 GPT 결과")
        press_result = st.session_state.get('press_result', "아직 생성된 보도자료가 없습니다.")
        st.text_area("📰 추천 제목 & 보도자료", value=press_result, height=600, key="press_display", disabled=True)
