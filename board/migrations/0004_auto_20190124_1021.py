# Generated by Django 2.1.2 on 2019-01-24 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_post_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]
