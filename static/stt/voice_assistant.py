import streamlit as st
import speech_recognition as sr
import pandas as pd
from konlpy.tag import Komoran
import os

# 페이지 설정
st.set_page_config(page_title="음성 인식 MBTI 견종 추천", page_icon="🎙️", layout="wide")

# CSS를 사용하여 디자인 개선
st.markdown("""
    <style>
.main-title {
    font-size: 3rem !important;
    color: #4A90E2;
    text-align: center;
    padding-bottom: 2rem;
}
.sub-title {
    font-size: 1.5rem;
    color: #666;
    text-align: center;
    padding-bottom: 1rem;
}
.info-box {
    background-color: #F0F7FF;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}
</style>
    """, unsafe_allow_html=True)

project_path = os.path.dirname(os.getcwd())

# Komoran 객체 생성
komo = Komoran()


# MBTI와 DBTI 데이터 로드 함수
@st.cache_data
def load_data():
    mbti_path = project_path + '/DBTI/static/mbti/csv/dog_match.csv'
    dbti_path = project_path + '/DBTI/static/dbti/csv/dbti_types.csv'
    return pd.read_csv(mbti_path), pd.read_csv(dbti_path)


# 데이터 로드
mbti_data, dbti_data = load_data()


# MBTI/DBTI 검색 함수
def search_type(text):
    nouns = komo.morphs(text)
    for noun in nouns:
        type_code = noun.upper()
        if len(type_code) == 4:
            if all(char in 'EINTFPJS' for char in type_code):
                result = mbti_data[mbti_data['MBTI'] == type_code]
                if not result.empty:
                    return 'MBTI', result.iloc[0]
            elif all(char in 'CWTNEIAL' for char in type_code):
                result = dbti_data[dbti_data['DBTI'] == type_code]
                if not result.empty:
                    return 'DBTI', result.iloc[0]
    return None, None


# 음성 인식 함수
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("말씀해 주세요...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "음성 인식에 실패했습니다. 다시 말씀해 주세요."
        except sr.RequestError:
            return "음성 인식 서비스에 접근할 수 없습니다. 네트워크 연결을 확인해 주세요."
        except:
            return "예상치 못한 오류가 발생했습니다. 다시 시도해 주세요."


# 성격 포맷팅 함수
def format_personality(personality):
    traits = personality.split('\n')
    formatted = "성격:\n"
    for i, trait in enumerate(traits, 1):
        formatted += f"{i}. {trait.strip()}\n"
    return formatted


def main():
    st.title("음성 인식 MBTI/DBTI 견종 추천")
    st.write("당신의 MBTI 또는 DBTI를 말씀해주세요!")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("🎙️ 음성 인식 시작"):
            text = recognize_speech()
            st.info(f"인식된 텍스트: {text}")

            type_name, result = search_type(text)
            if result is not None:

                if type_name == 'MBTI':
                    st.success(f"MBTI: {result['MBTI']}")
                    st.success(f"추천 견종: {result['Dog']}")
                    formatted_personality = format_personality(result['Personality'])
                    st.success(formatted_personality)
                    with col2:
                        st.image(result['Img URL'], caption=result['Dog'], use_column_width=True)

                elif type_name == 'DBTI':
                    st.success(f"DBTI: {result['DBTI']}")
                    st.success(f"Type Name: {result['Type Name']}")
                    st.success(f"Description: {result['Description']}")
                    st.success(f"Solution: {result['Solution']}")
                    with col2:
                        st.image(result['Img URL'], caption=result['Type Name'], use_column_width=True)

            else:
                st.warning("해당하는 MBTI 또는 DBTI 정보를 찾을 수 없습니다.")


if __name__ == "__main__":
    main()
