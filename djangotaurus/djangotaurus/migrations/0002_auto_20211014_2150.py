# Generated by Django 3.2.7 on 2021-10-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotaurus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='purchase_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='return_price',
        ),
        migrations.AddField(
            model_name='user',
            name='last_pw_change',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_pw_reset',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='salt',
            field=models.CharField(max_length=36, null=True, unique=True),
        ),
    ]
