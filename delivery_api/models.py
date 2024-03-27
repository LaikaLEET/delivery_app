from django.db import models

from additional_utilities.mixins import CreatedUpdatedMixin
from additional_utilities.enums import CargoStatuses


class Location(CreatedUpdatedMixin):
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)


class Tracks(CreatedUpdatedMixin):
    tail_number = models.CharField(max_length=5, blank=True, null=True)
    current_location = models.ForeignKey(Location, null=True, related_name="tracks", on_delete=models.CASCADE,
                                         blank=True)
    lifting_capacity = models.IntegerField(blank=True, null=True)


class Cargo(CreatedUpdatedMixin):
    status = models.IntegerField(default=1, choices=CargoStatuses.choices(), blank=True)
    pick_up = models.ForeignKey(Location, null=True, related_name="location_picup", on_delete=models.CASCADE,
                                blank=True)
    delivery = models.ForeignKey(Location, null=True, related_name="location_delivery", on_delete=models.CASCADE,
                                 blank=True)
    weigh = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    track = models.ForeignKey(Tracks, null=True, related_name="track", on_delete=models.CASCADE, blank=True)
