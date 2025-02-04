import requests
from django.conf import settings

def search_books_from_naver(query, display=10):
    """
    네이버 API를 이용한 도서 검색
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

def get_book_by_isbn_from_naver(isbn):
    """
    특정 ISBN의 책 정보 조회
    """
    return search_books_from_naver(isbn, display=1)
