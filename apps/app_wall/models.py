from django.db import models
from apps.app_login.models import User
from datetime import datetime

# Create your models here.
class  MessageManager(models.Manager):
    def validate_messages(self,postData):
        errors = {}
        if postData["create_message"] == "":
            errors["create_message"] = "Publicacion vacia"
        return errors

class Message(models.Model):
    user = models.ForeignKey(User, related_name="users_messages",on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class  CommentManager(models.Manager):
    def validate_comments_delete(self,id):
        errors = {}
        try:
            comentario = self.get(id=id)
            fecha_creacion = comentario.created_at
            fecha_actual = datetime.now()
            diferencia = fecha_actual - fecha_creacion
            diferenciaInt = diferencia.total_seconds() / 60
            if diferenciaInt > 30:
                errors["datetime"] = "No puedes eliminar un mensaje despues de haberlo creado hace mas de 30 minutos"
        except:
            comentario = None
        return errors
    def validate_comments(self,postData):
        errors = {}
        if postData["comment_message"] == "":
            errors["comment_message"] = "Comentario Vacio"
        return errors
            



class Comment(models.Model):
    user = models.ForeignKey(User, related_name="users_comments",on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="messages_comments",on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()