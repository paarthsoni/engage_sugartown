# Generated by Django 3.2.5 on 2022-05-23 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sugartownapp', '0014_alter_user_wallet_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_cart_value',
            name='coupon_applied',
            field=models.CharField(default='None', max_length=1024, null=True),
        ),
    ]
