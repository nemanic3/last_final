from django.urls import path
from .views import SearchBookView, GetBookByISBNView, RecentReviewView

urlpatterns = [
    path('search/', SearchBookView.as_view(), name='search_book'),  # ✅ /api/book/search/
    path('<str:isbn>/', GetBookByISBNView.as_view(), name='get_book_by_isbn'),  # ✅ /api/book/{isbn}/
    path('recent_review/', RecentReviewView.as_view(), name='recent_review'),  # ✅ /api/book/recent_review/
]
