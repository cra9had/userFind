from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def my(request):
    return render(request, "my.html")
