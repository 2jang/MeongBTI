import requests
from bs4 import BeautifulSoup
import csv

mbti_types = ['istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp',
              'estp', 'esfp', 'enfp', 'entp', 'estj', 'esfj', 'enfj', 'entj']

results = []

for mbti in mbti_types:
    url = f'https://www.16personalities.com/ko/성격유형-{mbti}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # 유형 이름 찾기
        type_name = soup.find('div', class_='type-info')
        type_name = type_name.find('span', class_='tw-block').text.strip() if type_name else "Not found"

        # 설명 찾기 (여러 방법 시도)
        type_description = soup.find('p', class_='p--blurb p-lg tw-text-white tw-hidden medium:tw-block')
        if not type_description:
            type_description = soup.find('p', class_='tw-text-white tw-hidden medium:tw-block')
        if not type_description:
            type_description = soup.find('div', class_='type-info').find('p')

        type_description = type_description.text.strip() if type_description else "Description not found"

        results.append({
            'MBTI': mbti.upper(),
            'Type Name': type_name,
            'Description': type_description
        })

        print(f"Crawled {mbti.upper()}: {type_description[:50]}...")
    except Exception as e:
        print(f"Error crawling {mbti.upper()}: {str(e)}")

# CSV 파일로 결과 저장
with open('../mbti/csv/mbti_types.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['MBTI', 'Type Name', 'Type Code', 'Description'])
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Crawling completed. Results saved to mbti_types.csv")