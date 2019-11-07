from django.urls import path

from . import views

urlpatterns = [
   path('', views.redirectToHomepage, name='redirectToHomepage'),
   path('homepage', views.homepage, name='homepage'),
   path('login', views.login, name='login'),
   path('register', views.register, name='register'),
   path('event_detail', views.event_detail, name='event_detail'),
 ]