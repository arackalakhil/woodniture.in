# Generated by Django 3.2.14 on 2022-08-07 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
