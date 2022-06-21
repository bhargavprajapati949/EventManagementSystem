from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirectToCoordinator_login, name='redirectToCoordinator_login'),
    path('coordinator_login', views.coordinator_login, name='coordinator_login'),
    path('coordinator_login_require', views.coordinator_login_require, name='coordinator_login_require'),
    path('coordinator_dashboard', views.coordinator_dashboard, name='coordinator_dashboard'),

    path('coordinator_confirm_participation', views.coordinator_confirm_participation, name='coordinator_confirm_participation'),

    path('coordinator_participation_certi_issue', views.coordinator_participation_certi_issue, name='coordinator_participation_certi_issue'),
    path('issue_participation_certi/?P<reg_no>/?P<event_id>', views.issue_participation_certi, name='issue_participation_certi'),

    path('coordinator_winner_certi_issue', views.coordinator_winner_certi_issue, name='coordinator_winner_certi_issue'),
    path('issue_winner_certi/?P<reg_no>/?P<event_id>', views.issue_winner_certi, name='issue_winner_certi'),

    path('coordinator_profile', views.coordinator_profile, name='coordinator_profile'),
    path('coordinator_logout', views.coordinator_logout, name='coordinator_logout')
]