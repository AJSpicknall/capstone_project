from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "main/home.html")


def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "main/about.html")
