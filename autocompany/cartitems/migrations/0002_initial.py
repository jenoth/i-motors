# Generated by Django 4.2.9 on 2024-01-08 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cartitems", "0001_initial"),
        ("carts", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="carts.cart"),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="products.product"),
        ),
        migrations.AlterUniqueTogether(name="cartitem", unique_together={("cart", "product")}),
    ]
