from django.db import models
from apps.app_login.models import User

# Create your models here.
class BookManager(models.Manager):
    def validate(self,postData):
        errors = {}
        if postData["title"] == "":
            errors['title'] = "Titulo esta vacio"
        if len(postData["description"]) < 5:
            errors['description'] = "Descripcion debe contener un minimo de 5 caracteres"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()


