from .views import SearchAPIView, SearchResultAPIView
from django.urls import path


urlpatterns = [
    path("search/", SearchAPIView.as_view(), name="search"),
    path("search/result/<int:search_pk>/", SearchResultAPIView.as_view(), name="search-result")
]
