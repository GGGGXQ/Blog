import uuid
from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import gettext as _ 

from account.models import User


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now_add=True)

    def modified_at_formatted(self):
        time_string = timesince(self.created_at)
        translations = {
            "year": _("年"),
            "month": _("个月"),
            "week": _("周"),
            "day": _("天"),
            "hour": _("小时"),
            "minute": _("分钟"),
            "second": _("秒"),
            "ago": _("前"),
        }
        for en, zh in translations.items():
            time_string = time_string.replace(en, zh).replace(en + "s", zh)

        return time_string + _("前") 



class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)

    def created_at_formatted(self):
        time_string = timesince(self.created_at)
        translations = {
            "year": _("年"),
            "month": _("个月"),
            "week": _("周"),
            "day": _("天"),
            "hour": _("小时"),
            "minute": _("分钟"),
            "second": _("秒"),
            "ago": _("前"),
        }
        for en, zh in translations.items():
            time_string = time_string.replace(en, zh).replace(en + "s", zh)

        return time_string + _("前") 