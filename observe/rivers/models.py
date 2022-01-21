from django.db import models
from django.urls import reverse
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager
from django.contrib.gis.db.models import Manager as GeoManager

from django.contrib.auth.models import User
from django.db.models.signals import post_save


class XY_River(models.Model):
    id_field = models.CharField(max_length=254,primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    old_id = models.CharField(max_length=254, blank=True,null=True)
    sitename_a = models.CharField(max_length=254, blank=True,null=True)
    sitename_e = models.CharField(max_length=254, blank=True,null=True)
    type = models.CharField(max_length=254, blank=True,null=True)
    agency = models.CharField(max_length=254, blank=True,null=True)
    mohafaza = models.CharField(max_length=254, blank=True,null=True)
    montika = models.CharField(max_length=254, blank=True,null=True)
    nahia = models.CharField(max_length=254, blank=True,null=True)
    village = models.CharField(max_length=254, blank=True,null=True)
    sub_baisn = models.CharField(max_length=254, blank=True,null=True)
    w84_utm_x = models.FloatField(blank=True,null=True)
    w84_utm_y = models.FloatField(null=True,blank=True)
    w84_utm_z = models.FloatField(null=True,blank=True)
    means_z = models.CharField(max_length=254, blank=True,null=True)
    data_sourc = models.CharField(max_length=254, blank=True,null=True)
    image = models.ImageField(default='default.jpg', upload_to='xy_river_pic')

    geom = models.MultiPointField(srid=4326)
    objects = GeoManager()

    def __unicode__(self):
        return self.id_field

    def __str__(self):
        return self.id_field

    def get_absolute_url(self):
        return reverse('xy_rivers', args=[])
class River_inf(models.Model):
    surveyer_name = models.CharField(max_length=254, null=True, blank=True)
    survey_date = models.DateField(null=True,blank=True)
    gps_number = models.CharField(max_length=50, null=True, blank=True)
    water_use = models.CharField(max_length=20, null=True, blank=True)
    open_date = models.DateField(null=True,blank=True)
    close_date = models.DateField(null=True,blank=True)
    channel_condition = models.CharField(max_length=254, null=True, blank=True)
    measurment_items = models.CharField(max_length=254, null=True, blank=True)
    labo_qual_analysis_frequency = models.CharField(max_length=254, null=True, blank=True)
    type_of_automatic_sensor = models.CharField(max_length=254, null=True, blank=True)
    station_condition = models.CharField(max_length=254, null=True, blank=True)
    equipped_with_stuff_gauge = models.CharField(max_length=254, null=True, blank=True)
    field_measur_freq_dryseason = models.CharField(max_length=254, null=True, blank=True)
    field_measur_freq_rainyseason = models.CharField(max_length=254, null=True, blank=True)
    measure_type_head = models.CharField(max_length=254, null=True, blank=True)
    measure_type_quality = models.CharField(max_length=254, null=True, blank=True)
    statuse_of_station = models.CharField(max_length=254, null=True, blank=True)
    improvement_point = models.CharField(max_length=254, null=True, blank=True)
    xy_river = models.OneToOneField(XY_River, on_delete=models.CASCADE, related_name='river_inf' )

    def __str__(self):
        return self.gps_number
def add_river_inf(sender, **kwarg):
    if kwarg['created']:
        xy_river_inf = River_inf.objects.create(xy_river=kwarg['instance'])
post_save.connect(add_river_inf, sender=XY_River)

class riverdischarge_anual(models.Model):
    obs_datetime = models.DateField()
    anual_discharge = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='riverdischarge_anuals')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

class riverdischarge_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_avg_discharge = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    monthly_total_discharge = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    meas_method = models.CharField(max_length=250, blank=True,null=True)
    data_source = models.CharField(max_length=250, blank=True,null=True)
    other_source = models.CharField(max_length=250, blank=True,null=True)
    remarks = models.CharField(max_length=250, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='riverdischarge_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

class riverdischarge_daily(models.Model):
    obs_datetime = models.DateField()
    stage_m = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    rc_id = models.CharField(max_length=50, null=True, blank=True)
    discharge_m3_sec = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    meas_method = models.CharField(max_length=250, blank=True, null=True)
    data_source = models.CharField(max_length=250, blank=True, null=True)
    other_source = models.CharField(max_length=250, blank=True, null=True)
    remarks = models.CharField(max_length=250, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='riverdischarge_dailys')

    # objects = riverdischarge_dailyManager()
    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

class riverflowmeasure(models.Model):
    obs_datetime = models.DateField()
    station_area = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    avg_flow_velocity = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    calculated_flow_velocity =models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    section_id = models.CharField(max_length=50, blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    meas_method = models.CharField(max_length=50, blank=True,null=True)
    equipment_spec = models.CharField(max_length=50, blank=True,null=True)
    data_source = models.CharField(max_length=50, blank=True,null=True)
    other_source = models.CharField(max_length=50, blank=True,null=True)
    remarks = models.CharField(max_length=50,blank=True,null=True)
    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='riverflowmeasures')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

class surface_hq(models.Model):
    obs_datetime = models.DateField()
    h = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    q = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    section_width_m =models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    section_depth_m = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    section_area_m2 = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    velocity_m_s = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    meas_method = models.CharField(max_length=254, null=True,blank=True)
    remarks = models.CharField(max_length=254, null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='surface_hqs')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

class discharge_survey(models.Model):
    year = models.DateField()
    type_of_regression = models.CharField(max_length=50, null=True,blank=True)
    data_limit_up = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    data_limit_low =models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    formula = models.CharField(max_length=50, null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='discharge_surveys')

    class Meta:
        unique_together = (('year', 'waterpoint'),)
        ordering = ('year',)

    def __unicode__(self):
        return self.formula

class sectionareasurvey(models.Model):
    datetime = models.DateField()
    sas_area = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    sas_surveyer = models.CharField(max_length=254, null=True,blank=True)
    sas_method = models.CharField(max_length=254, null=True,blank=True)
    data_source = models.CharField(max_length=254, null=True,blank=True)
    other_source = models.CharField(max_length=254, null=True,blank=True)
    remarks = models.CharField(max_length=254, null=True,blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='sectionareasurveys')

    class Meta:
        unique_together = (('datetime', 'waterpoint'),)
        ordering = ('datetime',)

    def __unicode__(self):
        return self.remarks


class sectiondata(models.Model):
    sec_datetime = models.DateField()
    sec_stano = models.CharField(max_length=254,blank=True,null=True)
    sec_x = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    sec_y = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_River, on_delete=models.CASCADE, related_name='sectiondatas')
    class Meta:
        unique_together = (('sec_datetime', 'waterpoint'),)
        ordering = ('sec_datetime',)

    def __unicode__(self):
        return self.sec_stano
