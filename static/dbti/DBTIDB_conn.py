from flask import jsonify


def save_result(request, mysql):
    mbti = request.json.get('mbti')

    if not mbti:
        return jsonify({'error': 'MBTI 데이터가 제공되지 않았습니다.'}), 400

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO easygymdb.owner_tbl (dogMbti) VALUES (%s)", (mbti,))
        mysql.connection.commit()
        cur.close()
        return 'MBTI 결과가 성공적으로 저장되었습니다.', 200
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return f'데이터베이스 오류: {str(e)}', 500
