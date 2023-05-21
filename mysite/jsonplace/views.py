import json
import requests
from django.http import HttpResponse
from django.shortcuts import render


def index(request):

    data = requests.get("https://jsonplaceholder.typicode.com/todos/")
    data = data.json()
    with open("files.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)

    return render(request, "jsonplace/index.html", {"data": data})
