# Generated by Django 2.1.5 on 2019-01-20 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0007_drawingmodel_drawing_base64'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawingmodel',
            name='drawing',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/None/%Y%m%d'),
        ),
    ]
