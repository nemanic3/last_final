import requests
from django.conf import settings

def search_books_from_naver(query, display=10):
    """ 네이버 API를 이용한 도서 검색 """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # ✅ 응답이 정상적인지 확인
        if isinstance(data, dict) and "items" in data and data["items"]:
            return data["items"]  # ✅ 정상적인 리스트 반환
        return []  # ✅ 데이터가 없으면 빈 리스트 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

import requests
from django.conf import settings

import requests
from django.conf import settings

def get_book_by_isbn_from_naver(isbn):
    """
    네이버 API에서 특정 ISBN으로 책 정보 조회
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}  # ✅ d_isbn → query 로 변경 (테스트 필요)

    try:
        response = requests.get(url, headers=headers, params=params)
        print("🔍 네이버 API 요청 URL:", response.url)  # ✅ API 요청 URL 확인
        response.raise_for_status()
        data = response.json()

        print("📌 네이버 API 응답 데이터:", data)  # ✅ 응답 데이터 확인
        if "items" in data and data["items"]:
            return data["items"][0]
        return None
    except requests.exceptions.RequestException as e:
        print("🚨 네이버 API 요청 오류:", e)  # ✅ 오류 로그 출력
        return None

