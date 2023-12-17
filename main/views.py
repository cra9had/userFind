from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from search_base.models import SearchHistory
from django.conf import settings
from .utils import buy_full_data


class BuyFullDataAPIView(APIView):

    def get_object(self, pk):
        try:
            return SearchHistory.objects.get(pk=pk, user=self.request.user)
        except SearchHistory.DoesNotExist:
            raise

    def post(self, request):
        try:
            search = self.get_object(request.data.get("pk"))
        except SearchHistory.DoesNotExist:
            return Response({"error": "Search does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if search.status != 2:
            return Response({"error": "Search status is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user.balance <= settings.FULLDATA_PRICE_RUB:
            return Response({"error": "Недостаточно средств!\nПополните баланс"}, status=status.HTTP_400_BAD_REQUEST)
        if search.paid:
            return Response({"error": "Данные уже куплены!"}, status=status.HTTP_400_BAD_REQUEST)
        full_data = buy_full_data(self.request.user, search)
        return Response({"balance": self.request.user.balance, "result": full_data}, status=status.HTTP_200_OK)


def home(request):
    return render(request, "index.html")


def payok(request):
    return render(request, "payok_project_verification.txt")


def my(request):
    return render(request, "my.html")
