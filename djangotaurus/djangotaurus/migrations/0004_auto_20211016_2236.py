# Generated by Django 3.2.8 on 2021-10-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotaurus', '0003_auto_20211016_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockpricecurrent',
            name='close',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='stockpricecurrent',
            name='high',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='stockpricecurrent',
            name='low',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='stockpricecurrent',
            name='open',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
