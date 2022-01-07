from django.db import models


# Create your models here.
class RealData(models.Model):
    date_time = models.DateTimeField(blank=False)
    rate = models.FloatField(blank=True, null=True)


class InterpolateData(models.Model):
    date_time = models.DateTimeField(blank=False)
    rate = models.FloatField(blank=False)
