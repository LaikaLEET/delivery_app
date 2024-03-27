from django.db import models

from .mixins import CreatedUpdatedMixin
from .enums import LogTypes


class ChangeLocationLog(CreatedUpdatedMixin):
    track_id = models.ForeignKey('delivery_api.Track', null=True, on_delete=models.CASCADE, blank=True)
    location_id = models.ForeignKey('delivery_api.Location', null=True, on_delete=models.CASCADE, blank=True)
    type = models.PositiveSmallIntegerField(choices=LogTypes.choices())

