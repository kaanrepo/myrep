# Generated by Django 4.1.7 on 2023-03-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunes', '0010_usertune_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertune',
            name='notes',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]