# Generated by Django 2.1.5 on 2019-01-20 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0008_auto_20190121_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawingmodel',
            name='drawing',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/%Y%m%d'),
        ),
    ]
