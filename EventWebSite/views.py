from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from Administrator.models import Payments
from EventWebSite.models import news, Event, Participants, Participation
from EventHead.models import Winner
from UserManager.models import User

from EventWebSite.form import ParticipantRegForm

import random
from django.db.models import Q

# Create your views here.

def redirectToHomepage(request):
    return HttpResponseRedirect('homepage')

def homepage(request):
    newsObject = news.objects.filter()
    return render(request, 'EventWebSite/homepage.html', {'news' : newsObject})

def participant_login(request):
    if request.user.is_authenticated and request.user.is_participant:
        return redirect('participant_dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('usernamefield')
            password = request.POST.get('passwordfield')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_participant:
                    auth_login(request, user)
                    return redirect('participant_dashboard')
                else:
                    msg = 'You are not registered. First Register yourself.'
                    context = {'message' : msg}
                    return render(request, 'EventWebSite/login.html', context)
            else:
                msg = "Email or Password is not valid"
                context = {'message' : msg}
                return render(request, 'EventWebSite/login.html', context)
        else:
            return render(request, 'EventWebSite/login.html')

def participant_login_require(request):
    return render(request, 'EventWebSite/participant_login_require.html')

def register(request):
    if request.method == 'POST':
        regform = ParticipantRegForm(data=request.POST)
        usercheck = User.objects.filter(email = request.POST.get('email'))
        if usercheck and len(usercheck) == 1:
            username = request.POST.get('email')
            password = request.POST.get('password1')
            user = authenticate(username=username, password=password)
            
            if user:
                # If user reregister for more events
                # TODO make sure to mark status as not paid 
                # reg = Participants(reg_no = usercheck[0])
                reg = Participants.objects.filter(reg_no = usercheck[0])[0]

                new_events = request.POST.getlist('select_event')
                old_events_q = Participation.objects.filter(reg_no = reg).values_list('event__event_name')

                old_events = []
                for event in old_events_q:
                    old_events.append(event[0])

                total_payment = 0

                selected_event_obj = {}

                for event in new_events:
                    if event not in old_events:
                        selected_event_obj[event] = Event.objects.get(event_name = event)
                        total_payment = total_payment + selected_event_obj[event].fees
                

                reg.total_payment +=  total_payment
                reg.remaining_payment += total_payment
                reg.save()

                for event in selected_event_obj:
                    Participation.objects.create(
                        reg_no = reg,
                        event = event,
                        reg_status = 'Not Paid',
                        certi_otp = random.randrange(1000, 9999),
                        attendance_otp = random.randrange(1000, 9999)
                    )
                auth_login(request, user)
                return redirect('participant_dashboard')
                # return redirect('participant_login')
            else:
                msg = "Password is not valid"
                events = Event.objects.values('event_name', 'fees')
                context = {'messages' : [msg], 'regform' : regform , 'events' : events}
                return render(request, 'EventWebSite/registration.html', context)
        else:
            if regform.is_valid():
                user = regform.save()
                
                selected_events = request.POST.getlist('select_event')

                total_payment = 0
                selected_event_obj = {}
                for event in selected_events:
                    selected_event_obj[event] = Event.objects.get(event_name = event)
                    total_payment = total_payment + selected_event_obj[event].fees

                reg = Participants(reg_no = user)
                reg.total_payment = total_payment
                reg.remaining_payment = reg.total_payment
                reg.save()

                for event in selected_events:
                    Participation.objects.create(
                        reg_no = reg,
                        event = selected_event_obj[event],
                        reg_status = 'Not Paid',
                        certi_otp = random.randrange(1, 9999),
                        attendance_otp = random.randrange(1000, 9999)
                    )
                auth_login(request, user)
                return redirect('participant_dashboard')
            else:
                events = Event.objects.values('event_name', 'fees')
                context = {'regform' : regform , 'events' : events}
                return render(request, 'EventWebSite/registration.html', context)
    else:
        regform = ParticipantRegForm()
        events = Event.objects.values('event_name', 'fees')
        context = {'regform' : regform, 'events' : events}
        return render(request, 'EventWebSite/registration.html', context)

def event_detail(request):
    query = request.GET.get('q')
    if query is not None:
        # events = Event.objects.filter(event_name=query).values('event_name','event_detail', 'rules', 'event_logo', 'fees', 'event_status')
        # events = Event.objects.filter(Q('event_name=query'))
        event_list = Event.objects.filter(event_name__icontains=query)
    else:    
        # events = Event.objects.values('event_name','event_detail', 'rules', 'event_logo', 'fees', 'event_status')
        event_list = Event.objects.all()

    context = {'event_list' : event_list}
    return render(request, 'EventWebSite/event_detail.html', context)


def participant_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_participant:
            reg_no = request.user.reg_no
            userinfo = Participants.objects.filter(reg_no=reg_no).values('reg_no','remark', 'total_payment', 'paid_payment', 'is_paid')[0]
            events = Participation.objects.filter(reg_no = reg_no).values('event_id', 'reg_status', 'event_id__event_name', 'event_id__date_time', 'event_id__venue', 'attendance_otp', 'certi_otp' )
            context = {'userinfo' : userinfo, 'events' : events}
            winners = Winner.objects.filter(winner__reg_no = reg_no).values('event', 'position', 'winning_certi_otp')

            if winners:            
                winnerVal = {}
                for winner in winners:
                    winnerVal[winner['event']] = winner
                context['winner'] = winnerVal

            return render(request, 'EventWebSite/participant_dashboard.html', context)
        elif request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('coordinator_dashboard')
    else:
        return redirect('participant_login_require')

def do_payment(request):
    if request.user.is_authenticated and request.user.is_participant:
        # Participants Table
        user = Participants.objects.get(reg_no = request.user)
        user.remaining_payment = 0
        user.paid_payment = user.total_payment
        user.is_paid = True
        user.save()

        # Participation Table
        events = Participation.objects.filter(reg_no = user)
        for event in events:
            event.reg_status = 'Paid'
            event.save()
        
        # Payments Table
        payment = Payments.objects.create(
            reg_no = user, 
            amount = user.total_payment,
        )

        return redirect('participant_dashboard')
    else:
        return redirect('participant_login_require')

def profile_participant(request):
    if request.user.is_authenticated and request.user.is_participant:
        userinfo = User.objects.filter(reg_no = request.user.reg_no).values('reg_no', 'fname', 'lname', 'email', 'contect_no', 'clg_id__clg_name', 'stream__stream_name')[0]
        context = {'userinfo' : userinfo}
        return render(request, 'EventWebSite/profile.html', context)
    else:
        return redirect('participant_login_require')

def participant_logout(request):
    auth_logout(request)
    return redirect('homepage')
