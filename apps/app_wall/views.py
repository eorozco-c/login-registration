from django.http.response import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User,Message,Comment
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "es_cl") 
# Create your views here.
def wall(request):
    if request.method == "GET":
        if "id" in request.session:
            idusuario = request.session["id"]
            context = {
                "usuario" : User.objects.get(id=idusuario),
                "message_users" : Message.objects.all().order_by("-id"),
                "comments" : Comment.objects.all(),
            }
            return render(request, "wall.html", context)
    return redirect("/")

def create_message(request):
    if request.method == "POST":
        if "id" in request.session:
            errors = Message.objects.validate_messages(request.POST)
            if len(errors) > 0:
                return JsonResponse(errors)
            idusuario = request.session["id"]
            usuario = User.objects.get(id=idusuario)
            mensaje = request.POST["create_message"]
            new_message = Message.objects.create(user=usuario,message=mensaje)
            data = {
                "id" : new_message.id,
                "message" : new_message.message,
                "first_name" : new_message.user.first_name,
                "last_name" : new_message.user.last_name,
                "created_at" : datetime.strftime(new_message.created_at, "%d de %B de %Y a las %H:%M")
            }
            return JsonResponse(data)
    return redirect("/")

def comment_message(request, idMesagge):
    if request.method == "POST":
        if "id" in request.session:
            #print(request.POST["comment_message"])
            errors = Comment.objects.validate_comments(request.POST)
            if len(errors) > 0:
                errors["idMesagge"] = idMesagge
                return JsonResponse(errors)
            idusuario = request.session["id"]
            usuario = User.objects.get(id=idusuario)
            try:
                mensaje = Message.objects.get(id=idMesagge)
            except:
                return JsonResponse({"errors": "No se puede comentar en esta publicacion"})
            comentario = request.POST["comment_message"]
            new_commentario = Comment.objects.create(user=usuario,message=mensaje,comment=comentario)
            data = {
                "id" : new_commentario.id,
                "idMessage" : new_commentario.message.id,
                "message" : new_commentario.message.message,
                "first_name" : new_commentario.user.first_name,
                "last_name" : new_commentario.user.last_name,
                "comment" : new_commentario.comment,
                "created_at" : datetime.strftime(new_commentario.created_at, "%d de %B de %Y a las %H:%M")
            }
            return JsonResponse(data)
    return redirect("/")

def comment_delete(request,idComment):
    if request.method == "GET":
        if "id" in request.session:
            errors = Comment.objects.validate_comments_delete(idComment)
            if len(errors) > 0:
                errors["idComment"] = idComment
                return redirect("/wall")
            try:
                del_comment = Comment.objects.get(id=idComment)
                id_comment = del_comment.id
                del_comment.delete()
            except:
                del_comment = None
                errors["idComment"] = idComment
                return redirect("/wall")
            print(id_comment)
            return redirect("/wall")
    return redirect("/")