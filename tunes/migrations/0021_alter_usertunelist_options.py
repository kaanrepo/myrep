# Generated by Django 4.1.7 on 2023-04-21 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0020_usertunelist_public'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertunelist',
            options={'ordering': ['updated']},
        ),
    ]
