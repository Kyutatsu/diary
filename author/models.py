import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from diarySite.settings import MEDIA_ROOT


class Author(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
    )
    name = models.CharField(
            max_length=50,
            help_text='名前を入力してください',
    )
    self_introduction = models.TextField(
            max_length=255,
            help_text='255文字以内',
            null=True, blank=True
    )
    birth = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
    )
    icon = models.FilePathField(MEDIA_ROOT, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_age(self):
        """誕生日登録すれば現在の年齢返す"""
        today = datetime.date.today()
        birth_to_now_days = today - self.birth
        return str(birth_to_now_days.days // 365)

    def get_absolute_url(self):
        return reverse('author:profile', args=[str(self.id)])
