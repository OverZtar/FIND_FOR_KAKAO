import os
import requests
import json
from dotenv import load_dotenv

#같은 폴더에 있는 .env 파일의 환경변수를 로드
load_dotenv()

#.env 파일에서 카카오 키를 안전하게 가져옵니다.
KAKAO_REST_KEY = 'KAKAO API KEY GO'

#키가 제대로 로드되지 않았을 때 예외 처리
if not KAKAO_REST_KEY:
    print("오류: 같은 폴더에서 .env 파일을 찾을 수 없거나 KAKAO_REST_KEY가 비어있습니다!")
    print("조치: .env 파일을 생성하고 KAKAO_REST_KEY=내_카카오_키 형태롤 입력해주세요.")
    exit()

URL = 'https://dapi.kakao.com/v2/local/search/keyword.json'

headers = {
    "Authorization": f"KakaoAK {KAKAO_REST_KEY.strip()}"
}

params = {
    "query": "", #찾고싶은것 찾기
    "size": 15  #최적의 사이즈 15
}

print("[로컬 PC 구동] 카카오 맵 엔진 기반 데이터 수집 시작...")

try:
    response = requests.get(URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        places = data.get('documents', [])
        
        print("\n" + "="*80)
        print(f"데이터 수집 성공! 총 {len(places)}개를 찾았습니다.")
        
        for place in places:
            name = place.get('place_name')
            address = place.get('road_address_name') or place.get('address_name')
            lng = place.get('x')  # 경도
            lat = place.get('y')  # 위도
            print(f"{name:<25} | {address:<45} | ({lat}, {lng})")
            
        #내 컴퓨터의 현재 프로젝트 폴더에 json 파일로 저장됩니다.
        with open('kakao_hadan_stores.json', 'w', encoding='utf-8') as f:
            json.dump(places, f, ensure_ascii=False, indent=4)
        print("-" * 80)
        print("💾 'kakao_hadan_stores.json' 파일이 현재 폴더에 성공적으로 저장되었습니다!")
        
    else:
        print(f"❌ 오류 발생 (HTTP 상태코드: {response.status_code})")
        print("💬 상세 내용:", response.text)

except Exception as e:
    print(f"🚨 코드 실행 에러: {e}")