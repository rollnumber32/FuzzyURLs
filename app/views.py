import json
import os
from django.shortcuts import render, redirect
import uuid
import urllib3
from pymongo import MongoClient
from django.core.mail import send_mail
from django.conf import settings

client = MongoClient(os.environ.get("URI"))
db = client[os.environ.get("database")]
collection = db[os.environ.get("collection")]
tokendb = db[os.environ.get("tokendb")]


def index(request):
    request.COOKIES["key"] = str(uuid.uuid1())
    response = render(request, "index.html")
    response.set_cookie("key", str(uuid.uuid1()))
    return response


def short(request):
    if request.method == "POST":
        user = request.COOKIES.get("key")
        url = request.POST["link"]

        if url.find("127.0.0.1") == 1:
            return render(request, "index.html", {"status": "Funny"})

        http = urllib3.PoolManager()
        valid = False

        if not url.startswith("http"):
            url = "http://" + url

        try:
            ret = http.request("GET", url)
            if ret.status == 200:
                valid = True
        except Exception as e:
            valid = False

        if valid == True:
            new_url = str(uuid.uuid4())[:5]
            surl = "127.0.0.1/" + new_url
            sch = {"uid": user, "link": url, "new": surl}
            collection.insert_one(sch)
            return render(
                request, "short.html", {"user": user, "url": url, "new": surl}
            )
        else:
            return render(request, "index.html", {"status: False"})

    return redirect("/")


def mailing(request):
    if request.method == "POST":
        mail = request.POST["mail"]
        user = request.COOKIES.get("key")
        details = collection.find_one({"uid": user})
        # details = json.loads(details)
        msg = f"Hey,\nThanks for using FuzzyURLs.\nThe shortened link for {details['link']} is: {details['new']}.\nRegards,\nLakshay Mittal"
        surl = details["new"]
        try:
            send_mail("FuzzyURLs", msg, settings.EMAIL_HOST_USER, [mail])
            return render(
                request, "short.html", {"user": user, "new": surl, "success": True}
            )
        except Exception as e:
            print(e)
            return render(
                request, "short.html", {"user": user, "new": surl, "success": False}
            )
    return redirect("/")
