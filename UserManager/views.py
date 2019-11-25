from django.shortcuts import render, redirect
from UserManager.form import EventCommitteeRegForm, EventCommitteeDetailForm
from UserManager.models import User, Participant

from Administrator.forms import news_model_form
from EventWebSite.models import news

# Create your views here.

def eventCommittee(request):
    return render(request, 'UserManager/eventCommittee.html')


def eventCommitteeRegForm(request):
    if request.method == 'POST':
        regform = EventCommitteeRegForm(data=request.POST)
        infoform = EventCommitteeDetailForm(data=request.POST)
        if regform.is_valid():
            user = regform.save()
            mem = infoform.save(commit = False)
            mem.reg_no = user
            mem.save()
            print('done')
            return redirect('successRegAsEventCommittee')
        else:
            print('invalid data')
            context = {'regform' : regform , 'infoform': infoform}
            return render(request, 'UserManager/event_committee_reg_form.html', context)
    else:
        infoform = EventCommitteeDetailForm()
        regform = EventCommitteeRegForm()
        context = {'regform' : regform , 'infoform': infoform}
        return render(request, 'UserManager/event_committee_reg_form.html', context)

def successRegAsEventCommittee(request):
    return render(request, 'UserManager/successRegAsEventCommittee.html')