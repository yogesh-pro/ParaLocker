from re import M
from django.shortcuts import render , HttpResponse ,redirect
from .src import ENCODE, MongoDB
import string
import random



def index(request):
    
    return render(request,"index.html")

def unlock(request,url):
    if request.method == "GET":
        password = request.GET.get("password")
        mongo = MongoDB.find(MongoDB,url)
        scramble = mongo["scrambled"]
        hints = mongo["hints"]
        print(password)
        print(scramble)
        if scramble == "True":
            decoded = ENCODE.unscramble(ENCODE,mongo["encoded"],password)
        else:
            decoded = ENCODE.revert(ENCODE,mongo["encoded"],password)
        print(decoded)
        return render(request,"unlockedpara.html",{"message":decoded,"hints":hints})

def lockedpara(request,url):
    try:
        mongo = MongoDB.find(MongoDB,url)
        # if mongo is None:
        #     raise Exception
    except:
        return HttpResponse("<h1>Something went wrong --- find</h1>")
    data = mongo
    message = data["message"]
    hints = data["hints"]
    encoded= data["encoded"]
    return render(request,"lockedpara.html",{"message":encoded,"hints":hints,"url":url,"unlock":f"unlock/{url}"
    })


def process(request):
    if request.method == "POST":
        choice = request.POST.get("choice")
        message = request.POST.get("message")
        hints = request.POST.get("hints")
        password = request.POST.get("password")
        url = ''.join(random.choice(string.ascii_letters) for x in range(10))
        if choice == "Scramble":
            scrambled = ENCODE.scramble(ENCODE,message,password)
            data_dict = {"url":url,"message":message,"hints":hints,"password":password,"encoded":scrambled,"scrambled":"True"}
            try:
                mongo = MongoDB.insert(MongoDB,data_dict)
            except:
                return HttpResponse("<h1>Something went wrong --- choice scrambled</h1>")
        elif choice == "Scramble + Change Characters":
            altered = ENCODE.alter(ENCODE,message,password)
            data_dict = {"url":url,"message":message,"hints":hints,"password":password,"encoded":altered,"scrambled":"False"}
            try:
                mongo = MongoDB.insert(MongoDB,data_dict)
            except:
                return HttpResponse("<h1>Something went wrong --- choice unscrambled</h1>")
        return redirect(f"p/{str(url)}")
