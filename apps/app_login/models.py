from django.db import models
from datetime import datetime
import re,math

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validator_reg(self,postData):
        errores = {}
        birthday =  datetime.strptime(postData['birthday'], '%Y-%m-%d')
        today = datetime.now()
        edad = today-birthday
        edad = math.floor(edad.days/365)
        if not LETTER_REGEX.match(postData["fname"]) or len(postData['fname']) < 2:
            errores['fname'] = "El nombre debe contener solo letras y tener un minimo de 2 caracteres"
        if not LETTER_REGEX.match(postData["lname"]) or len(postData['lname']) < 2:
            errores['lname'] = "El apellido debe contener solo letras y tener un minimo de 2 caracteres"
        if not EMAIL_REGEX.match(postData['email']):     
            errores['email'] = "Email invalido"
        if len(postData["password"]) < 8:
            errores['password'] = "Contraseña debe tener minimo 8 caracteres"
        if postData["password"] != postData["confirm_password"]:
            errores["password"] = "Contraseña no coincide"
        if  birthday >= today:
            errores["birthday"] = "Fecha debe ser menor al dia de hoy"
        if self.filter(email__iexact=postData["email"]).exists():
            errores["email"] = "Email ya existe, favor ingresar uno nuevo"
        if edad < 13:
            errores["edad"] = "La edad debe ser mayor a 13 años"
        return errores
    def validator_log(self,postData):
        errores = {}
        if not EMAIL_REGEX.match(postData['email']):     
            errores['email'] = "Email invalido"
        if len(postData["password"]) < 8:
            errores['password'] = "Contraseña debe tener minimo 8 caracteres"
        return errores

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
