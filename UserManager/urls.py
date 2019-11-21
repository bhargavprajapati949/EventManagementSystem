from django.urls import path

from . import views

urlpatterns = [
    path('', views.eventCommittee, name="eventCommittee"),
    path('eventCommitteeRegForm', views.eventCommitteeRegForm, name="eventCommitteeRegForm"),
    path('successRegAsEventCommittee', views.successRegAsEventCommittee, name="successRegAsEventCommittee"),
]