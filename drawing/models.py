import uuid

from django.db import models
from diary.models import Article
from author.models import Author


class DrawingModel(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            )
    title = models.CharField(max_length=200, null=True, default=None)

    # 消去予定
    article = models.OneToOneField(
            Article,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
    )
    author = models.ForeignKey(
            Author,
            on_delete=models.CASCADE,
            null=True,
            blank=True,
    )
    drawing = models.ImageField(
            upload_to='pictures/%Y%m%d',
            null=True, blank=True
    )
    drawing_base64 = models.TextField()  # 消去予定
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
