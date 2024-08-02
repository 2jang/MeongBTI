from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MBTI 결과를 저장할 딕셔너리를 생성
mbti_storage = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_mbti', methods=['POST'])
def submit_mbti():
    mbti = request.json.get('mbti')
    # 새로운 식별자 생성 (현재 저장된 항목 수 + 1).
    identifier = len(mbti_storage) + 1
    mbti_storage[identifier] = mbti
    # 저장 완료 메시지와 식별자를 JSON 형식으로 반환
    return jsonify({"message": "MBTI 저장 완료", "id": identifier}), 200


@app.route('/kakao_api', methods=['POST'])
def kakao_api():
    # 저장된 MBTI 결과 중 가장 최근의 식별자를 찾습니다.
    latest_id = max(mbti_storage.keys()) if mbti_storage else None
    # 최근 식별자에 해당하는 MBTI 결과를 가져옵니다. 없으면 'Unknown'을 사용합니다.
    mbti_result = mbti_storage.get(latest_id, 'Unknown')

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{mbti_result}"
                    }
                }
            ]
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
