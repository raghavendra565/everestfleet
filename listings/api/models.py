from django.db import models

# TODO: Create your models here.

class FleetDailyTrips(models.Model):
    date = models.DateField(default=None)
    fare_total = models.FloatField(default=None)
    trips = models.IntegerField(default=None)
    hours_online = models.FloatField(default=None)
    total_km = models.FloatField(default=None)
    rating = models.FloatField(max_length=5, default=None)
    acceptance_rate_perc = models.FloatField(max_length=1, default=None)
    driver_cancellation_rate = models.FloatField(max_length=1, default=None)
    driver_id = models.IntegerField(blank=True, null=True, default=None)
    car_id = models.IntegerField(blank=True, null=True, default=None)
    cash_collected = models.FloatField(default=None)
    toll = models.FloatField(default=None)
    team_id = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ['id']
