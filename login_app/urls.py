from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('success',views.success),#disabling it for the wall to work
    path('logout',views.logout),
]
