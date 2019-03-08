# Generated by Django 2.1.2 on 2018-12-12 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_article_author'),
        ('drawing', '0002_drawingmodel_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawingmodel',
            name='article',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diary.Article'),
        ),
    ]
