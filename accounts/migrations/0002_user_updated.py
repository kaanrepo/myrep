# Generated by Django 4.1.7 on 2023-02-18 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
