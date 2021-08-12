from django.http.response import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User,Message,Comment

# Create your views here.
def wall(request):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "message_users" : Message.objects.all(),
                "comments" : Comment.objects.all(),
            }
            return render(request, "wall.html", context)
    return redirect("/")

def create_message(request):
    if request.method == "POST":
        if "id" in request.session:
            errors = Message.objects.validate_messages(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/wall")
            idusuario = request.session["id"]
            usuario = User.objects.get(id=idusuario)
            mensaje = request.POST["create_message"]
            Message.objects.create(user=usuario,message=mensaje)
            return redirect("/wall")
    return redirect("/")

def comment_message(request, idMesagge):
    if request.method == "POST":
        if "id" in request.session:
            idusuario = request.session["id"]
            usuario = User.objects.get(id=idusuario)
            try:
                mensaje = Message.objects.get(id=idMesagge)
            except:
                return redirect("/wall")
            comentario = request.POST["comment_message"]
            Comment.objects.create(user=usuario,message=mensaje,comment=comentario)
            return redirect("/wall")
    return redirect("/")

def comment_delete(request,idComment):
    if request.method == "GET":
        if "id" in request.session:
            errors = Comment.objects.validate_comments(idComment)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/wall")
            try:
                del_comment = Comment.objects.get(id=idComment)
                del_comment.delete()
            except:
                del_comment = None
            return redirect("/wall")
    return redirect("/")