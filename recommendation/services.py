import requests
from django.conf import settings

def get_book_recommendations(query, display=5):
    """
    네이버 API를 사용하여 입력된 키워드와 관련된 도서를 추천.
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    return []
