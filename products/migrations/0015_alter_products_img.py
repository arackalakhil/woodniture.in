# Generated by Django 3.2.14 on 2022-07-12 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_products_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img',
            field=models.CharField(max_length=3000),
        ),
    ]
