# Generated by Django 4.1.4 on 2022-12-11 16:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_alter_profile_profile_picture'),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(default='General', on_delete=django.db.models.deletion.SET_DEFAULT, to='web.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.profile')),
            ],
        ),
    ]