# Generated by Django 2.1.2 on 2018-12-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0004_auto_20181214_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawingmodel',
            name='drawing',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/%Y%m%d/'),
        ),
    ]