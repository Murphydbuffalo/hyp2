# Generated by Django 3.2.5 on 2021-10-31 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0028_dailyvariantmetrics_uniq_metric_per_day_per_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdempotencyKey',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('key', models.TextField()),
            ],
        ),
        migrations.AddIndex(
            model_name='idempotencykey',
            index=models.Index(fields=['key'], name='hyp_idempot_key_ed9a1f_idx'),
        ),
        migrations.AddConstraint(
            model_name='idempotencykey',
            constraint=models.UniqueConstraint(fields=('key',), name='uniq_idempotency_key'),
        ),
    ]
