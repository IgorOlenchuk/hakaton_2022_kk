# Generated by Django 3.1.6 on 2022-08-26 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_purchase'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
