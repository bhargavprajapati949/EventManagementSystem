from django.shortcuts import render, redirect
from UserManager.form import EventCommitteeRegForm
from UserManager.models import User, Participant

from Administrator.forms import news_model_form
from EventWebSite.models import news

# Create your views here.

def eventCommittee(request):
    n = news.objects.get(news_id = 1)
    if request.method == 'POST':
        print("post called")
        form = news_model_form(data = request.POST , instance = n)
        if form.is_valid():
            print("valid data")
            form.save()
            return redirect('homepage')
        else:
            print("invalid data")
            context = {'form' : form}
            return render(request, 'UserManager/eventCommittee.html', context)
    else:
        print("get called")
        form = news_model_form(instance = n)
        context = {'form' : form}
        return render(request, 'UserManager/eventCommittee.html', context)

def eventCommitteeRegForm(request):
    if request.method == 'POST':
        regform = EventCommitteeRegForm(data=request.POST)
        if regform.is_valid():
            user = regform.save()
            print('done')
            return redirect('successRegAsEventCommittee')
        else:
            print('invalid data')
            context = {'regform' : regform }
            return render(request, 'UserManager/event_committee_reg_form.html', context)
    else:
        regform = EventCommitteeRegForm()
        context = {'regform' : regform }
        return render(request, 'UserManager/event_committee_reg_form.html', context)

def successRegAsEventCommittee(request):
    return render(request, 'UserManager/successRegAsEventCommittee.html')