from django.db import models


class Car(models.Model):
    inventory_code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
