# Generated by Django 3.1.7 on 2021-03-29 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0016_auto_20210329_0108'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='experiment',
            index=models.Index(fields=['name', 'stopped', 'customer_id'], name='hyp_experim_name_498342_idx'),
        ),
    ]