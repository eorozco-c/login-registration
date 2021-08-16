from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from .models import User,Book
# Create your views here.
def index(request):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "libros" : Book.objects.all(),
            }
            return render(request,"books.html",context)
    return redirect("/")

def create_book(request):
    if request.method == "POST":
        if "id" in request.session:
            errors = Book.objects.validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return redirect("/books")
            title = request.POST["title"]
            description = request.POST["description"]
            user_upload = User.objects.get(id=request.session["id"])
            new_book = Book.objects.create(title=title,description=description,uploaded_by=user_upload)
            new_book.users_who_like.add(user_upload)
    return redirect("/books")

def view_book(request,idBook):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            try: 
                book = Book.objects.get(id=idBook)
            except:
                return redirect("/books")
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "libro" : book,
            }
            return render(request,"view_book.html",context)
    return redirect("/")
            
def update_book(request,idBook):
    if request.method == "POST":
        if "id" in request.session:
            errors = Book.objects.validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f"/books/{idBook}")
            try:
                book = Book.objects.get(id=idBook)
            except:
                book = None
                return redirect("/books")
            book.title = request.POST["title"]
            book.description = request.POST["description"]
            book.save()
            return redirect(f"/books/{idBook}")
    return redirect("/")

def delete_book(request,idBook):
    if request.method == "GET":
        if "id" in request.session:
            try:
                book = Book.objects.get(id=idBook)
            except:
                book = None
                return redirect("/books")
            book.delete()
            return redirect("/books")
    return redirect("/")

def like_book(request,idBook):
    if request.method == "GET":
        if "id" in request.session:
            try:
                book = Book.objects.get(id=idBook)
            except:
                book = None
                return redirect(f"/books/{idBook}")
            user_upload = User.objects.get(id=request.session["id"])
            if user_upload in book.users_who_like.all():
                messages.error(request, "Usuario ya tiene este libro como favorito", "favorito")
                return redirect(f"/books/{idBook}")
            book.users_who_like.add(user_upload)
            return redirect(f"/books/{idBook}")
    return redirect("/")
