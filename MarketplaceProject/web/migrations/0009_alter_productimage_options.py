# Generated by Django 4.1.4 on 2022-12-17 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_message_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['id']},
        ),
    ]
