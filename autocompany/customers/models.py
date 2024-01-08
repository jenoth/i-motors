from django.db import models

description_of_customer_address = (
    "Complete residential address which made up of a house number, street name, town or city, zip code and etc."
)
example_of_customer_address = "No 08, Allarai North Kodikamam, Jaffna, Sri Lanka, 40000."


class Customer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    address = models.TextField(
        verbose_name=description_of_customer_address,
        help_text=f"{description_of_customer_address} Eg, {example_of_customer_address}",
    )

    class Meta:
        db_table = "customer"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip().casefold()
        self.last_name = self.last_name.strip().casefold()
        self.email = self.email.strip().casefold()
        self.address = self.address.strip().casefold()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
