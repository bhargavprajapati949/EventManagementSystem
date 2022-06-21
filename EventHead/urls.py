from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToEventHead_login, name='redirectToEventHead_login'),
    path('eventHead_login', views.eventHead_login, name='eventHead_login'),
    path('eventHead_login_require', views.eventHead_login_require, name='eventHead_login_require'),
    path('eventHead_dashboard', views.eventHead_dashboard, name='eventHead_dashboard'),

    path('attendance/?P<event_id>', views.attendance, name="attendance"),
    path('mark_attendance/?P<reg_no>/?P<event_id>', views.mark_attendance, name="mark_attendance"),

    path('winner_entry/?P<event_id>', views.winner_entry, name="winner_entry"),

    path('event_head_profile', views.event_head_profile, name="event_head_profile"),
    path('eventHead_logout', views.eventHead_logout, name="eventHead_logout")
]