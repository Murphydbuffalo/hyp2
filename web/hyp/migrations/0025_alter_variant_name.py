# Generated by Django 3.2 on 2021-06-21 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0024_auto_20210620_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
