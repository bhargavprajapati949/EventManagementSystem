from django.shortcuts import render, redirect
from UserManager.models import Collages, Stream
from EventWebSite.models import news

# Create your views here.

def redirectToAdmin_login(request):
    return redirect('admin_login')

def admin_login(request):
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
    data = {}
    newslist = news.objects.values_list('news_id', 'for_whome', 'news_containt', 'hyperlink')
    data['news'] = newslist
    return render(request, 'Administrator/news_manager.html', data)

def stream_manager(request):
    data = {}
    streamlist = Stream.objects.values_list('stream_id', 'stream_name')
    data['streams'] = streamlist
    return render(request, 'Administrator/stream_manager.html')

def collect_money(request):
    return render(request, 'Administrator/collect_money.html')

def signout(request):
    return redirect('admin_login')