# Generated by Django 3.2.8 on 2021-10-26 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangotaurus', '0011_auto_20211027_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangotaurus.stock'),
        ),
    ]
