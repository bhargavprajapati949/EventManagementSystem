from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from UserManager.models import User, Event_Committee
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
            return redirect('eventHead_dashboard')
        else:
            msg = "Email or Password is not valid"
            context = {'message' : msg, 'email' : email}
            return render(request, 'EventHead/eventHead_login.html', context)
    else:
        msg = ""
        context = {'message' : msg , "email" : ""}
        return render(request, 'EventHead/eventHead_login.html',context)

def eventHead_login_require(request):
    return render(request, 'EventHead/eventHead_login_require.html')

def eventHead_dashboard(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_event_head:
        events = Event_Head.objects.filter(reg_no = request.user.reg_no, isActive = True).values('event__event_name', 'event__event_id')
        context = {'events' : events}
        return render(request, 'EventHead/eventHead_dashboard.html', context)
    elif request.user.is_authenticated and ec and ec[0].is_coordinator:
        return redirect('coordinator_dashboard')
    elif request.user.is_authenticated and request.user.is_participant:
        return redirect('participant_dashboard')
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_dashboard')
    else:
        return redirect('eventHead_login_require')

def attendance(request, event_id):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_event_head:
        if Event_Head.objects.filter(reg_no = request.user.reg_no, event_id = event_id, isActive = True):
            participants = Participation.objects.filter(event = event_id, reg_status__in = ['Confirm', 'Attended', 'Attended Winner', 'Certificate Issued', 'Winner Certificate Issued']).values('reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__clg__clg_name', 'reg_no__reg_no__stream__stream_name', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'reg_status')
            event = Event.objects.filter(event_id = event_id).values('event_id', 'event_name')[0]
            context = {'event': event ,'participants' : participants}
            return render(request, 'EventHead/attendance.html', context)
        else:
            # event = Event.objects.filter(event_id = event_id)
            # if event:
            #     event = event.values('event_name')['event_name']
            #     msg = 'Your account is disabled as event head for ' + event + ' event'
            # else:
            #     msg = 'Event Dose not exists'
            
            # messages = [msg]
            # context = {'messages' : messages}
            return redirect('eventHead_dashboard')
    else:
        return redirect('eventHead_login_require')

def mark_attendance(request, reg_no, event_id):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_event_head:
        if Event_Head.objects.filter(reg_no = request.user.reg_no, event_id = event_id, isActive = True):
            mark_attendance = {'reg_no' : reg_no}
            if request.method == 'POST':
                otp = request.POST['attendance_otp']
                res = Participation.objects.filter(reg_no = reg_no, event_id = event_id, attendance_otp = otp)
                if res:
                    res[0].reg_status = 'Attended'
                    res[0].save()
                    return redirect('attendance', event_id)
                else:
                    mark_attendance['otp_msg'] = "Wrong OTP"
            
            participants = Participation.objects.filter(event = event_id, reg_status__in = ['Confirm', 'Attended', 'Attended Winner', 'Certificate Issued', 'Winner Certificate Issued']).values('reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__clg__clg_name', 'reg_no__reg_no__stream__stream_name', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'reg_status')
            event = Event.objects.filter(event_id = event_id).values('event_id', 'event_name')[0]
            context = {'event': event ,'participants' : participants, 'mark_attendance': mark_attendance}
            return render(request, 'EventHead/attendance.html', context)
        else:
            return redirect('eventHead_dashboard')
    else:
        return redirect('eventHead_login_require')
    
def winner_entry(request, event_id):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_event_head:
        if Event_Head.objects.filter(reg_no = request.user.reg_no, event_id = event_id):
            winner_messages = []
            if request.method == 'POST':
                position = request.POST['position']
                reg_no = request.POST['reg_no']

                if Winner.objects.filter(event_id = event_id, winner__reg_no = reg_no):
                    winner_messages.append("Participant is already declared winner in this event")
                if len(Winner.objects.filter(event_id = event_id, position = position)) >= 2:
                    winner_messages.append("Maximum two participants can share same position in single event")
                
                
                if len(winner_messages) == 0:
                    participation = Participation.objects.get(reg_no = reg_no, event = event_id)
                    Winner.objects.create(
                        event = Event.objects.get(event_id = event_id),
                        winner = participation,
                        position = position,
                        winning_certi_otp = random.randrange(1000, 9999),
                        event_head = Event_Head.objects.get(reg_no = request.user.reg_no, event = event_id)
                    )
                    participation.reg_status = "Attended Winner"
                    participation.save()

            winners = Winner.objects.filter(event_id = event_id).values('winner__reg_no', 'winner__reg_no__reg_no__fname', 'winner__reg_no__reg_no__lname', 'winner__reg_no__reg_no__contect_no','winner__reg_no__reg_no__email', 'position', 'winning_certificate_issue')
            winners_participants = Winner.objects.filter(event_id = event_id).values_list('winner__reg_no')
            participants = Participation.objects.filter(event_id = event_id, reg_status = 'Attended').exclude(reg_no__in = winners_participants).values('reg_no')
            context = {'participants' : participants, 'winners': winners, 'winner_messages': winner_messages}
            return render(request, 'EventHead/winner_entry.html', context)
        else:
            return redirect('eventHead_dashboard', context)
    else:
        return redirect('eventHead_login_require')

def event_head_profile(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_event_head:
        userinfo = User.objects.filter(reg_no = request.user.reg_no).values('reg_no', 'fname', 'lname', 'email', 'contect_no', 'clg_id__clg_name', 'stream__stream_name')[0]
        context = {'userinfo' : userinfo}
        return render(request, 'EventHead/profile.html', context)
    else:
        return redirect('eventHead_login_require')

def eventHead_logout(request):
    auth_logout(request)
    return redirect('eventCommittee')