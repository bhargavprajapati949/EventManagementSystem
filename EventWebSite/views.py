from django.shortcuts import render, redirect
from django.http import HttpResponse
from EventWebSite.models import news, Event, Parent_event 
from EventWebSite.form import ParticipantRegForm

 # Create your views here.

def redirectToHomepage(request):
    return redirect('homepage')

def homepage(request):

    newsObject = news.objects.filter(for_whome='Participants')

    return render(request, 'FestOfficialWebSite/homepage.html', {'news' : newsObject})


def login(request):
    return render(request, 'FestOfficialWebSite/login.html')

# def register(request):
#     form = UserCreationForm
#     return render(request, 'FestOfficialWebSite/registration.html')

def register(request):
    if request.method == 'POST':
        regform = ParticipantRegForm(data=request.POST)
        if regform.is_valid():
            user = regform.save()
            print('done')
            return redirect('homepage')
        else:
            return redirect('register')
    else:
        regform = ParticipantRegForm()
        context = {'regform' : regform}
        return render(request, 'FestOfficialWebSite/registration.html', context)

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