from import_export import resources
from observe.wells.models import groundwaterlevel,groundwaterlevel_manual,auto_groundwater,wells_quality,\
    welltoplevel,welllogging,lithologging,loggingdata,log_plot,drilling,casing,packing,XY_Well

class xy_wellResource(resources.ModelResource):
    class Meta:
        model = XY_Well

class groundwaterlevelResource(resources.ModelResource):
    class Meta:
        model = groundwaterlevel

class groundwaterlevel_manualResource(resources.ModelResource):
    class Meta:
        model = groundwaterlevel_manual

class auto_groundwaterResource(resources.ModelResource):
    class Meta:
        model = auto_groundwater

class wells_qualityResource(resources.ModelResource):
    class Meta:
        model = wells_quality

class welltoplevelResource(resources.ModelResource):
    class Meta:
        model = welltoplevel


class wellloggingResource(resources.ModelResource):
    class Meta:
        model = welllogging

class drillingResource(resources.ModelResource):
    class Meta:
        model = drilling


class packingResource(resources.ModelResource):
    class Meta:
        model = packing

class casingResource(resources.ModelResource):
    class Meta:
        model = casing

class lithologgingResource(resources.ModelResource):
    class Meta:
        model = lithologging


class log_plotResource(resources.ModelResource):
    class Meta:
        model = log_plot


class loggingdataResource(resources.ModelResource):
    class Meta:
        model = loggingdata
