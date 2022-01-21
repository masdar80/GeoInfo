from import_export import resources
from observe.rivers.models import riverdischarge_daily,riverdischarge_anual,riverdischarge_monthly,surface_hq,\
    riverflowmeasure,discharge_survey,sectionareasurvey,sectiondata,XY_River

class riverdischarge_dailyResource(resources.ModelResource):
    class Meta:
        model = riverdischarge_daily

class xy_riverResource(resources.ModelResource):
    class Meta:
        model = XY_River


class riverdischarge_anualResource(resources.ModelResource):
    class Meta:
        model = riverdischarge_anual

class riverdischarge_monthlyResource(resources.ModelResource):
    class Meta:
        model = riverdischarge_monthly

class surface_hqResource(resources.ModelResource):
    class Meta:
        model = surface_hq

class riverflowmeasureResource(resources.ModelResource):
    class Meta:
        model = riverflowmeasure


class discharge_surveyResource(resources.ModelResource):
    class Meta:
        model = discharge_survey

class sectionareasurveyResource(resources.ModelResource):
    class Meta:
        model = sectionareasurvey


class sectiondataResource(resources.ModelResource):
    class Meta:
        model = sectiondata

