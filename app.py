from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MBTI 결과를 저장할 딕셔너리를 생성
dbti_storage = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_mbti', methods=['POST'])
def submit_mbti():
    print("Received request:", request.json)  # 이 줄을 추가
    dbti = request.json.get('dbti')
    # 새로운 식별자 생성 (현재 저장된 항목 수 + 1).
    identifier = len(dbti_storage) + 1
    dbti_storage[identifier] = dbti
    # 저장 완료 메시지와 식별자를 JSON 형식으로 반환
    return jsonify({"message": "MBTI 저장 완료", "id": identifier}), 200


@app.route('/kakao_api', methods=['POST'])
def kakao_api():
    # 저장된 MBTI 결과 중 가장 최근의 식별자를 찾습니다.
    latest_id = max(dbti_storage.keys()) if dbti_storage else None
    # 최근 식별자에 해당하는 MBTI 결과를 가져옵니다. 없으면 'Unknown'을 사용합니다.
    dbti_result = dbti_storage.get(latest_id, 'Unknown')

    print("dbti : "+dbti_result)
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{dbti_result}"
                    }
                }
            ]
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
