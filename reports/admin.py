from django.contrib import admin
from .models import report1
from leaflet.admin import LeafletGeoAdmin
class reportadmin(LeafletGeoAdmin):
    pass
admin.site.register(report1,reportadmin)
# Register your models here.

