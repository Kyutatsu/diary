# Generated by Django 2.1.2 on 2018-12-08 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
        ('drawing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawingmodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='author.Author'),
        ),
    ]
