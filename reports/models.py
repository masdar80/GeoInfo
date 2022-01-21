from django.db import models

from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

class report1(models.Model):
    name = models.CharField(max_length=20)
    location = models.PointField(srid=4326)
    objects = GeoManager()
    def __unicode__(self):
        return self.name