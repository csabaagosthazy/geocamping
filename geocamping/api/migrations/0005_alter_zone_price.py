# Generated by Django 3.2.13 on 2022-06-09 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220609_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
