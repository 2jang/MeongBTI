import requests
from bs4 import BeautifulSoup
import csv

# MBTI 유형 리스트 정의
mbti_types = ['istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp',
              'estp', 'esfp', 'enfp', 'entp', 'estj', 'esfj', 'enfj', 'entj']

# 결과를 저장할 리스트 초기화
results = []

# 각 MBTI 유형에 대해 반복
for mbti in mbti_types:
    # 해당 MBTI 유형의 URL 생성
    url = f'https://www.16personalities.com/ko/성격유형-{mbti}'

    # 웹 페이지 요청
    response = requests.get(url)
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # end 웹 페이지 요청, 파싱

    # 크롤링 할 리소스 찾기
    try:
        # 유형 이름 찾기
        type_name = soup.find('div', class_='type-info')
        # 유형 이름이 존재하면 텍스트 추출, 없으면 "Not found" 반환
        type_name = type_name.find('span', class_='tw-block').text.strip() if type_name else "Not found"

        # 유형 코드 찾기
        type_code = soup.find('div', class_='code')
        # 유형 코드가 존재하면 텍스트 추출, 없으면 기본값 설정
        type_code = type_code.find('h1').text.strip() if type_code else f"성격 유형: {mbti.upper()}"

        # 설명 찾기 (여러 방법 시도)
        type_description = soup.find('p', class_='p--blurb p-lg tw-text-white tw-hidden medium:tw-block')
        if not type_description:
            type_description = soup.find('p', class_='tw-text-white tw-hidden medium:tw-block')
        if not type_description:
            type_description = soup.find('div', class_='type-info').find('p')

        # 설명이 존재하면 텍스트 추출, 없으면 "Description not found" 반환
        type_description = type_description.text.strip() if type_description else "Description not found"

        # end 크롤링 할 리소스 찾기

        #결과 리스트로 생성
        # 결과를 딕셔너리로 만들어 결과 리스트에 추가
        results.append({
            'MBTI': mbti.upper(),
            'Type Name': type_name,
            'Type Code': type_code,
            'Description': type_description
        })

        #end 결과 리스트로 생성

        #디버그 로깅
        # 크롤링 진행 상황 출력 (설명의 처음 50자만 표시)
        print(f"Crawled {mbti.upper()}: {type_description[:50]}...")
    except Exception as e:
        # 오류 발생 시 오류 메시지 출력
        print(f"Error crawling {mbti.upper()}: {str(e)}")

        #end 디버그 로깅

#크롤링 결과 파일 저장
# CSV 파일로 결과 저장
FILE = "/mbti/csv/mbti_types.csv"
with open(FILE, 'w', newline='', encoding='utf-8') as file:
    # CSV 작성을 위한 DictWriter 객체 생성
    writer = csv.DictWriter(file, fieldnames=['MBTI', 'Type Name', 'Type Code', 'Description'])
    # 헤더 작성
    writer.writeheader()
    # 각 결과를 CSV 파일에 작성
    for result in results:
        writer.writerow(result)
#end 크롤링 결과 파일 저장

# 크롤링 완료 메시지 출력
print("Crawling completed. Results saved " + FILE)
