# 필요한 모듈 import
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os

# Flask 애플리케이션 생성
app = Flask(__name__)
# CORS 설정 (Cross-Origin Resource Sharing)
CORS(app)

# MBTI 결과를 저장할 인메모리 딕셔너리
mbti_storage = {}

# 루트 경로 설정
@app.route('/')
def home():
    # index.html 템플릿 렌더링
    return render_template('index.html')

# MBTI 제출을 위한 엔드포인트
@app.route('/submit_mbti', methods=['POST'])
def submit_mbti():
    # 요청에서 JSON 데이터 추출
    body = request.get_json()
    print(body)  # 디버깅을 위해 요청 본문 출력

    # JSON에서 'mbti' 키의 값 추출
    mbti = body.get('mbti')
    print(f"Received MBTI: {mbti}")  # 받은 MBTI 값 출력

    # 고유 식별자 생성 (여기서는 간단히 카운터를 사용)
    identifier = len(mbti_storage) + 1
    # MBTI 결과를 인메모리 저장소에 저장
    mbti_storage[identifier] = mbti

    print(f"Stored MBTI: {mbti}")  # 저장된 MBTI 값 출력

    # 성공 응답 반환
    return jsonify({"message": "MBTI 결과가 성공적으로 저장되었습니다.", "id": identifier}), 200

# 카카오 API 엔드포인트
@app.route('/kakao_api', methods=['POST'])
def kakao_api():
    # 요청에서 JSON 데이터 추출
    body = request.get_json()
    print(body)  # 디버깅을 위해 요청 본문 출력

    # 가장 최근에 저장된 MBTI 결과 가져오기
    latest_id = max(mbti_storage.keys()) if mbti_storage else None
    mbti_result = mbti_storage.get(latest_id, 'Unknown')

    print(f"Retrieved MBTI: {mbti_result}")  # 검색된 MBTI 값 출력

    # 카카오톡 응답 형식에 맞춘 응답 본문 생성
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"당신의 MBTI는 {mbti_result}입니다."
                    }
                }
            ]
        }
    }
    # JSON 형식으로 응답 반환
    return jsonify(responseBody)

# 메인 실행 부분
if __name__ == '__main__':
    # Flask 애플리케이션 실행
    app.run(host='0.0.0.0', port=5000, debug=True)