# Generated by Django 2.2.4 on 2019-08-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190820_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku_code',
            field=models.CharField(max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='productpropertyvalues',
            name='sku_code',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
