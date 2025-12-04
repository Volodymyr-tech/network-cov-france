from django.db import models




# Create your models here.
class Operator(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 20801
    name = models.CharField(max_length=100)  # Orange


class MobileSite(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    has_2g = models.BooleanField()
    has_3g = models.BooleanField()
    has_4g = models.BooleanField()
