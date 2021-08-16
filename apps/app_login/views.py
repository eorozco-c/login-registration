from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import User
import bcrypt
# Create your views here.

def index(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("/wall")
    return render(request, "login.html")

def create_user(request):
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
        email = request.POST["email_login"]
        password = request.POST["password_login"]
        errors = User.objects.validator_log(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)   
        try:
            usuario = User.objects.get(email=email)
        except:
            errors = {
                "email_login" : "Email no existe favor registrese"
            }
            return JsonResponse(errors) 
        if bcrypt.checkpw(password.encode(), usuario.password.encode()):
            request.session["id"] = usuario.id
            return JsonResponse({"resultado": usuario.id })
        else:
            errors = {
                "password_login" : "Contraseña incorrecta"
            }
            return JsonResponse(errors)

def success(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("/books")
        return redirect("/")

def logout(request):
    if request.method == "GET":
        if "id" in request.session:
            del request.session['id']
        return redirect("/")