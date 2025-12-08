from django.db import models


# Create your models here.
class Operator(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 20801
    name = models.CharField(max_length=100)  # Orange


class Location(models.Model):
    city = models.CharField(max_length=255)
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)

    class Meta:
        unique_together = ("x", "y")

    def __str__(self):
        return self.city


class MobileSite(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sites")
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    has_2g = models.BooleanField()
    has_3g = models.BooleanField()
    has_4g = models.BooleanField()
