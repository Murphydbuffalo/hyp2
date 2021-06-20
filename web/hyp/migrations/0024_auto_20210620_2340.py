# Generated by Django 3.2 on 2021-06-20 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0023_auto_20210509_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Variant name'),
        ),
        migrations.AddConstraint(
            model_name='experiment',
            constraint=models.UniqueConstraint(fields=('customer_id', 'name'), name='uniq_experiment_name_per_customer'),
        ),
    ]
