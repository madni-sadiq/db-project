# Generated by Django 3.1.5 on 2021-01-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frozery', '0005_order_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('COD', 'Cash On Delivery'), ('JZC', 'Jazzcash'), ('EPS', 'Easypaisa')], default='COD', max_length=3),
        ),
    ]