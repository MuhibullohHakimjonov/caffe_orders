# Generated by Django 5.1.4 on 2025-01-14 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_items_alter_order_status_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]