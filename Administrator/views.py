from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.generic import DetailView
from UserManager.models import Collages, Stream
from EventWebSite.models import news, Event
from Administrator.forms import *
# Create your views here.

def redirectToAdmin_login(request):
    return redirect('admin_login')

def admin_login(request):
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
            print(msg)
            context = {'message' : msg, 'email' : email}
            return render(request, 'Administrator/admin_login.html', context)
    else:
        msg = ""
        context = {'message' : msg , "email" : ""}
        return render(request, 'Administrator/admin_login.html')

def admin_dashboard(request):
    return render(request, 'Administrator/admin_dashboard.html')

def participant_manager(request):
    return render(request, 'Administrator/participant_manager.html')

def volunteer_manager(request):
    volunteerlist = Event.objects.all()
    context = {}
    return render(request, 'Administrator/volunteer_manager.html')

def volunteer_add(request):
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

def event_head_manager(request):
    return render(request, 'Administrator/event_head_manager.html')

def event_head_add(request):
    return render(request, 'Administrator/event_head_manager.html')

def coordinator_add(request):
    return render(request, 'Administrator/coordinator_manager.html')

def coordinator_manager(request):
    return render(request, 'Administrator/coordinator_manager.html')

def event_manager(request):
    eventlist = Event.objects.values('event_id', 'event_name', 'event_status')
    context = {'events' : eventlist}
    return render(request, 'Administrator/event_manager.html', context)

def event_info(request, event_id):
    event_detail = Event.objects.get(event_id = event_id)
    context = {'eventdetail' : event_detail}
    return render(request, 'Administrator/event_manager.html', context)

# class event_info(DetailView):
#     model = Event
#     context_object_name = 'eventdetail'
#     pk_url_kwarg = 'event_id'
#     template_name = 'Administrator/event_manager.html'

def event_add(request):
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


# def event_edit(request, event_id):
#     print(event_id)
#     print('event_edit called')
#     if request.method == 'POST':
#         pass
#     else:
#         pass

def event_edit(request, event_id):
    event_obj = Event.objects.get(event_id = event_id)
    print("news_edit called")
    if request.method == 'POST':
        print("post called")
        editevent_form = event_model_form(request.POST, request.FILES , instance = event_obj)
        if editevent_form.is_valid():
            print("valid data")
            editevent_form.save()
            return redirect('event_manager')
        else:
            print("invalid data")            
            context = {'editevent_form' : editevent_form, 'editevent_id' : event_id}
            return render(request, 'Administrator/event_manager.html', context)
    else:
        print("get called")
        editevent_form = event_model_form(instance = event_obj, initial = {'event_logo': event_obj.event_logo} )
        context = {'editevent_form' : editevent_form, 'editevent_id' : event_id}
        return render(request, 'Administrator/event_manager.html', context)


def event_delete(request, event_id):
    print(event_id, 'event_delete called')
    if request.method == 'POST':
        Event.objects.get(event_id = event_id).delete()
        return redirect('event_manager')
    else:
        event_obj = Event.objects.get(event_id = event_id)
        context = {'deleteevent_id' : event_id, 'eventdetail':  event_obj}
        return render(request, 'Administrator/event_manager.html', context)

def collage_manager(request):
    print('collage_manager called')
    clg = Collages.objects.values('clg_id', 'clg_name')
    context = {'collages' : clg}
    return render(request, 'Administrator/collage_manager.html', context)

def collage_add(request):
    print('collage_add called')
    clg = Collages.objects.values('clg_id', 'clg_name')
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

def collage_edit(request, clg_id):
    clg_obj = Collages.objects.get(clg_id = clg_id)
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
            clg = Collages.objects.values('clg_id', 'clg_name')
            context = {'collages' : clg, 'editcollage_form' : editcollage_form, 'clg_id': clg_id}
            return render(request, 'Administrator/collage_manager.html', context)
    else:
        print("get called")
        editcollage_form = collage_model_form(instance = clg_obj)
        clg = Collages.objects.values('clg_id', 'clg_name')
        context = {'collages' : clg, 'editcollage_form' : editcollage_form, 'clg_id': clg_id}
        return render(request, 'Administrator/collage_manager.html', context)

def collage_delete(request, clg_id):
    print('collage_delete called')
    if request.method == 'POST':
        Collages.objects.get(clg_id = clg_id).delete()
        return redirect('collage_manager')
    else:
        clg = Collages.objects.values('clg_id', 'clg_name')
        context = {'collages' : clg, 'clg_id': 'None', 'deletecollage_id' : clg_id }
        return render(request, 'Administrator/collage_manager.html', context)


def stream_manager(request):
    streamlist = Stream.objects.values('stream_id', 'stream_name')
    context = {'streams' : streamlist}
    return render(request, 'Administrator/stream_manager.html', context)

def stream_add(request):
    print('stream_add called')
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

def stream_edit(request, stream_id):
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


def stream_delete(request, stream_id):
    print('stream_delete called')
    if request.method == 'POST':
        Stream.objects.get(stream_id = stream_id).delete()
        return redirect('stream_manager')
    else:
        streamlist = Stream.objects.values('stream_id', 'stream_name')
        context = {'streams' : streamlist, 'stream_id': 'None', 'deletestream_id' : stream_id }
        return render(request, 'Administrator/stream_manager.html', context)

def news_manager(request):
    newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
    context = {'news' : newslist }
    return render(request, 'Administrator/news_manager.html', context)

def news_add(request):
    print('news_add called')
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

def news_edit(request, news_id):
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

def news_delete(request, news_id):
    print('news_delete called')
    if request.method == 'POST':
        print('post method')
        news.objects.get(news_id = news_id).delete()
        return redirect('news_manager')
    else:
        print('get method')
        newslist = news.objects.values('news_id', 'for_whome', 'news_content', 'hyperlink')
        context = {'news' : newslist , 'news_id' : 0, 'delnews_id' : news_id}
        return render(request, 'Administrator/news_manager.html', context)

def collect_money(request):
    return render(request, 'Administrator/collect_money.html')

def signout(request):
    return redirect('admin_login')