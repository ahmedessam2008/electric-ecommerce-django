# Generated by Django 4.0.4 on 2022-07-02 18:54

import creditcards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_price_orderdetails_new_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderdetails',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_adress', models.CharField(blank=True, max_length=150)),
                ('shipping_mobile', models.CharField(blank=True, max_length=150)),
                ('pyment_method', models.CharField(choices=[('paypal', 'paypal'), ('cod', 'cod'), ('credit', 'credit'), ('bank', 'bank')], max_length=100)),
                ('card_number', creditcards.models.CardNumberField(max_length=25)),
                ('expired', creditcards.models.CardExpiryField(default='12/22')),
                ('security_code', creditcards.models.SecurityCodeField(max_length=4)),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
