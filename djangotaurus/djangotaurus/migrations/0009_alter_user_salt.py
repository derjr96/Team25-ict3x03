# Generated by Django 3.2.8 on 2021-10-21 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotaurus', '0008_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
