from import_export import resources
from observe.rivers.models import riverdischarge_daily

class River_dis_dailyResource(resources.ModelResource):
    class Meta:
        model = riverdischarge_daily
        widgets = {

                     'obs_datetime': {'format': '%y.%m.%d'},
        }
        fields = ('waterpoint__id_field',)