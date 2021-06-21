# Generated by Django 3.2 on 2021-05-09 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hyp', '0022_auto_20210427_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='baseline',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='hypuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]