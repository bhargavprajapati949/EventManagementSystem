from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToEventHead_login, name='redirectToEventHead_login'),
    path('eventHead_login', views.eventHead_login, name='eventHead_login'),
    path('eventHead_dashboard', views.eventHead_dashboard, name='eventHead_dashboard')
]