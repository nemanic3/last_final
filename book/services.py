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

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 네트워크 오류 발생 시 예외 발생

        data = response.json().get("items", [])
        formatted_data = [
            {
                "title": book["title"],
                "author": book.get("author", "Unknown Author"),
                "publisher": book.get("publisher", "Unknown Publisher"),
                "image": book.get("image", ""),
                "link": book.get("link", ""),
            }
            for book in data
        ]
        return formatted_data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_book_by_isbn_from_naver(isbn):
    """
    특정 ISBN의 책 정보 조회
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"d_isbn": isbn, "display": 1}  # ✅ ISBN 검색을 위해 "query" 대신 "d_isbn" 사용

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 네트워크 오류 발생 시 예외 발생

        data = response.json().get("items", [])
        return data[0] if data else None  # ✅ 검색 결과가 있으면 첫 번째 책 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
