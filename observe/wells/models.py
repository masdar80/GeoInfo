
from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class ObservationWell_Inf(models.Model):
    construction_method = models.CharField(max_length=254)
    completion_date = models.DateField()
    construction_firm = models.CharField(max_length=50)
    total_depth = models.IntegerField()
    well_type = models.CharField(max_length=50)
    obs_start_date = models.DateField()
    obs_end_date=models.DateField()
    obs_item=models.CharField(max_length=254)
    obs_frequency=models.CharField(max_length=254)
    obs_type=models.CharField(max_length=254)
    equipment_spec=models.CharField(max_length=254)
    data_source_2 =models.CharField(max_length=254)
    other_source_2=models.CharField(max_length=254)
    well_registration =models.CharField(max_length=254)
    data_availability=models.CharField(max_length=254)
    coordinates_inf=models.CharField(max_length=254)

    def __str__(self):
        return self.well_type
class XY_Well(models.Model):
    id_field = models.CharField(max_length=254,primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    old_id = models.CharField(max_length=254,null=True,blank=True)
    sitename_a = models.CharField(max_length=254,null=True,blank=True)
    sitename_e = models.CharField(max_length=254,null=True,blank=True)
    type = models.CharField(max_length=254,null=True,blank=True)
    agency = models.CharField(max_length=254,null=True,blank=True)
    mohafaza = models.CharField(max_length=254,null=True,blank=True)
    montika = models.CharField(max_length=254,null=True,blank=True)
    nahia = models.CharField(max_length=254,null=True,blank=True)
    village = models.CharField(max_length=254,null=True,blank=True)
    sub_baisn = models.CharField(max_length=254,null=True,blank=True)

    w84_utm_x = models.FloatField(null=True,blank=True)
    w84_utm_y = models.FloatField(null=True,blank=True)
    w84_utm_z = models.FloatField(null=True,blank=True)
    means_z = models.CharField(max_length=254,null=True,blank=True)

    data_sourc = models.CharField(max_length=254,null=True,blank=True)
    geom = models.MultiPointField(srid=4326)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.jpg',upload_to='xy_well_pic')


    def __unicode__(self):
        return self.id_field

    def get_absolute_url(self):
        return reverse('xy_wells',args=[])
class well_inf(models.Model):
    surveyer_name = models.CharField(max_length=254,null=True,blank=True)
    survey_date = models.DateField(null=True,blank=True)
    gps_number = models.CharField(max_length=50,null=True,blank=True)
    well_completion_date =models.DateField(null=True,blank=True)
    open_date = models.DateField(null=True,blank=True)
    close_date=models.DateField(null=True,blank=True)
    water_use=models.CharField(max_length=254,blank=True)
    atitude_of_top_of_well=models.CharField(max_length=254,blank=True)
    total_depth=models.IntegerField(null=True,blank=True)
    well_ownership=models.CharField(max_length=254,null=True,blank=True)
    well_oner_name=models.CharField(max_length=254,null=True,blank=True)
    dia_top_casing=models.CharField(max_length=254,null=True,blank=True)
    min_dia_casing=models.CharField(max_length=254,null=True,blank=True)
    pump_installed_in_the_well = models.CharField(max_length=254,null=True,blank=True)
    measurment_items = models.CharField(max_length=254,null=True,blank=True)
    gw_meas_freq_dryseason = models.CharField(max_length=254,null=True,blank=True)
    gw_meas_freq_rainyseason = models.CharField(max_length=254,null=True,blank=True)
    labo_qual_analysis_freq_drysea =models.CharField(max_length=254,null=True,blank=True)
    labo_qual_analysis_freq_rainysea=models.CharField(max_length=254,null=True,blank=True)
    type_of_measurment=models.CharField(max_length=254,null=True,blank=True)
    type_of_automatic_sensor=models.CharField(max_length=254,null=True,blank=True)
    sensor_depth=models.IntegerField(null=True,blank=True)
    condition_of_station=models.CharField(max_length=254,null=True,blank=True)
    improvement_point=models.CharField(max_length=254,null=True,blank=True)
    xy_well = models.OneToOneField(XY_Well, on_delete=models.CASCADE,related_name = 'well_inf', primary_key = True,)

    def __unicode__(self):
        return self.gps_number
def add_well_inf(sender,**kwarg):
    if kwarg['created']:
        xy_well_inf = well_inf.objects.create(xy_well= kwarg['instance'])
post_save.connect(add_well_inf,sender=XY_Well)

class groundwaterlevel(models.Model):
    obs_datetime = models.DateField()
    depth_to_water= models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    waterlevel =models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    meas_method = models.CharField(max_length=50, blank=True,null=True)
    data_source = models.CharField(max_length=50, blank=True,null=True)
    other_source = models.CharField(max_length=50, blank=True,null=True)

    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='groundwaterlevels')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('-obs_datetime',)

    def __unicode__(self):
        return self.remarks
class groundwaterlevel_manual(models.Model):
    obs_datetime = models.DateField()
    depth_to_water= models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    waterlevel =models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    meas_method = models.CharField(max_length=250, blank=True,null=True)
    data_source = models.CharField(max_length=250, blank=True,null=True)
    other_source = models.CharField(max_length=250, blank=True,null=True)
    remarks = models.CharField(max_length=250,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='groundwaterlevel_manuals')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks
class wells_quality(models.Model):
    obs_datetime = models.DateField()
    ph = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    ec_ms_m=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    temp=models.CharField(max_length=254,null=True,blank=True)
    meas_method=models.CharField(max_length=254,null=True,blank=True)
    data_source=models.CharField(max_length=254,null=True,blank=True)
    other_source=models.CharField(max_length=254,null=True,blank=True)
    remarks=models.CharField(max_length=254,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='wells_qualitys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks
class welltoplevel(models.Model):
    meas_date =models.DateField()
    x_stm = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    y_stm =models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    z_stm = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    x_utm = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    y_utm = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    z_utm = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    ground_level = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    top_concrete = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    top_casing=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    source=models.CharField(max_length=245,null=True,blank=True)
    method=models.CharField(max_length=254,null=True,blank=True)
    accuracy=models.CharField(max_length=254,null=True,blank=True)
    convert_g_sys=models.CharField(max_length=254,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='welltoplevels')

    class Meta:
        unique_together = (('meas_date', 'waterpoint'),)
        ordering = ('meas_date',)

    def __unicoce__(self):
        return self.source
class auto_groundwater(models.Model):
    obs_date = models.DateField()
    depth_m =models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    gw_level_m = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='auto_groundwaters')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.gw_level_m
class welllogging(models.Model):
    log_from = models.DateField()
    log_to=models.DateField()
    log_layer=models.CharField(max_length=254,null=True,blank=True)
    log_type=models.CharField(max_length=254,null=True,blank=True)
    data_source=models.CharField(max_length=254,null=True,blank=True)
    other_source=models.CharField(max_length=254,null=True,blank=True)
    revision_inf=models.CharField(max_length=254,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='wellloggings')

    class Meta:
        unique_together = (('log_from', 'waterpoint'),)
        ordering = ('log_from',)

    def __unicode__(self):
        return self.log_type
class lithologging(models.Model):
    depth_from = models.DateField()
    depth_to=models.DateField()
    description=models.CharField(max_length=254,null=True,blank=True)
    rock=models.CharField(max_length=254,null=True,blank=True)
    code = models.CharField(max_length=254, null=True,blank=True)
    age1 = models.CharField(max_length=254, null=True,blank=True)
    age2 = models.CharField(max_length=254, null=True,blank=True)
    age3 = models.CharField(max_length=254, null=True,blank=True)
    hydrocondition = models.CharField(max_length=254, null=True,blank=True)
    hydromedia = models.CharField(max_length=254, null=True,blank=True)
    aquifertype = models.CharField(max_length=254, null=True,blank=True)
    sgwl = models.FloatField( null=True,blank=True)
    data_source=models.CharField(max_length=254,null=True,blank=True)
    other_source=models.CharField(max_length=254,null=True,blank=True)
    revision_inf=models.CharField(max_length=254,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='lithologgings')

    class Meta:
        unique_together = (('depth_from', 'waterpoint'),)
        ordering = ('-depth_from',)

    def __unicode__(self):
        return self.rock
class loggingdata(models.Model):
    logdata_type = models.CharField(max_length=40,null=True,blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    value= models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    data_source = models.CharField(max_length=50,null=True,blank=True)
    other_source = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='loggingdatas')
    def __unicode__(self):
        return self.logdata_type
class log_plot(models.Model):
    old_id = models.CharField(max_length=40,null=True,blank=True)
    log_design = models.CharField(max_length=254,null=True,blank=True)
    log_description = models.CharField(max_length=254,null=True,blank=True)
    log_inf = models.CharField(max_length=254,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='log_plots')
    def __unicode__(self):
        return self.log_design
class drilling(models.Model):
    drilling_from = models.DateField()
    drilling_to = models.DateField()
    drilling_diameter = models.FloatField(null=True,blank=True)
    drilling_layer = models.CharField(max_length=254,null=True,blank=True)
    data_source = models.CharField(max_length=50,null=True,blank=True)
    other_source = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='drillings')
    class Meta:
        unique_together = (('drilling_from', 'waterpoint'),)
        ordering = ('drilling_from',)
    def __unicode__(self):
        return self.drilling_layer
class casing(models.Model):
    casing_from = models.DateField()
    casing_to = models.DateField()
    casing_diameter = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    casing_type = models.CharField(max_length=254,null=True,blank=True)
    data_source = models.CharField(max_length=50,null=True,blank=True)
    other_source = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='casings')
    class Meta:
        unique_together = (('casing_from', 'waterpoint'),)
        ordering = ('casing_from',)
    def __unicode__(self):
        return self.casing_type
class packing(models.Model):
    packing_from = models.DateField()
    packing_to = models.DateField()
    packing_layer = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Well, on_delete=models.CASCADE, related_name='packings')
    class Meta:
        unique_together = (('packing_from', 'waterpoint'),)
        ordering = ('-packing_from',)
    def __unicode__(self):
        return self.packing_layer

