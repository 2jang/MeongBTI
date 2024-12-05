import speech_recognition as sr
import pandas as pd
import os

# 프로젝트 경로 설정
project_path = os.path.dirname(os.getcwd())  # 현재 작업 디렉토리 기준으로 경로 설정

# 음성 인식 함수
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            # 구글 음성 인식 사용
            text = r.recognize_google(audio, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "음성 인식에 실패했습니다. 다시 말씀해 주세요."
        except sr.RequestError:
            return "음성 인식 서비스에 접근할 수 없습니다. 네트워크 연결을 확인해 주세요."
        except Exception as e:
            return f"예상치 못한 오류: {e}"

# MBTI/DBTI 데이터 로드 함수
def load_data():
    # mbti_path와 dbti_path를 나중에 합치기
    mbti_path = os.path.join(project_path, 'DBTI', 'static', 'mbti', 'csv', 'dog_match.csv')
    dbti_path = os.path.join(project_path, 'DBTI', 'static', 'dbti', 'csv', 'dbti_types.csv')

    try:
        # 절대 경로를 사용하여 파일 읽기
        mbti_data = pd.read_csv(mbti_path)
        dbti_data = pd.read_csv(dbti_path)
        return mbti_data, dbti_data
    except Exception as e:
        return None, None

# MBTI/DBTI 검색 함수
def search_type(text):
    mbti_data, dbti_data = load_data()

    if mbti_data is None or dbti_data is None:
        return None, None

    # 텍스트에서 단어 추출 (공백을 기준으로 분리)
    search_words = text.lower().split()

    # MBTI와 DBTI 데이터에서 검색
    for word in search_words:
        # 대문자로 변환하여 검색
        word = word.upper()

        if word in mbti_data['MBTI'].str.upper().values:  # MBTI 데이터에서 대문자로 검색
            result = mbti_data[mbti_data['MBTI'].str.upper() == word]
            return "MBTI", result.iloc[0].to_dict() if not result.empty else None
        elif word in dbti_data['DBTI'].str.upper().values:  # DBTI 데이터에서 대문자로 검색
            result = dbti_data[dbti_data['DBTI'].str.upper() == word]
            return "DBTI", result.iloc[0].to_dict() if not result.empty else None
        else:
            return "WordError", search_words

    return "SearchError", text

# 음성 인식 시작 예시
if __name__ == "__main__":
    text = recognize_speech()  # 음성 인식 함수 호출
    result_type, result_data = search_type(text)  # 검색 함수 호출
    if result_data:
        print(f"검색 결과: {result_type} - {result_data}")
    else:
        print("검색 결과 없음")
