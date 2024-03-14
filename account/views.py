from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserInfoForm
import re

# Create your views here.

def signup(request):
    usercreationform = None
    if request.method == "POST":
        usercreationform = UserCreationForm(request.POST)
        if usercreationform.is_valid():
            #print(f'{request.POST["username"]}, {request.POST["profile_name"]}, {request.POST["password1"]}, {request.POST["password2"]}')
            user = usercreationform.save(commit=True)
            login(request, user)
            if request.GET.get("next") != None and not re.match(f'{reverse("account")}*', request.GET.get("next")):
                return redirect(request.GET[next])
            else:
                return redirect(reverse("forum:index"))
    else:
         usercreationform = UserCreationForm()

    return render(request, "account/signup.html",
                  {"form": usercreationform})

@login_required
def settings(request):
    userformfieldclassdict = UserInfoForm.formClassFromFieldsFactoryDict()
    if request.method == "POST":
        for field, formclass in userformfieldclassdict.items():
            if request.POST.get("submit") == field:
                receivedform = formclass(request.POST)
                if receivedform.is_valid():
                    user = request.user
                    setattr(user, field, receivedform.cleaned_data[field])
                    user.save()
                else:
                    return HttpResponseBadRequest()
            else:
                continue
    initializedformfieldclasses = [form(instance=request.user) for form in userformfieldclassdict.values()]
    passwordchangeform = PasswordChangeForm(request.user)

    return render(request, "account/settings.html", {"user": request.user, 
                                                     "forms": initializedformfieldclasses,
                                                     "passwordchangeform": passwordchangeform})

@login_required
def passwordchange(request):
    if request.method == "POST":
        passform = PasswordChangeForm(request.user, request.POST)
        if passform.is_valid():
            formuser = passform.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(["POST"])

@login_required
def deleteuser(request):
    if request.method == "POST":
        if request.POST.get("submit") == "delete":
            user = request.user
            user.is_active = False
            user.save()
            logout(request=request)
            return redirect(reverse("forum:index"))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(["POST"])