from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToHomepage, name='redirectToHomepage'),
    path('homepage', views.homepage, name='homepage'),
    path('event_detail', views.event_detail, name='event_detail'),

    path('participant_login', views.participant_login, name='participant_login'),
    path('participant_login_require', views.participant_login_require, name='participant_login_require'),
    path('register', views.register, name='register'),
    
    path('participant_dashboard', views.participant_dashboard, name="participant_dashboard"),
    path('do_payment', views.do_payment, name="do_payment"),
    path('profile_participant', views.profile_participant, name='profile_participant'),
    
    path('participant_logout', views.participant_logout, name='participant_logout')
]