from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply_to = models.ForeignKey("Message", on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(blank=True, auto_now_add=True)
    edit_date = models.DateTimeField(blank=True, null=True, default=None)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liking")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="disliking")
    is_active = models.BooleanField(default=True)

    #TODO: Do the equivalent of select_related(reply_to) using raw sql queries

    #Traverse through specified number of parent messages and aggregate them recursively
    def get_replied_messages(self,n):
        return Message.objects.raw(
            'WITH RECURSIVE replies_to(id) AS (\
            SELECT forum_message.reply_to_id \
            FROM forum_message \
            WHERE forum_message.id = %s \
            UNION \
            SELECT forum_message.reply_to_id \
            FROM forum_message, replies_to \
            WHERE forum_message.id = replies_to.id \
            LIMIT %s ) \
            SELECT * FROM forum_message \
            WHERE forum_message.id IN replies_to', [self.pk, n])

    #Traverse through all parent messages and aggregate them recursively
    def get_all_replied_messages(self):
        return Message.objects.raw(
            'WITH RECURSIVE replies_to(id) AS (\
            SELECT forum_message.reply_to_id \
            FROM forum_message \
            WHERE forum_message.id = %s \
            UNION \
            SELECT forum_message.reply_to_id \
            FROM forum_message, replies_to \
            WHERE forum_message.id = replies_to.id ) \
            SELECT * FROM forum_message \
            WHERE forum_message.id IN replies_to', [self.pk])

    def soft_delete(self, commit=True):
        """Does not actually delete the message, sets it as inactive"""
        self.is_active = False
        if commit:
            self.save()
        return self

    def updateandsave(self, content, commit=True):
        self.content = content
        self.edit_date = datetime.now()
        if commit:
            self.save()
        return self

    def likes_count(self):
        return str(self.likes.count())

    def dislikes_count(self):
        return str(self.dislikes.count())

    def __str__(self):
        return f"{self.id} - {self.content[:20]}"
