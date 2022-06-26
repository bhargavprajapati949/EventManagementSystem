from distutils import core
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import DetailView

from UserManager.models import College, Stream, Event_Committee
from EventWebSite.models import news, Event, Participants, Participation
from EventHead.models import Event_Head, Winner
from Administrator.models import Payments
from Administrator.forms import *
# Create your views here.

def redirectToAdmin_login(request):
    return redirect('admin_login')

def admin_login(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username = email, password = password)
            if user and user.is_admin:
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                msg = "Email or Password is not valid"
                context = {'message' : msg, 'email' : email}
                return render(request, 'Administrator/administrator_login.html', context)
        else:
            msg = ""
            context = {'message' : msg , "email" : ""}
            return render(request, 'Administrator/administrator_login.html')

def admin_login_require(request):
    return render(request, 'Administrator/administrator_login_require.html')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Administrator/administrator_dashboard.html')
    elif request.user.is_authenticated and request.user.is_participant:
        return render('participant_dashboard')
    elif request.user.is_authenticated:
        return redirect('coordinator_dashboard')
    else:
        return redirect('admin_login_require')

def participant_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        participant_list = Participants.objects.values('reg_no', 'reg_no__fname', 'reg_no__lname', 'reg_no__email', 'reg_no__contect_no', 'reg_no__clg_id__clg_name', 'reg_no__stream__stream_name', 'remark', 'total_payment', 'remaining_payment', 'paid_payment', 'is_paid')
        events = {}
        for participant in participant_list:
            events[participant['reg_no']] = Participation.objects.filter(reg_no = participant['reg_no']).values('event__event_name', 'reg_status')
        context = {'participant_list' : participant_list, 'event_list' : events}
        return render(request, 'Administrator/participant_manager.html', context)
    else:
        return redirect('admin_login_require')

def participant_detail(request, reg_no):
    if request.user.is_authenticated and request.user.is_admin:
        participant = Participants.objects.filter(reg_no = reg_no).values('reg_no', 'reg_no__fname', 'reg_no__lname', 'reg_no__email', 'reg_no__contect_no', 'reg_no__clg_id__clg_name', 'reg_no__stream__stream_name', 'remark', 'total_payment', 'remaining_payment', 'paid_payment', 'is_paid')[0]
        events = Participation.objects.filter(reg_no = reg_no).values('event__event_name', 'reg_status')
        context = {'participant' : participant, 'events': events, 'detail_form' : True}
        return render(request, 'Administrator/participant_details.html', context)
    else:
        return redirect('admin_login_require')

def participant_edit(request, reg_no):
    if request.user.is_authenticated and request.user.is_admin:
        participant_user = User.objects.get(reg_no = reg_no)
        registration = Participants.objects.get(reg_no = reg_no)
        if request.method == 'POST':
            participant_user_form = participant_user_model_form(data = request.POST, instance = participant_user)
            registers_form = registers_model_form(data = request.POST, instance = registration)
            if participant_user_form.is_valid() and registers_form.is_valid():
                participant_user_form.save()
                registers_form.save()
                return redirect('participant_manager')
            else:
                events = Participation.objects.filter(reg_no = reg_no).values('event__event_name', 'reg_status')
                context = {'participant_user_form' : participant_user_form, 'registers_form' : registers_form, 'edit_form' : True , 'participant' : registration, 'reg_no':participant_user.reg_no, 'events': events}
                return render(request, 'Administrator/participant_details.html', context)
        else:
            participant_user_form = participant_user_model_form(instance = participant_user)
            registers_form = registers_model_form(instance = registration)
            events = Participation.objects.filter(reg_no = reg_no).values('event__event_name', 'reg_status')
            context = {'participant_user_form' : participant_user_form, 'registers_form' : registers_form, 'edit_form' : True , 'participant' : registration, 'reg_no':participant_user.reg_no, 'events': events}
            return render(request, 'Administrator/participant_details.html', context)
    else:
        return redirect('admin_login_require')

def confirm_all_participation(request):
    if request.user.is_authenticated and request.user.is_admin:
        participation = Participation.objects.filter(reg_status = 'Paid')
        for item in participation:
            item.reg_status = 'Confirm'
            item.save()
        
        return redirect('participant_manager')
    else:
        return redirect('admin_login_require')
    
def event_head_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            addeventhead_form = event_head_model_form(request.POST)
            if addeventhead_form.is_valid():
                if not Event_Head.objects.filter(reg_no = request.POST['reg_no'], event = request.POST['event']):
                    addeventhead_form.save()
                    committee_obj = Event_Committee.objects.get(reg_no = request.POST['reg_no'])
                    committee_obj.is_event_head = True
                    committee_obj.save()
                return redirect(event_head_manager)
            else:
                eventhead_list = Event_Head.objects.all().values('reg_no', 'reg_no__committee_id', 'event__event_name', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive', 'event__event_id')
                context = {'eventhead_list' : eventhead_list, 'addeventhead_form' : addeventhead_form}
                return render(request, 'Administrator/event_head_manager.html', context)
        else:
            eventhead_list = Event_Head.objects.all().values('reg_no', 'reg_no__committee_id', 'event__event_name', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive', 'event__event_id')
            addeventhead_form = event_head_model_form()
            context = {'eventhead_list' : eventhead_list, 'addeventhead_form' : addeventhead_form}
            return render(request, 'Administrator/event_head_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def eventhead_active(request, reg_no, event):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            eh = Event_Head.objects.filter(reg_no = reg_no, event = event)
            for item in eh:
                item.isActive = True
                item.save()
            return redirect('event_head_manager')
    else:
        return redirect('admin_login_require')

def eventhead_disable(request, reg_no, event):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            eh = Event_Head.objects.filter(reg_no = reg_no, event = event)
            for item in eh:
                item.isActive = False
                item.save()
            return redirect('event_head_manager')
    else:
        return redirect('admin_login_require')

def coordinator_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            addCoordinator_form = coordinator_model_form(request.POST)
            if addCoordinator_form.is_valid():
                reg_no = request.POST['reg_no']
                if not Coordinator.objects.filter(reg_no = reg_no):
                    addCoordinator_form.save()
                    committee_obj = Event_Committee.objects.get(reg_no = request.POST['reg_no'])
                    committee_obj.is_coordinator = True
                    committee_obj.save()
                return redirect(coordinator_manager)
            else:
                coordinator_list = Coordinator.objects.all().values('reg_no', 'reg_no__committee_id', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive')
                context = {'coordinator_list': coordinator_list, 'addCoordinator_form': addCoordinator_form}
                return render(request, 'Administrator/coordinator_manager.html', context)
        else:
            coordinator_list = Coordinator.objects.all().values('reg_no', 'reg_no__committee_id', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive')
            addCoordinator_form = coordinator_model_form()
            context = {'coordinator_list': coordinator_list, 'addCoordinator_form': addCoordinator_form}
            return render(request, 'Administrator/coordinator_manager.html', context)
    else:
        return redirect('admin_login_require')
    
def coordinator_active(request, reg_no):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            coordinator = Coordinator.objects.get(reg_no = reg_no)
            coordinator.isActive = True
            coordinator.save()
            return redirect('coordinator_manager')
    else:
        return redirect('admin_login_require')

def coordinator_disable(request, reg_no):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            coordinator = Coordinator.objects.get(reg_no = reg_no)
            coordinator.isActive = False
            coordinator.save()
            return redirect('coordinator_manager')
    else:
        return redirect('admin_login_require')

def event_committee_list(request):
    if request.user.is_authenticated and request.user.is_admin:
        committee = Event_Committee.objects.values('reg_no', 'committee_id', 'reg_no__fname', 'reg_no__lname', 'reg_no__contect_no', 'reg_no__email', 'reg_no__clg__clg_name', 'reg_no__stream__stream_name', 'yearOfStudy', 'is_coordinator', 'is_event_head', 'in_sponsorship', 'in_publicity', 'in_criative', 'in_technical', 'in_volunteering', 'in_logistics', 'in_graphics', 'in_eventManagement')
        context = {'committee' : committee}
        return render(request, 'Administrator/event_committee_list.html', context)
    else:
        return redirect('admin_login_require')

def event_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        eventlist = Event.objects.values('event_id', 'event_name', 'event_status')
        event_heads = {}
        for event in eventlist:
            event_heads[event['event_id']] = Event_Head.objects.filter(event = event['event_id']).values('reg_no__committee_id', 'isActive')
        context = {'events' : eventlist, 'event_heads': event_heads}
        return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def event_info(request, event_id):
    if request.user.is_authenticated and request.user.is_admin:
        event_detail = Event.objects.get(event_id = event_id)
        context = {'eventdetail' : event_detail}
        return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    
def event_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            addevent_form = event_model_form(request.POST, request.FILES)
            if addevent_form.is_valid():
                addevent_form.save()
                return redirect('event_manager')
            else:
                context = {'addevent_form' : addevent_form}
                return render(request, 'Administrator/event_manager.html', context)
        else:
            addevent_form = event_model_form()
            context = {'addevent_form' : addevent_form}
            return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def event_edit(request, event_id):
    if request.user.is_authenticated and request.user.is_admin:
        event_obj = Event.objects.get(event_id = event_id)
        
        if request.method == 'POST':
            
            editevent_form = event_model_form(request.POST, request.FILES , instance = event_obj)
            if editevent_form.is_valid():
            
                editevent_form.save()
                return redirect('event_manager')
            else:
            
                context = {'editevent_form' : editevent_form, 'editevent_id' : event_id}
                return render(request, 'Administrator/event_manager.html', context)
        else:
            
            editevent_form = event_model_form(instance = event_obj, initial = {'event_logo': event_obj.event_logo} )
            context = {'editevent_form' : editevent_form, 'editevent_id' : event_id}
            return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def event_delete(request, event_id):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            event = Event.objects.get(event_id = event_id)
            event.delete()
            return redirect('event_manager')
        else:
            event_obj = Event.objects.get(event_id = event_id)
            context = {'deleteevent' : event_obj.event_name, 'deleteevent_id': event_id, 'eventdetail':  event_obj}
            return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    
def event_participation_list(request, event_id):
    if request.user.is_authenticated and request.user.is_admin:
        participation = Participation.objects.filter(event = event_id).values('reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_status')
        event_name = Event.objects.filter(event_id = event_id).values('event_name')[0]['event_name']
        context = {'participation' : participation, 'event_name': event_name}
        return render(request, 'Administrator/event_participation_list.html', context)
    else:
        return redirect('admin_login_require')

def event_winners_list(request, event_id):
    if request.user.is_authenticated and request.user.is_admin:
        winners = Winner.objects.filter(event = event_id).values('winner__reg_no', 'winner__reg_no__reg_no__fname', 'winner__reg_no__reg_no__lname', 'position', 'winning_certificate_issue', 'event_head__reg_no__committee_id')
        event_name = Event.objects.filter(event_id = event_id).values('event_name')[0]['event_name']
        context = {'winners' : winners, 'event_name': event_name}
        return render(request, 'Administrator/event_winners_list.html', context)
    else:
        return redirect('admin_login_require')

def payments_list(request):
    if request.user.is_authenticated and request.user.is_admin:
        payments = Payments.objects.values('payment_id', 'reg_no', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'amount', 'date_time')
        context = {'payments' : payments}
        return render(request, 'Administrator/payments_list.html', context)
    else:
        return redirect('admin_login_require')

def collage_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        clg = College.objects.values('clg_id', 'clg_name')
        context = {'collages' : clg}
        return render(request, 'Administrator/collage_manager.html', context)
    else:
        return redirect('admin_login_require')

def collage_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        clg = College.objects.values('clg_id', 'clg_name')
        if request.method == 'POST':
            addcollage_form = collage_model_form(data = request.POST)
            if addcollage_form.is_valid():
                addcollage_form.save()
                return redirect('collage_manager')
            else:
                context = {'collages':clg, 'addcollage_form':addcollage_form, 'clg_id' : 'None'}
                return render(request, 'Administrator/collage_manage.html', context)
        else:
            addcollage_form = collage_model_form()
            context = {'collages' : clg , 'addcollage_form': addcollage_form, 'clg_id' : 'None'}
            return render(request, 'Administrator/collage_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def collage_edit(request, clg_id):
    if request.user.is_authenticated and request.user.is_admin:
        clg_obj = College.objects.get(clg_id = clg_id)
        if request.method == 'POST':
            editcollage_form = collage_model_form(data = request.POST , instance = clg_obj)
            if editcollage_form.is_valid():
                editcollage_form.save()
                return redirect('collage_manager')
            else:
                clg = College.objects.values('clg_id', 'clg_name')
                context = {'collages' : clg, 'editcollage_form' : editcollage_form, 'clg_id': clg_id}
                return render(request, 'Administrator/collage_manager.html', context)
        else:
            editcollage_form = collage_model_form(instance = clg_obj)
            clg = College.objects.values('clg_id', 'clg_name')
            context = {'collages' : clg, 'editcollage_form' : editcollage_form, 'clg_id': clg_id}
            return render(request, 'Administrator/collage_manager.html', context)
    else:
        return redirect('admin_login_require')

def collage_delete(request, clg_id):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            College.objects.get(clg_id = clg_id).delete()
            return redirect('collage_manager')
        else:
            clg = College.objects.values('clg_id', 'clg_name')
            context = {'collages' : clg, 'clg_id': 'None', 'deletecollage_id' : clg_id }
            return render(request, 'Administrator/collage_manager.html', context)
    else:
        return redirect('admin_login_require')


def stream_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        streamlist = Stream.objects.values('stream_id', 'stream_name')
        context = {'streams' : streamlist}
        return render(request, 'Administrator/stream_manager.html', context)
    else:
        return redirect('admin_login_require')

def stream_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        streamlist = Stream.objects.values('stream_id', 'stream_name')
        if request.method == 'POST':
            addstream_form = stream_model_form(data = request.POST)
            if addstream_form.is_valid():
                addstream_form.save()
                return redirect('stream_manager')
            else:
                context = {'streams': streamlist, 'addstream_form':addstream_form, 'stream_id' : 'None'}
                return render(request, 'Administrator/stream_manage.html', context)
        else:
            addstream_form = stream_model_form()
            context = {'streams' : streamlist , 'addstream_form': addstream_form, 'stream_id' : 'None'}
            return render(request, 'Administrator/stream_manager.html', context)
    else:
        return redirect('admin_login_require')

def stream_edit(request, stream_id):
    if request.user.is_authenticated and request.user.is_admin:
        stream_obj = Stream.objects.get(stream_id = stream_id)
        if request.method == 'POST':
            editstream_form = stream_model_form(data = request.POST , instance = stream_obj)
            if editstream_form.is_valid():
                editstream_form.save()
                return redirect('stream_manager')
            else:                
                streamlist = Stream.objects.values('stream_id', 'stream_name')
                context = {'streams' : streamlist, 'editstream_form' : editstream_form, 'stream_id': stream_id}
                return render(request, 'Administrator/stream_manager.html', context)
        else:
            editstream_form = stream_model_form(instance = stream_obj)
            streamlist = Stream.objects.values('stream_id', 'stream_name')
            context = {'streams' : streamlist, 'editstream_form' : editstream_form, 'stream_id': stream_id}
            return render(request, 'Administrator/stream_manager.html', context)
    else:
        return redirect('admin_login_require')


def stream_delete(request, stream_id):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            Stream.objects.get(stream_id = stream_id).delete()
            return redirect('stream_manager')
        else:
            streamlist = Stream.objects.values('stream_id', 'stream_name')
            context = {'streams' : streamlist, 'stream_id': 'None', 'deletestream_id' : stream_id }
            return render(request, 'Administrator/stream_manager.html', context)
    else:
        return redirect('admin_login_require')

def news_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        newslist = news.objects.values('news_id', 'news_content', 'hyperlink')
        context = {'news' : newslist }
        return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')

def news_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        newslist = news.objects.values('news_id', 'news_content', 'hyperlink')
        context = {'news' : newslist }
        context['news_id'] = 0
        if request.method == 'POST':
            addnews_form = news_model_form(data = request.POST)
            if addnews_form.is_valid():
                addnews_form.save()
                return redirect('news_manager')
            else:
                context['addnews_form'] = addnews_form
                return render(request, 'Administrator/news_manager.html', context)
        else:
            addnews_form = news_model_form()
            context['addnews_form'] = addnews_form
            return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def news_edit(request, news_id):
    if request.user.is_authenticated and request.user.is_admin:
        n = news.objects.get(news_id = news_id)
        if request.method == 'POST':
            editnews_form = news_model_form(data = request.POST , instance = n)
            if editnews_form.is_valid():
                editnews_form.save()
                return redirect('news_manager')
            else:
                newslist = news.objects.values('news_id', 'news_content', 'hyperlink')
                context = {'news' : newslist, 'editnews_form' : editnews_form, 'news_id': n.news_id}
                return render(request, 'Administrator/news_manager.html', context)
        else:
            editnews_form = news_model_form(instance = n)
            newslist = news.objects.values('news_id', 'news_content', 'hyperlink')
            context = {'news' : newslist, 'editnews_form' : editnews_form, 'news_id' : n.news_id}
            return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')

def news_delete(request, news_id):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            news.objects.get(news_id = news_id).delete()
            return redirect('news_manager')
        else:            
            newslist = news.objects.values('news_id', 'news_content', 'hyperlink')
            context = {'news' : newslist , 'news_id' : 0, 'delnews_id' : news_id}
            return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')
    

# def collect_money(request):
#     if request.user.is_authenticated and request.user.is_admin:
#         return render(request, 'Administrator/collect_money.html')
#     else:
#         return redirect('admin_login_require')

def profile_administrator(request):
    reg_no = request.user.reg_no
    if request.user.is_authenticated and request.user.is_admin:
        userinfo = User.objects.filter(reg_no = reg_no).values('reg_no', 'fname', 'lname', 'email', 'contect_no', 'clg_id__clg_name', 'stream__stream_name')[0]
        committeeinfo = Event_Committee.objects.filter(reg_no = reg_no).values('committee_id', 'yearOfStudy')
        context = {'userinfo' : userinfo, 'committeeinfo' : committeeinfo}
        return render(request, 'Administrator/profile.html', context)
    else:
        return redirect('admin_login_require')

def admin_logout(request):
    auth_logout(request)
    return redirect('eventCommittee')