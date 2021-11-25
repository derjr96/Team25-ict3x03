# Generated by Django 3.2.8 on 2021-10-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotaurus', '0009_alter_user_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login_attempt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='login_attempts',
            field=models.IntegerField(default=0),
        ),
    ]
