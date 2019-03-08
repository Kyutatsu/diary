# Generated by Django 2.1.2 on 2018-11-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20181104_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='picture',
            field=models.ImageField(blank=True, upload_to='pictures/%Y%m%d/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]