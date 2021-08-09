from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse
from .models import *
import bcrypt
# Create your views here.

def index(request):
    return render(request, "login.html")

def create(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        errors = User.objects.validator_reg(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)
        usuario = User.objects.create(first_name=fname,last_name=lname,email=email,password=password_hs,birthday=birthday)
        request.session["id"] = usuario.id
        return JsonResponse({"resultado": usuario.id })

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        errors = User.objects.validator_log(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)   
        try:
            usuario = User.objects.get(email=email)
        except:
            errors = {
                "none" : "Email no existe favor registrese"
            }
            return JsonResponse(errors) 
        if bcrypt.checkpw(password.encode(), usuario.password.encode()):
            request.session["id"] = usuario.id
            return JsonResponse({"resultado": usuario.id })
        else:
            errors = {
                "password" : "Contraseña incorrecta"
            }
            return JsonResponse(errors)



def success(request):
    if request.method == "GET":
        if "id" in request.session:
            try:
                usuario = User.objects.get(id=request.session["id"])
            except:
                usuario = None
            context = {
                "usuario" : usuario
            }
            return render(request, "success.html", context)
        return redirect("/")

def logout(request):
    if request.method == "GET":
        del request.session['id']
        return redirect("/")