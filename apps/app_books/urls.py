from django.urls import  path
from . import views

urlpatterns = [
    path('',views.index),
    path('create',views.create_book),
    path('<int:idBook>',views.view_book),
    path('update/<int:idBook>',views.update_book),
    path('delete/<int:idBook>',views.delete_book),
    path('like/<int:idBook>',views.like_book),
    ]
