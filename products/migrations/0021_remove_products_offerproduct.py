# Generated by Django 3.2.14 on 2022-07-27 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_auto_20220727_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='offerproduct',
        ),
    ]
