from django.shortcuts import render, redirect, HttpResponse
from .src import ENCODE, MongoDB
import string
import random


def index(request):
    return render(request, "index.html")


def unlock(request, url):
    if request.method == "GET":
        password = request.GET.get("password")
        if not password:
            return HttpResponse("<h1>Password is required</h1>")

        mongo = MongoDB().find({"url": url})
        if not mongo:
            return HttpResponse("<h1>Invalid URL or data not found</h1>")

        scramble_flag = mongo["scrambled"]
        encoded_message = mongo["encoded"]
        hints = mongo["hints"]

        encoder = ENCODE()
        if scramble_flag == "True":
            decoded = encoder.unscramble(encoded_message, password)
        else:
            return HttpResponse("<h1>Unsupported encoding method</h1>")

        return render(request, "unlockedpara.html", {"message": decoded, "hints": hints})


def lockedpara(request, url):
    mongo = MongoDB().find({"url": url})
    if not mongo:
        return HttpResponse("<h1>Invalid URL or data not found</h1>")

    return render(request, "lockedpara.html", {
        "message": mongo["encoded"],
        "hints": mongo["hints"],
        "url": url,
        "unlock": f"unlock/{url}"
    })


def process(request):
    if request.method == "POST":
        choice = request.POST.get("choice")
        message = request.POST.get("message")
        hints = request.POST.get("hints")
        password = request.POST.get("password")

        if not all([choice, message, hints, password]):
            return HttpResponse("<h1>All fields are required</h1>")

        if choice != "Scramble":
            return HttpResponse("<h1>Invalid encoding choice</h1>")

        # Generate a unique URL identifier
        url = ''.join(random.choices(string.ascii_letters, k=10))
        encoder = ENCODE()
        scrambled_message = encoder.scramble(message, password)

        data_dict = {
            "url": url,
            "message": message,
            "hints": hints,
            "password": password,
            "encoded": scrambled_message,
            "scrambled": "True"
        }

        try:
            MongoDB().insert(data_dict)
        except Exception as e:
            return HttpResponse(f"<h1>Something went wrong: {e}</h1>")

        return redirect(f"p/{str(url)}")
