from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToHomepage, name='redirectToHomepage'),
    path('homepage', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('event_detail', views.event_detail, name='event_detail'),
    path('participant_dashboard', views.participant_dashboard, name="participant_dashboard"),
    path('participant_logout', views.participant_logout, name='participant_logout')

]