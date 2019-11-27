from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from UserManager.models import Event_Committee

# Create your views here.

def redirectToEventHead_login(request):
    return redirect('eventHead_login')

def eventHead_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        if user and Event_Committee.objects.get(reg_no = user).is_event_head:
            auth_login(request, user)
            print('login success')
            return redirect('eventHead_dashboard')
        else:
            msg = "Email or Password is not valid"
            print(msg)
            context = {'message' : msg, 'email' : email}
            return render(request, 'Administrator/eventHead_login.html', context)
    else:
        msg = ""
        context = {'message' : msg , "email" : ""}
        return render(request, 'EventHead/eventHead_login.html',context)

#only login
def eventHead_dashboard(request):
    print(request.user)
    if request.user.is_authenticated:
        return render(request, 'EventHead/eventHead_dashboard.html')
    else:
        return redirect('eventHead_login')