from django.forms import ModelForm
from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['a_title', 'text']

        error_messages = {
                'text': {
                    'required': '本文を入力してください',
                },
        }
