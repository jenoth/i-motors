# Generated by Django 4.2.9 on 2024-01-08 20:28

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("sku", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock_quantity", models.IntegerField(default=1000)),
                ("created_datetime", models.DateTimeField(auto_now_add=True)),
                ("updated_datetime", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "product"},
        )
    ]
