from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from EventWebSite.models import news, Event
from EventWebSite.form import ParticipantRegForm
from UserManager.models import User, Participant

 # Create your views here.

def redirectToHomepage(request):
    return HttpResponseRedirect('homepage')

def homepage(request):

    newsObject = news.objects.filter(for_whome='Participants')

    return render(request, 'EventWebSite/homepage.html', {'news' : newsObject})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('usernamefield')
        password = request.POST.get('passwordfield')
        print('username = ', username)
        print('password = ', password)
        user = authenticate(username=username, password=password)
        print('user object = ', user)
        if user:
            if user.is_participant:
                auth_login(request, user)
                print('login success')
                return redirect('homepage')
            else:
                print('is_participant = false')
                return HttpResponse('You are not registered. First Register yourself.')
        else:
            return HttpResponse('Invalid login details')
            print('invalid details')
    else:
        print('get method')
        return render(request, 'EventWebSite/login.html')


def register(request):
    if request.method == 'POST':
        regform = ParticipantRegForm(data=request.POST)
        usercheck = User.objects.filter(email = request.POST.get('email'))
        if usercheck and len(usercheck) == 1:
            Participant.objects.create(reg_no = usercheck[0])
            return redirect('homepage')
        else:
            if regform.is_valid():
                user = regform.save()
                print('done')
                return redirect('homepage')
            else:
                print('invalid')
                context = {'regform' : regform }
                return render(request, 'EventWebSite/registration.html', context)
    else:
        regform = ParticipantRegForm()
        context = {'regform' : regform}
        return render(request, 'EventWebSite/registration.html', context)

def event_detail(request):
    return render(request, 'EventWebSite/event_detail.html')