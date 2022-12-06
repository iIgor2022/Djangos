from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='measurements', on_delete=models.CASCADE)
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, blank=True)
