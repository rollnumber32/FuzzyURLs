from django.shortcuts import render
import uuid


def index(request):
    request.COOKIES["key"] = str(uuid.uuid1())
    response = render(request, "index.html")
    response.set_cookie("key", str(uuid.uuid1()))
    return response
