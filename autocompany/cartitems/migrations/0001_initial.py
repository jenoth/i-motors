# Generated by Django 4.2.9 on 2024-01-08 20:28

from django.db import migrations, models

import autocompany.cartitems.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=1,
                        validators=[autocompany.cartitems.models.validate_positive],
                    ),
                ),
            ],
            options={
                "db_table": "cart_item",
                "db_table_comment": "Ordered(cart) items of customer",
            },
        )
    ]
