# Generated by Django 3.2.5 on 2022-05-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sugartownapp', '0013_user_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_wallet',
            name='wallet_balance',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
