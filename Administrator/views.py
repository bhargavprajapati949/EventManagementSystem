from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from UserManager.models import Collages, Stream
from EventWebSite.models import news
from Administrator.forms import addnews_form
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
    return render(request, 'Administrator/volunteer_manager.html')

def event_head_manager(request):
    return render(request, 'Administrator/event_head_manager.html')

def coordinator_manager(request):
    return render(request, 'Administrator/coordinator_manager.html')

def collage_manager(request):
    data = {}
# [('clg_id', 'clg_name')] + 
    clg = Collages.objects.values_list('clg_id', 'clg_name')
    data['collages'] = clg
    return render(request, 'Administrator/collage_manager.html', data)

def news_manager(request):
    newslist = news.objects.values_list('news_id', 'for_whome', 'news_content', 'hyperlink')
    context = {'news' : newslist }
    if request.method == 'POST':
        addnewsform = addnews_form(data = request.POST)
        if addnewsform.is_valid():
            addnewsform.save()
            addnewsform = addnews_form()
            context['addnews_form'] = addnewsform
            return render(request, 'Administrator/news_manager.html', context)
        else:
            context['addnews_form'] = addnewsform
            return render(request, 'Administrator/news_manager.html', context)
    else:
        addnewsform = addnews_form
        context['addnews_form'] = addnewsform
        return render(request, 'Administrator/news_manager.html', context)

def stream_manager(request):
    data = {}
    streamlist = Stream.objects.values_list('stream_id', 'stream_name')
    data['streams'] = streamlist
    return render(request, 'Administrator/stream_manager.html')

def collect_money(request):
    return render(request, 'Administrator/collect_money.html')

def signout(request):
    return redirect('admin_login')