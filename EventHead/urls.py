from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToEventHead_login, name='redirectToEventHead_login'),
    path('eventHead_login', views.eventHead_login, name='eventHead_login'),
    path('eventHead_dashboard', views.eventHead_dashboard, name='eventHead_dashboard'),
    path('attendance', views.attendance, name="attendance"),
    path('participation_info', views.participation_info, name="participation_info"),
    path('enter_result', views.enter_result, name="enter_result"),
    path('event_head_profile', views.event_head_profile, name="event_head_profile"),
    path('logout', views.logout, name="logout")
]