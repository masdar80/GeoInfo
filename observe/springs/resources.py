from import_export import resources
from observe.springs.models import springdischarge_anual,springdischarge_avg_monthly,\
    springdischarge_avg_anual,springdischarge_daily,springdischarge_monthly,XY_Spring

class xy_springResource(resources.ModelResource):
    class Meta:
        model = XY_Spring

class springdischarge_monthlyResource(resources.ModelResource):
    class Meta:
        model = springdischarge_monthly

class springdischarge_dailyResource(resources.ModelResource):
    class Meta:
        model = springdischarge_daily

class springdischarge_avg_anualResource(resources.ModelResource):
    class Meta:
        model = springdischarge_avg_anual

class springdischarge_avg_monthlyResource(resources.ModelResource):
    class Meta:
        model = springdischarge_avg_monthly

class springdischarge_anualResource(resources.ModelResource):
    class Meta:
        model = springdischarge_anual

