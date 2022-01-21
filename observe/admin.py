from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from observe.rivers.models import riverdischarge_daily,riverdischarge_monthly,riverdischarge_anual,riverflowmeasure,\
surface_hq,discharge_survey,sectionareasurvey,sectiondata
from .models import Waterpoint
from observe.wells.models import groundwaterlevel,groundwaterlevel_manual,wells_quality,welltoplevel,auto_groundwater,\
welllogging,lithologging,loggingdata, log_plot,drilling,packing,casing,XY_Well
from observe.metologys.models import precipitation_daily,precipitation_monthly,precipitation_annual,temperature_daily,temperature_monthly,\
    evaporation_daily,evaporation_monthly,humidity_daily,humidity_monthly,airpressure,wind_monthly,wind_daily,sunshine_daily,snowfall,snowdepth
from observe.springs.models import springdischarge_anual,springdischarge_avg_monthly,springdischarge_avg_anual,\
    springdischarge_monthly,springdischarge_daily,XY_Spring
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from observe.rivers.models import XY_River

from observe.metologys.models import XY_Metology


class WaterpointAdmin(LeafletGeoAdmin):
    pass
admin.site.register(Waterpoint,WaterpointAdmin)
#######river########

@admin.register(XY_River)
class XY_RiverAdmin(ImportExportModelAdmin):
    pass

class riverdischarge_dailyAdmin(ImportExportModelAdmin):
    # pass
    class Meta:
        model = riverdischarge_daily
        widgets = {

                     'obs_datetime': {'format': 'yyyy.mm.dd'},
        }
        fields = ('waterpoint__id_field',)

class riverdischarge_monthlyAdmin(ImportExportModelAdmin):
    # pass
    class Meta:
        model = riverdischarge_monthly
        widgets = {

                     'obs_datetime': {'format': 'yyyy.mm.dd'},
        }
        fields = ('waterpoint__id_field',)

@admin.register(riverdischarge_daily)
class riverdischarge_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(riverdischarge_anual)
class riverdischarge_anualAdmin(ImportExportModelAdmin):
    pass
@admin.register(riverdischarge_monthly)
class riverdischarge_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(riverflowmeasure)
class riverflowmeasureAdmin(ImportExportModelAdmin):
    pass
@admin.register(surface_hq)
class surface_hqAdmin(ImportExportModelAdmin):
    pass
@admin.register(discharge_survey)
class discharge_surveyAdmin(ImportExportModelAdmin):
    pass
@admin.register(sectionareasurvey)
class sectionareasurveyAdmin(ImportExportModelAdmin):
    pass
@admin.register(sectiondata)
class sectiondataAdmin(ImportExportModelAdmin):
    pass
#######well###
@admin.register(XY_Well)
class xy_wellAdmin(ImportExportModelAdmin):
    pass

@admin.register(groundwaterlevel)
class groundwaterlevelAdmin(ImportExportModelAdmin):
    pass
@admin.register(groundwaterlevel_manual)
class groundwaterlevel_manualAdmin(ImportExportModelAdmin):
    pass
@admin.register(wells_quality)
class wells_qualityAdmin(ImportExportModelAdmin):
    pass
@admin.register(welltoplevel)
class welltoplevelAdmin(ImportExportModelAdmin):
    pass
@admin.register(auto_groundwater)
class auto_groundwaterAdmin(ImportExportModelAdmin):
    pass

@admin.register(lithologging)
class lithologgingAdmin(ImportExportModelAdmin):
    pass

@admin.register(loggingdata)
class loggingdataAdmin(ImportExportModelAdmin):
    pass


@admin.register(welllogging)
class wellloggingAdmin(ImportExportModelAdmin):
    pass


@admin.register(log_plot)
class log_plotAdmin(ImportExportModelAdmin):
    pass


@admin.register(drilling)
class drillingAdmin(ImportExportModelAdmin):
    pass


@admin.register(casing)
class casingAdmin(ImportExportModelAdmin):
    pass


@admin.register(packing)
class packingAdmin(ImportExportModelAdmin):
    pass



######springs
@admin.register(XY_Spring)
class xy_springAdmin(ImportExportModelAdmin):
    pass


@admin.register(springdischarge_daily)
class springdischarge_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(springdischarge_monthly)
class springdischarge_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(springdischarge_avg_anual)
class springdischarge_avg_anualAdmin(ImportExportModelAdmin):
    pass
@admin.register(springdischarge_avg_monthly)
class springdischarge_avg_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(springdischarge_anual)
class springdischarge_anualAdmin(ImportExportModelAdmin):
    pass
####metology###

@admin.register(XY_Metology)
class XY_MetologyAdmin(ImportExportModelAdmin):
    pass
@admin.register(evaporation_daily)
class evaporation_dailyAdmin(ImportExportModelAdmin):
    pass

@admin.register(evaporation_monthly)
class evaporation_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(humidity_daily)
class humidity_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(humidity_monthly)
class humidity_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(airpressure)
class airpressureAdmin(ImportExportModelAdmin):
    pass
@admin.register(wind_monthly)
class wind_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(wind_daily)
class wind_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(sunshine_daily)
class sunshine_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(precipitation_daily)
class precipitation_dailyAdmin(ImportExportModelAdmin):
    pass
@admin.register(precipitation_monthly)
class precipitation_monthlyAdmin(ImportExportModelAdmin):
    pass
@admin.register(precipitation_annual)
class precipitation_annualAdmin(ImportExportModelAdmin):
    pass
@admin.register(temperature_daily)
class temperature_dailyAdmin(ImportExportModelAdmin):
    pass

@admin.register(temperature_monthly)
class temperature_monthlyAdmin(ImportExportModelAdmin):
    pass

@admin.register(snowfall)
class snowfallAdmin(ImportExportModelAdmin):
    pass


@admin.register(snowdepth)
class snowdepthAdmin(ImportExportModelAdmin):
    pass
########## end metology

