# Generated by Django 2.1.2 on 2018-12-27 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]
