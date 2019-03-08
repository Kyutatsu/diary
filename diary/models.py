from django.db import models
from author.models import Author


class Article(models.Model):
    '''日記の1記事を表すクラス'''

    a_title = models.CharField(max_length=200)
    text = models.TextField()                # 多量テキスト用
    created_date = models.DateTimeField(auto_now=True)    # datetime.datetime()
    picture = models.FilePathField(null=True, blank=True)
    author = models.ForeignKey(
            Author,
            on_delete=models.CASCADE,
            blank=True,
            null=True,
    )

    def __str__(self):
        return self.a_title

    @property
    def text20(self):
        '''本文最初20文字を返す。

        propertyデコレで読み取り専用値にして返す
        property(fget, fset, fdel, doc)のgetter
        2018-12-2これ要らないのでは(?)'''
        return (self.text[:20] + '...')
