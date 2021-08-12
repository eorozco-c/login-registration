from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall),
    path('create', views.create_message),
    path('comment_message/<int:idMesagge>', views.comment_message),
    path('comment_delete/<int:idComment>', views.comment_delete),
]
