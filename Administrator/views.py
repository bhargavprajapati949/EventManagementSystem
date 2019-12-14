from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import DetailView

from UserManager.models import College, Stream, Event_Committee
from EventWebSite.models import news, Event, Participants
from EventHead.models import Event_Head
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
                print('login success')
                return redirect('admin_dashboard')
            else:
                msg = "Email or Password is not valid"
                context = {'message' : msg, 'email' : email}
                return render(request, 'Administrator/admin_login.html', context)
        else:
            msg = ""
            context = {'message' : msg , "email" : ""}
            return render(request, 'Administrator/admin_login.html')

def admin_login_require(request):
    return render(request, 'Administrator/admin_login_require.html')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Administrator/admin_dashboard.html')
    else:
        return redirect('admin_login_require')

def participant_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        participant_list = Participants.objects.values('reg_no', 'reg_no__fname', 'reg_no__lname', 'reg_no__email', 'reg_no__contect_no', 'reg_no__clg_id__clg_name', 'reg_no__stream__stream_name', 'remark', 'total_payment', 'remaining_payment', 'paid_payment', 'filled_by__reg_no__committee_id', 'is_paid')
        context = {'participant_list' : participant_list}
        return render(request, 'Administrator/participant_manager.html', context)
    else:
        return redirect('admin_login_require')

def participant_detail(request, reg_no):
    if request.user.is_authenticated and request.user.is_admin:
        participant = Participants.objects.filter(reg_no = reg_no).values('reg_no', 'reg_no__fname', 'reg_no__lname', 'reg_no__email', 'reg_no__contect_no', 'reg_no__clg_id__clg_name', 'reg_no__stream__stream_name', 'remark', 'total_payment', 'remaining_payment', 'paid_payment', 'filled_by__reg_no__committee_id', 'is_paid')[0]
        context = {'participant' : participant, 'detail_form' : True}
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
                context = {'participant_user_form' : participant_user_form, 'registers_form' : registers_form, 'edit_form' : True , 'participant' : registration}
                return render(request, 'Administrator/participant_details.html', context)
        else:
            participant_user_form = participant_user_model_form(instance = participant_user)
            registers_form = registers_model_form(instance = registration)
            context = {'participant_user_form' : participant_user_form, 'registers_form' : registers_form, 'edit_form' : True , 'participant' : registration, 'reg_no':participant_user.reg_no}
            return render(request, 'Administrator/participant_details.html', context)
    else:
        return redirect('admin_login_require')

def volunteer_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        volunteerlist = Event.objects.all()
        context = {}
        return render(request, 'Administrator/volunteer_manager.html')
    else:
        return redirect('admin_login_require')


def volunteer_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            volunteer_form = volunteer_model_form(request.POST)
            if volunteer_form.is_valid():
                volunteer_form.save()
                return redirect('volunteer_manager')
            else:
                context = {'volunteeradd_form' : volunteer_form}
                return render(request, 'Administrator/volunteer_manager.html', context)
        else:
            pass
    else:
        return redirect('admin_login_require')
    

def event_head_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            addeventhead_form = event_head_model_form(request.POST)
            if addeventhead_form.is_valid():
                if not Event_Head.objects.filter(reg_no = request.POST['reg_no'], event = request.POST['event']):
                    eventhead = addeventhead_form.save()
                    committee_obj = Event_Committee.objects.get(reg_no = request.POST['reg_no'])
                    committee_obj.is_event_head = True
                    committee_obj.save()
                return redirect(event_head_manager)
            else:
                eventhead_list = Event_Head.objects.all().values('reg_no', 'event__event_name', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive', 'event__event_id')
                context = {'eventhead_list' : eventhead_list, 'addeventhead_form' : addeventhead_form}
                return render(request, 'Administrator/event_head_manager.html', context)
        else:
            eventhead_list = Event_Head.objects.all().values('reg_no', 'event__event_name', 'reg_no__reg_no__fname', 'reg_no__reg_no__lname', 'reg_no__reg_no__contect_no', 'reg_no__reg_no__email', 'isActive', 'event__event_id')
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

def coordinator_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Administrator/coordinator_manager.html')
    else:
        return redirect('admin_login_require')
    

def coordinator_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Administrator/coordinator_manager.html')
    else:
        return redirect('admin_login_require')
    

def event_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        eventlist = Event.objects.values('event_id', 'event_name', 'event_status')
        context = {'events' : eventlist}
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
    

# class event_info(DetailView):
#     model = Event
#     context_object_name = 'eventdetail'
#     pk_url_kwarg = 'event_id'
#     template_name = 'Administrator/event_manager.html'

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
    


# def event_edit(request, event_id):
#     print(event_id)
#     print('event_edit called')
#     if request.method == 'POST':
#         pass
#     else:
#         pass

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
            Event.objects.get(event_id = event_id).delete()
            return redirect('event_manager')
        else:
            event_obj = Event.objects.get(event_id = event_id)
            context = {'deleteevent_id' : event_id, 'eventdetail':  event_obj}
            return render(request, 'Administrator/event_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def collage_manager(request):
    if request.user.is_authenticated and request.user.is_admin:
        print('collage_manager called')
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
        print("news_edit called")
        if request.method == 'POST':
            print("post called")
            editcollage_form = collage_model_form(data = request.POST , instance = clg_obj)
            if editcollage_form.is_valid():
                print("valid data")
                editcollage_form.save()
                return redirect('collage_manager')
            else:
                print("invalid data")
                clg = College.objects.values('clg_id', 'clg_name')
                context = {'collages' : clg, 'editcollage_form' : editcollage_form, 'clg_id': clg_id}
                return render(request, 'Administrator/collage_manager.html', context)
        else:
            print("get called")
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
        print("stream_edit called")
        if request.method == 'POST':
            print("post called")
            editstream_form = stream_model_form(data = request.POST , instance = stream_obj)
            if editstream_form.is_valid():
                print("valid data")
                editstream_form.save()
                return redirect('stream_manager')
            else:
                print("invalid data")
                streamlist = Stream.objects.values('stream_id', 'stream_name')
                context = {'streams' : streamlist, 'editstream_form' : editstream_form, 'stream_id': stream_id}
                return render(request, 'Administrator/stream_manager.html', context)
        else:
            print("get called")
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
        newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
        context = {'news' : newslist }
        return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')

def news_add(request):
    if request.user.is_authenticated and request.user.is_admin:
        newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
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
        print("news_edit called")
        if request.method == 'POST':
            print("post called")
            editnews_form = news_model_form(data = request.POST , instance = n)
            if editnews_form.is_valid():
                print("valid data")
                editnews_form.save()
                return redirect('news_manager')
            else:
                print("invalid data")
                newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
                context = {'news' : newslist, 'editnews_form' : editnews_form, 'news_id': n.news_id}
                return render(request, 'Administrator/news_manager.html', context)
        else:
            print("get called")
            editnews_form = news_model_form(instance = n)
            newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
            context = {'news' : newslist, 'editnews_form' : editnews_form, 'news_id' : n.news_id}
            return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')

def news_delete(request, news_id):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            print('post method')
            news.objects.get(news_id = news_id).delete()
            return redirect('news_manager')
        else:
            print('get method')
            newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
            context = {'news' : newslist , 'news_id' : 0, 'delnews_id' : news_id}
            return render(request, 'Administrator/news_manager.html', context)
    else:
        return redirect('admin_login_require')
    

def collect_money(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'Administrator/collect_money.html')
    else:
        return redirect('admin_login_require')

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
    return redirect('admin_login')