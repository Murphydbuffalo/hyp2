# Generated by Django 3.1.1 on 2020-12-16 15:34

from django.db import migrations, models
import hyp.models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0007_auto_20201208_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='access_token',
            field=models.UUIDField(default=hyp.models.create_access_token),
        ),
    ]