from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from EventWebSite.models import news, Event, Registers, Participation, Winner
from EventWebSite.form import ParticipantRegForm
from UserManager.models import User

import random

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

            selected_events = request.POST.getlist('select_event')

            total_payment = 0

            selected_event_obj = {}
            for event in selected_events:
                selected_event_obj[event] = Event.objects.get(event_name = event)
                total_payment = total_payment + selected_event_obj[event].fees

            reg = Registers(reg_no = usercheck[0])
            reg.total_payment = total_payment
            reg.remaining_payment = reg.total_payment
            reg.save()
            for event in selected_events:
                Participation.objects.create(
                    reg_no = reg,
                    event_id = selected_event_obj[event],
                    reg_status = 'Not Paid',
                    certi_otp = random.randrange(1000, 9999),
                    attendance_otp = random.randrange(1000, 9999)
                )
                
            return redirect('homepage')
        else:
            if regform.is_valid():
                user = regform.save()
                
                selected_events = request.POST.getlist('select_event')

                total_payment = 0
                selected_event_obj = {}
                for event in selected_events:
                    selected_event_obj[event] = Event.objects.get(event_name = event)
                    total_payment = total_payment + selected_event_obj[event].fees

                reg = Registers(reg_no = user)
                reg.total_payment = total_payment
                reg.remaining_payment = reg.total_payment
                reg.save()

                for event in selected_events:
                    Participation.objects.create(
                        reg_no = reg,
                        event_id = selected_event_obj[event],
                        reg_status = 'Not Paid',
                        certi_otp = random.randrange(1, 9999),
                        attendance_otp = random.randrange(1000, 9999)
                    )

                print('done')
                return redirect('homepage')
            else:
                events = Event.objects.values('event_name', 'fees')
                print('invalid')
                context = {'regform' : regform , 'events' : events}
                return render(request, 'EventWebSite/registration.html', context)
    else:
        regform = ParticipantRegForm()
        events = Event.objects.values('event_name', 'fees')
        context = {'regform' : regform, 'events' : events}
        return render(request, 'EventWebSite/registration.html', context)

def event_detail(request):
    events = Event.objects.values('event_name','event_detail', 'rules', 'event_logo', 'fees', 'event_status')
    context = {'events' : events}
    return render(request, 'EventWebSite/event_detail.html', context)

def participant_dashboard(request, reg_no):
    user_details_obj = Registers.objects.filter(reg_no=reg_no).values('reg_no','remark', 'total_payment', 'paid_payment')[0]
    events = Participation.objects.filter(reg_no = reg_no).values('reg_status', 'event_id__event_name', 'event_id__date_time', 'event_id__venue', 'attendance_otp', 'certi_otp' )
    context = {'userinfo' : user_details_obj, 'events' : events, 'status' : 'status'}
    winner = Winner.objects.filter(winner_reg_no = reg_no)
    if winner:
        winner.values('position', 'winning_certificate_issue', 'winning_certi_otp', 'event_head_id')
        context['winner'] = winner
    return render(request, 'EventWebSite/participant_dashboard.html', context)

def profile_participant(request, reg_no):
    userinfo = User.objects.filter(reg_no = reg_no).values('reg_no', 'fname', 'lname', 'email', 'contect_no', 'clg_id__clg_name', 'stream__stream_name')[0]
    context = {'userinfo' : userinfo}
    return render(request, 'EventWebSite/profile.html', context)

def participant_logout(request):
    auth_logout(request)
    return redirect('homepage')
