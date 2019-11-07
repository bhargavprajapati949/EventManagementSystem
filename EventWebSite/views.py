from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import news, Event, Parent_event

 # Create your views here.

def redirectToHomepage(request):
    return redirect('homepage')

def homepage(request):

    newsObject = news.objects.filter(for_whome='Participants')

    return render(request, 'FestOfficialWebSite/homepage.html', {'news' : newsObject})


def login(request):
    return render(request, 'FestOfficialWebSite/login.html')

def register(request):
    return render(request, 'FestOfficialWebSite/registration.html')

def event_detail(request):
    content = {}
    parent_events = Parent_event.objects.all()
    # content['parent_event'] = parant_events
    events = []
    for pevent in parent_events:
        event = Event.objects.filter(parent_event_id = pevent.parent_event_id)
        events += event

    content['events'] = events
    return render(request, 'FestOfficialWebSite/event_detail.html', content)