from math import ceil
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from .models import Message
from .forms import MessageForm, RatingForm

# Create your views here.

@login_required
def ratepage(request, msgid):
    message = get_object_or_404(Message, id=msgid)
    if request.method == 'POST':
        ratingform = RatingForm(request.POST)
        if ratingform.is_valid():
            rating = ratingform.cleaned_data["rating"]
            user = request.user
            match rating:
                case "like":
                    if user.disliking.filter(id=msgid):
                        user.disliking.remove(message)
                    user.liking.add(message)
                    return redirect(request.META.get('HTTP_REFERER'))
                case "dislike":
                    message = get_object_or_404(Message, id=msgid)
                    if user.liking.filter(id=msgid):
                        user.liking.remove(message)
                    user.disliking.add(message)
                    return redirect(request.META.get('HTTP_REFERER'))
                case "none":
                    if user.liking.filter(id=msgid):
                        user.liking.remove(message)
                    if user.disliking.filter(id=msgid):
                        user.disliking.remove(message)
                    return redirect(request.META.get('HTTP_REFERER'))

                case _:
                    return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(["POST"])

def ratingspage(request, msgid):
    message = get_object_or_404(Message, id=msgid)
    messagelikes = message.likes.all()
    messagedislikes = message.dislikes.all()
    return render(request, "forum/ratingspage.html", {"messagelikes": messagelikes,
                                                 "messagedislikes": messagedislikes})



@login_required
def createmessage(request, msgid=None):
    if request.method == 'POST':
        repliedmessage = get_object_or_404(Message, id=msgid) if msgid else None
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            receivedmessage = messageform.save(commit=False)
            receivedmessage.author = request.user
            receivedmessage.reply_to = repliedmessage
            receivedmessage.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(["POST"])

def readmessage(request, msgid):
    if request.method == 'GET' or 'HEAD':
        try:
            message = Message.objects.select_related('reply_to').get(id=msgid)
        except Message.DoesNotExist:
            raise Http404("Message does not exist")
        return render(request, "forum/messagedisplay.htmlinc", {"message": message})
    else:
        return HttpResponseNotAllowed(["GET", "HEAD"])

@login_required
def updatemessage(request, msgid):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=msgid)
        if not message.is_active:
            return HttpResponseForbidden()
        if request.user == message.author:
            messageform = MessageForm(request.POST)
            if messageform.is_valid():
                content = messageform.cleaned_data['content']
                message.updateandsave(content)
                return redirect(reverse('forum:userpage', args=[request.user.username]))
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotAllowed(["POST"])

@login_required
def deletemessage(request, msgid):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=msgid)
        if request.user == message.author:
            message.soft_delete()
            return redirect(reverse('forum:userpage', args=[request.user.username]))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotAllowed(["POST"])

def forumindex(request):
    currpage = int(request.GET.get("page") or 1)
    messagecount = Message.objects.all().count()
    messages = Message.objects.all().select_related("reply_to").order_by('-id', '-pub_date')[10*(currpage-1):10*currpage]
    pagenum = [*range(1, ceil(messagecount / 10) + 1)]
    return render(request, "forum/index.html", {"messages": messages,
                                                "pagenum": pagenum})

def userpage(request, username):
    userpageowner = get_object_or_404(get_user_model(), username=username)

    messageform = MessageForm() if request.user.is_authenticated else None

    currpage = int(request.GET.get("page") or 1)
    messagecount = userpageowner.message_set.filter(reply_to=None).count()
    messages = userpageowner.message_set.filter(reply_to=None).order_by('-id', '-pub_date')[10*(currpage - 1):10*currpage]
    pagenum = [*range(1, ceil(messagecount / 10) + 1)]

    return render(request, "forum/userpage.html",
                  {"userpageowner": userpageowner,
                   "messages": messages,
                   "messageform": messageform,
                   "pagenum": pagenum})

def userpagewithreplies(request, username):
    userpageowner = get_object_or_404(get_user_model(), username=username)

    messageform = MessageForm() if request.user.is_authenticated else None

    messagecount = userpageowner.message_set.all().count()
    currpage = int(request.GET.get("page") or 1)
    messages = userpageowner.message_set.all().select_related("reply_to").order_by('-id', '-pub_date')[10*(currpage - 1):10*currpage]
    pagenum = [*range(1, ceil(messagecount / 10) + 1)]

    return render(request, "forum/userpage.html",
                  {"userpageowner": userpageowner,
                   "messages": messages,
                   "messageform": messageform,
                   "pagenum": pagenum})

def messageinfo(request, msgid):
    message = get_object_or_404(Message, pk=msgid)

    messagereplyform = MessageForm() if request.user.is_authenticated else None
    messageupdateform = MessageForm(instance=message) if request.user.is_authenticated else None
    ratingform = RatingForm() if request.user.is_authenticated else None

    replies = message.message_set.all().order_by('-id', '-pub_date')
    reply_chain = message.get_all_replied_messages()

    return render(request, "forum/messageinfo.html",
                  {"message": message,
                   "replies": replies,
                   "reply_chain": reply_chain,
                   "messagereplyform": messagereplyform,
                   "messageupdateform": messageupdateform,
                   "ratingform": ratingform})
