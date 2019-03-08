import uuid

from django.db import models
from django.urls import reverse
from author.models import Author
from drawing.models import DrawingModel


class Board(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
    )
    name = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey(
            Author,
            on_delete=models.SET_NULL,
            null=True,
    )

    def __str__(self):
        return self.name


class Topic(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
    )
    name = models.CharField(max_length=50)
    updated_date = models.DateTimeField()
    board = models.ForeignKey(
            Board,
            on_delete=models.SET_NULL,
            null=True,
    )
    author = models.ForeignKey(
            Author,
            on_delete=models.SET_NULL,
            null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """board:topicのurl"""
        return reverse('board:topic', args=[str(self.id)])


class Post(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
    )
    name = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    picture = models.FilePathField(null=True, blank=True)
    topic = models.ForeignKey(
            Topic,
            on_delete=models.CASCADE,
            null=True,
            blank=True,
    )
    author = models.ForeignKey(
            Author,
            on_delete=models.SET_NULL,
            null=True,
    )

    def __str__(self):
        return self.name
