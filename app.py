import csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from static.stt.voice_assistant import recognize_speech, search_type

app = Flask(__name__)
CORS(app)

# 가장 최근의 DBTI 결과를 저장할 변수
latest_dbti_result = None

# DBTI, MBTI 정보와 Dog 매칭 정보를 저장할 딕셔너리
dbti_info = {}
mbti_info = {}
dog_match = {}


# CSV 파일에서 DBTI 정보를 읽어오는 함수
def read_dbti_info():
    csv_path = "static/dbti/csv/dbti_types.csv"
    with open(csv_path, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            dbti_info[row['DBTI']] = row


# CSV 파일에서 MBTI 정보를 읽어오는 함수
def read_mbti_info():
    with open('static/mbti/csv/mbti_types.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            mbti_info[row['MBTI']] = row


# CSV 파일에서 Dog 매칭 정보를 읽어오는 함수
def read_dog_match():
    with open('static/mbti/csv/dog_match.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            dog_match[row['MBTI']] = row


# 데이터 로드
read_dbti_info()
read_mbti_info()
read_dog_match()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_dbti', methods=['POST'])
def submit_dbti():
    global latest_dbti_result
    latest_dbti_result = request.json.get('dbti')
    return jsonify({"message": "DBTI 저장 완료"}), 200


@app.route('/kakao_api', methods=['POST'])
def kakao_api():
    global latest_dbti_result

    if latest_dbti_result is None:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "DBTI 결과를 찾을 수 없습니다. 먼저 DBTI 테스트를 완료해주세요."
                        }
                    }
                ]
            }
        })

    if latest_dbti_result in dbti_info:
        dbti_data = dbti_info[latest_dbti_result]
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"견주님의 강아지는 {latest_dbti_result} 성향을 가지고 있습니다."
                        }
                    },
                    {
                        "basicCard": {
                            "title": dbti_data['Type Name'],
                            "description": dbti_data['Description'],
                            "thumbnail": {
                                "imageUrl": dbti_data['Img URL'],
                                "link": {
                                    "web": dbti_data['Site URL']
                                }
                            },
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "더 자세히 알아보기",
                                    "webLinkUrl": dbti_data['Site URL']
                                },
                                {
                                    "action": "share",
                                    "label": "결과 공유하기"
                                }
                            ]
                        }
                    },
                    {
                        "simpleText": {
                            "text": f"해당 DBTI를 가진 반려견을 키우는 방법입니다.\n" + dbti_data['Solution']
                        }
                    }
                ]
            }
        })
    else:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "DBTI 결과를 찾을 수 없습니다."
                        }
                    }
                ]
            }
        })


@app.route('/mbti_api', methods=['POST'])
def mbti_api():
    data = request.get_json()
    mbti = data.get('userRequest', {}).get('utterance', '').upper()  # 사용자 입력을 대문자로 변환

    if mbti not in mbti_info or mbti not in dog_match:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "올바른 MBTI 유형을 입력해주세요."
                        }
                    }
                ]
            }
        })

    mbti_data = mbti_info[mbti]
    dog_data = dog_match[mbti]

    dog_name = dog_data['Dog'].split(', ')[-1] if ', ' in dog_data['Dog'] else dog_data['Dog']
    wiki_url = f"https://namu.wiki/w/{dog_name}"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "음성인식으로 DBTI와 MBTI를 검색하기",
                        "description": "음성 인식은 1개국어만 지원합니다.\n(한국어, 영어)\n자동으로 리다이렉트 됩니다",
                        "thumbnail": {
                            "imageUrl": "https://i.ibb.co/SmT95WX/cat-meme.jpg"
                        },
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "더 자세히 알아보기",
                                "webLinkUrl": ""
                            }
                        ]
                    }
                }
            ]
        }
    }
    return responseBody

@app.route('/sttmenu')
def stt():
    return render_template('index2.html')

@app.route('/stt')
def stt():
    return render_template('index2.html')


@app.route('/api/speech', methods=['POST'])
def speech_call():
    try:
        text = recognize_speech()  # 음성 인식 실행

        type_name, result = search_type(text)

        if result is None:
            return jsonify({"message": "음성 인식 실패 또는 해당 데이터 없음"}), 400

        return jsonify({
            "type": type_name,
            "result": result
        })
    except Exception as e:
        return jsonify({"message": f"서버 오류: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
