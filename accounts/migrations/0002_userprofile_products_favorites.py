# Generated by Django 4.0.4 on 2022-06-27 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_options'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='products_favorites',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]