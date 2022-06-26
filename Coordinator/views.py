import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import Coordinator

from EventWebSite.models import Participants, Participation
from EventHead.models import Winner
from Coordinator.models import Coordinator
from UserManager.models import User, Event_Committee


# Create your views here.

def redirectToCoordinator_login(request):
    return redirect('coordinator_login')

def coordinator_login(request):
    if request.user.is_authenticated:
        ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
        if ec and ec[0].is_coordinator:
            if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
                return redirect('coordinator_dashboard')
            else:
                msg = 'Your account is disabled by admin.'
                email = request.POST.get('email')
                context = {'message' : msg , "email" : email}
                return render(request, 'Coordinator/coordinator_login.html', context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        ec = Event_Committee.objects.filter(reg_no = user.reg_no)
        if user and ec and ec[0].is_coordinator:
            auth_login(request, user)
            return redirect('coordinator_dashboard')
        else:
            msg = "Email or Password is not valid"
            context = {'message' : msg, 'email' : email}
            return render(request, 'Coordinator/coordinator_login.html', context)
    else:
        msg = ""
        context = {'message' : msg , "email" : ""}
        return render(request, 'Coordinator/coordinator_login.html', context)

def coordinator_login_require(request):
    return render(request, 'Coordinator/coordinator_login_require.html')

def coordinator_dashboard(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            return render(request, 'Coordinator/coordinator_dashboard.html')
        else:
            return redirect('coordinator_login')
    elif request.user.is_authenticated and ec and ec[0].is_event_head:
        return redirect('eventHead_dashboard')
    elif request.user.is_authenticated and request.user.is_participant:
        return redirect('participant_dashboard')
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_dashboard')
    else:
        return redirect('coordinator_login_require')

def coordinator_confirm_participation(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            if request.method == 'POST':
                reg_no = request.POST['reg_no']
                for participation in Participation.objects.filter(reg_no = reg_no, reg_status = 'Paid'):
                    participation.reg_status = 'Confirm'
                    participation.save()
            
            participant_list = Participants.objects.values('reg_no', 'reg_no__fname', 'reg_no__lname', 'reg_no__email', 'reg_no__contect_no', 'reg_no__clg_id__clg_name', 'reg_no__stream__stream_name', 'remark', 'total_payment', 'remaining_payment', 'paid_payment', 'is_paid')
            events = {}
            is_confirmed = {}
            for participant in participant_list:
                events[participant['reg_no']] = Participation.objects.filter(reg_no = participant['reg_no']).values('event__event_name', 'reg_status')
                is_confirmed[participant['reg_no']] = True
                for participation in events[participant['reg_no']]:
                    if participation['reg_status'] == 'Paid':
                        is_confirmed[participant['reg_no']] = False
                    
            context = {'participant_list' : participant_list, 'event_list' : events, 'is_confirmed' : is_confirmed}
            return render(request, 'Coordinator/coordinator_confirm_participation.html', context)
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')

def coordinator_participation_certi_issue(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            participation_list = Participation.objects.filter(reg_status__in = ['Attended', 'Certificate Issued']).values('reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'event', 'event__event_name', 'reg_status')
            context = {'participation_list' : participation_list}
            return render(request, 'Coordinator/coordinator_participation_certi_issue.html', context)
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')
    
def issue_participation_certi(request, reg_no, event_id):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            issue_certificate = {'reg_no' : reg_no, 'event_id': event_id}
            if request.method == 'POST':
                certi_otp = request.POST['certi_otp']
                res = Participation.objects.filter(reg_no = reg_no, event_id = event_id, certi_otp =certi_otp)
                if res:
                    res[0].reg_status = 'Certificate Issued'
                    res[0].save()
                    return redirect('coordinator_participation_certi_issue')
                else:
                    issue_certificate['otp_msg'] = "Wrong OTP"

            participation_list = Participation.objects.filter(reg_status__in = ['Attended', 'Certificate Issued']).values('reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'event', 'event__event_name', 'reg_status')
            context = {'participation_list' : participation_list, 'issue_certificate' : issue_certificate}
            return render(request, 'Coordinator/coordinator_participation_certi_issue.html', context)   
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')

def coordinator_winner_certi_issue(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            winners = Winner.objects.all().values('winner__reg_no', 'winner__reg_no__reg_no__fname', 'winner__reg_no__reg_no__lname', 'winner__reg_no__reg_no__contect_no', 'winner__reg_no__reg_no__email', 'event', 'event__event_name', 'position', 'winner__reg_status')
            context = {'winners' : winners}
            return render(request, 'Coordinator/coordinator_winner_certi_issue.html', context)
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')
    

def issue_winner_certi(request, reg_no, event_id):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            issue_certificate = {'reg_no' : reg_no, 'event_id': event_id}
            if request.method == 'POST':
                winning_certi_otp = request.POST['winning_certi_otp']
                res = Winner.objects.filter(winner__reg_no = reg_no, event = event_id, winning_certi_otp = winning_certi_otp)
                if res:
                    participation = Participation.objects.filter(id = res[0].winner.id)[0]
                    participation.reg_status = 'Winner Certificate Issued'
                    participation.save()

                    res[0].winning_certificate_issue = True
                    res[0].save()
                    
                    return redirect('coordinator_winner_certi_issue')
                else:
                    issue_certificate['otp_msg'] = "Wrong OTP"

            winners = Winner.objects.all().values('winner__reg_no', 'winner__reg_no__reg_no__fname', 'winner__reg_no__reg_no__lname', 'winner__reg_no__reg_no__contect_no', 'winner__reg_no__reg_no__email', 'event', 'event__event_name', 'position', 'winner__reg_status')
            context = {'winners' : winners, 'issue_certificate' : issue_certificate}
            return render(request, 'Coordinator/coordinator_winner_certi_issue.html', context)
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')

def coordinator_profile(request):
    ec = Event_Committee.objects.filter(reg_no = request.user.reg_no)
    if request.user.is_authenticated and ec and ec[0].is_coordinator:
        if Coordinator.objects.filter(reg_no = request.user.reg_no, isActive = True):
            userinfo = User.objects.filter(reg_no = request.user.reg_no).values('reg_no', 'fname', 'lname', 'email', 'contect_no', 'clg_id__clg_name', 'stream__stream_name')[0]
            context = {'userinfo' : userinfo}
            return render(request, 'Coordinator/profile.html', context)
        else:
            return redirect('coordinator_login')
    else:
        return redirect('coordinator_login_require')

def coordinator_logout(request):
    auth_logout(request)
    return redirect('eventCommittee')