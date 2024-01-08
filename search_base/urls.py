from .views import SearchAPIView, SearchResultAPIView, SearchHistoryAPIView
from django.urls import path


urlpatterns = [
    path("search/", SearchAPIView.as_view(), name="search"),
    path("search/history/", SearchHistoryAPIView.as_view(), name="search-history"),
    path("search/result/<int:search_pk>/", SearchResultAPIView.as_view(), name="search-result")
]
