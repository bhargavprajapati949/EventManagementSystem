from django.shortcuts import render, redirect
from UserManager.form import EventCommitteeRegForm
from UserManager.models import User, Participant

# Create your views here.

def eventCommittee(request):
    return render(request, 'UserManager/eventCommittee.html')

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