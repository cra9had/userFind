import json

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import SearchCreateSerializer, SearchSerializer
from .models import SearchHistory
from django.core.cache import cache

from .utils import update_search_cache


class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SearchCreateSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return SearchHistory.objects.get(pk=pk, user=self.request.user)

    def get(self, request, search_pk: int):
        try:
            search = self.get_object(pk=search_pk)
        except SearchHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if search.status == 0:  # In process
            return Response({"status": "In progress"}, status=status.HTTP_204_NO_CONTENT)

        elif search.status == 1:
            return Response({"status": 404, "details": search.get_status_display()},
                            status=status.HTTP_200_OK)
        elif search.status == 2:
            dumped_json = cache.get(f"search_{search.pk}")
            if not dumped_json:
                dumped_json = update_search_cache(search_pk)
            return Response({"status": 200, "result": {**json.loads(dumped_json)}}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SearchHistoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchSerializer

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by("-date_created")
