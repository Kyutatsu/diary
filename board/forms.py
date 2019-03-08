from django.forms import ModelForm
from .models import Post, Topic


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text']

        error_messages = {
                'text': {
                    'required': '本文を入力してください',
                },
        }
