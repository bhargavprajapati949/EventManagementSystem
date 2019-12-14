from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from UserManager.models import Event_Committee
from EventWebSite.models import Participation, Event
from EventHead.models import Event_Head, Winner
from EventHead.forms import *

import random

# Create your views here.

def redirectToEventHead_login(request):
    return redirect('eventHead_login')

def eventHead_login(request):
    if request.user.is_authenticated:
        ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
        if ec and ec[0].is_event_head:
            return redirect('eventHead_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        ec = Event_Committee.objects.filter(reg_no = user.reg_no)
        if user and ec and ec[0].is_event_head:
            auth_login(request, user)
            print('login success')
            return redirect('eventHead_dashboard')
        else:
            msg = "Email or Password is not valid"
            print(msg)
            context = {'message' : msg, 'email' : email}
            return render(request, 'EventHead/eventHead_login.html', context)
    else:
        msg = ""
        context = {'message' : msg , "email" : ""}
        return render(request, 'EventHead/eventHead_login.html',context)

def eventHead_login_require(request):
    return render(request, 'EventHead/eventHead_login_require.html')

def eventHead_dashboard(request):
    if request.user.is_authenticated:
        events = Event_Head.objects.filter(reg_no = request.user.reg_no).values('event__event_name', 'event__event_id')
        context = {'events' : events}
        return render(request, 'EventHead/eventHead_dashboard.html', context)
    else:
        return redirect('eventHead_login_require')

def attendance(request, event_id):
    if request.user.is_authenticated:
        if Event_Head.objects.filter(reg_no = request.user.reg_no, event_id = event_id):
            if request.method == 'POST':
                reg_no = request.POST['participant']
                p = Participation.objects.filter(reg_no = reg_no, event_id = event_id)[0]
                p.reg_status = 'Attended'
                p.save()
            
            participants = Participation.objects.filter(event_id = event_id, reg_status = 'Comform').values('reg_no')
            context = {'participants' : participants}
            return render(request, 'EventHead/attendance.html', context)
        else:
            context = {'message' : 'You do not have permissions to take attendance in this event.'}
            return redirect('eventHead_dashboard', context)
    else:
        return redirect('eventHead_login_require')

def participation_info(request, event_id):
    if request.user.is_authenticated:
        participation_data = Participation.objects.filter()
        print('pass')
    else:
        return redirect('eventHead_login_require')

def enter_result(request, event_id):
    if request.user.is_authenticated:
        if Event_Head.objects.filter(reg_no = request.user.reg_no, event_id = event_id):
            if request.method == 'POST':
                first = request.POST['firstPosition']
                second = request.POST['secondPosition']
                third = request.POST['thirdPostion']
                if not (first == second or first == third or second == third):
                    first_obj = Participation.objects.filter(reg_no = first, event_id = event_id)[0]
                    first_obj.reg_status = 'Attended Winner'
                    first_obj.save()

                    second_obj = Participation.objects.filter(reg_no = second, event_id = event_id)[0]
                    second_obj.reg_status = 'Attended Winner'
                    second_obj.save()

                    third_obj = Participation.objects.filter(reg_no = third, event_id = event_id)[0]
                    third_obj.reg_status = 'Attended Winner'
                    third_obj.save()

                    event = Event.objects.get(event_id = event_id)
                    
                    Winner.objects.create(
                        event_id = event,
                        position = '1',
                        winner_reg_no = Participation.objects.get(reg_no = first),
                        winning_certi_otp = random.randrange(1000, 9999),
                        event_head_id = Event_Head.objects.get(reg_no = request.user.reg_no)
                    )

                    Winner.objects.create(
                        event_id = event,
                        position = '2',
                        winner_reg_no = Participation.objects.get(reg_no = second),
                        winning_certi_otp = random.randrange(1000, 9999),
                        event_head_id = Event_Head.objects.get(reg_no = request.user.reg_no)
                    )

                    Winner.objects.create(
                        event_id = event,
                        position = '3',
                        winner_reg_no = Participation.objects.get(reg_no = third),
                        winning_certi_otp = random.randrange(1000, 9999),
                        event_head_id = Event_Head.objects.get(reg_no = request.user.reg_no)
                    )

                    return redirect('eventHead_dashboard')
                else:
                    participants = Participation.objects.filter(event_id = event_id, reg_status = 'Attended').values('reg_no')
                    context = {'participants' : participants, 'first' : first, 'second' : second, 'third' : third }
                    return render(request, 'EventHead/eventHead_enter_result.html', context)
            else:
                participants = Participation.objects.filter(event_id = event_id, reg_status = 'Attended').values('reg_no')
                context = {'participants' : participants}
                return render(request, 'EventHead/eventHead_enter_result.html', context)
        else:
            context = {'message' : 'You do not have permissions to take attendance in this event.'}
            return redirect('eventHead_dashboard', context)
    else:
        return redirect('eventHead_login_require')
        

def event_head_profile(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('eventHead_login')

def eventHead_logout(request):
    auth_logout(request)
    return redirect('eventHead_login')