from import_export import resources,fields
from observe.metologys.models import precipitation_daily,precipitation_monthly,precipitation_annual,temperature_daily,temperature_monthly,\
    evaporation_daily,evaporation_monthly,humidity_daily,humidity_monthly,airpressure,wind_monthly,XY_Metology,\
    wind_daily,sunshine_daily,snowdepth,snowfall
from django.contrib.auth.models import User

from import_export.widgets import ForeignKeyWidget

class evaporation_dailyResource(resources.ModelResource):
    class Meta:
        model = evaporation_daily

class xy_metologyResource(resources.ModelResource):
    class Meta:
        model = XY_Metology

class evaporation_monthlyResource(resources.ModelResource):
    class Meta:
        model = evaporation_monthly

class humidity_dailyResource(resources.ModelResource):
    class Meta:
        model = humidity_daily

class humidity_monthlyResource(resources.ModelResource):
    class Meta:
        model = humidity_monthly

class airpressureResource(resources.ModelResource):

    created_by = fields.Field(
        column_name='created_by',
        attribute='User',
        widget=ForeignKeyWidget(User,'username')
    )
    class Meta:
        model = airpressure


class wind_monthlyResource(resources.ModelResource):
    class Meta:
        model = wind_monthly

class wind_dailyResource(resources.ModelResource):
    class Meta:
        model = wind_daily


class sunshine_dailyResource(resources.ModelResource):
    class Meta:
        model = sunshine_daily


class precipitation_dailyResource(resources.ModelResource):
    class Meta:
        model = precipitation_daily


class precipitation_monthlyResource(resources.ModelResource):
    class Meta:
        model = precipitation_monthly


class precipitation_annualResource(resources.ModelResource):
    class Meta:
        model = precipitation_annual


class temperature_dailyResource(resources.ModelResource):
    class Meta:
        model = temperature_daily

class temperature_monthlyResource(resources.ModelResource):
    class Meta:
        model = temperature_monthly


class snowdepthResource(resources.ModelResource):
    class Meta:
        model = snowdepth

class snowfallResource(resources.ModelResource):
    class Meta:
        model = snowfall
