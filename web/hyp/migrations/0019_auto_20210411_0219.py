# Generated by Django 3.1.7 on 2021-04-11 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0018_auto_20210329_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='num_conversions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variant',
            name='num_interactions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name='variant',
            index=models.Index(fields=['customer_id', 'experiment_id'], name='hyp_variant_custome_de7aa4_idx'),
        ),
    ]
