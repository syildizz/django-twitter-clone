
from django.urls import path, reverse_lazy
from django.contrib.auth import views

from . import views

app_name = "forum"
urlpatterns = [
    path('', views.forumindex, name="index"),
    path('<str:username>', views.userpage, name="userpage"),
    path('<str:username>/with_replies', views.userpagewithreplies, name="userpagewithreplies"),
    path('messages/<int:msgid>', views.messageinfo, name="messageinfo"),
    path('messages/rate/<int:msgid>', views.ratepage, name="ratepage"),
    path('messages/ratings/<int:msgid>', views.ratingspage, name="ratingspage"),
    path('messages/create', views.createmessage, name="createmessage"),
    path('messages/create/<int:msgid>', views.createmessage, name="createmessage"),
    path('messages/read/<int:msgid>', views.readmessage, name="readmessage"),
    path('messages/update/<int:msgid>', views.updatemessage, name="updatemessage"),
    path('messages/delete/<int:msgid>', views.deletemessage, name="deletemessage")
]