# Generated by Django 4.2.1 on 2023-05-20 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_remove_member_whatsapp_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tithe',
            name='description',
        ),
    ]
