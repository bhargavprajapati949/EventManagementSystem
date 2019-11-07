from django.urls import path

from . import views

urlpatterns = [
   path('', views.redirectToAdmin_login, name='redirectToAdmin_login'),
   path('admin_login', views.admin_login, name='admin_login'),
   path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
   path('participant_manager', views.participant_manager, name='participant_manager'),
   path('volunteer_manager', views.volunteer_manager, name='volunteer_manager'),
   path('event_head_manager', views.event_head_manager, name='event_head_manager'),
   path('coordinator_manager', views.coordinator_manager, name='coordinator_manager'),
   path('collage_manager', views.collage_manager, name='collage_manager'), 
   path('collect_money', views.collect_money, name='collect_money'),
   path('signout', views.signout, name='signout'),
]