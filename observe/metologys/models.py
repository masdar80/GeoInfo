from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


class XY_Metology(models.Model):
    id_field = models.CharField(max_length=254, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    old_id = models.CharField(max_length=254, null=True, blank=True)
    sitename_a = models.CharField(max_length=254, null=True, blank=True)
    sitename_e = models.CharField(max_length=254, null=True, blank=True)
    type = models.CharField(max_length=254, null=True, blank=True)
    agency = models.CharField(max_length=254, null=True, blank=True)
    mohafaza = models.CharField(max_length=254, null=True, blank=True)
    mohafaza_en = models.CharField(max_length=254, null=True, blank=True)
    montika = models.CharField(max_length=254, null=True, blank=True)
    nahia = models.CharField(max_length=254, null=True, blank=True)
    village = models.CharField(max_length=254, null=True, blank=True)
    sub_baisn = models.CharField(max_length=254, null=True, blank=True)

    w84_utm_x = models.FloatField(null=True, blank=True)
    w84_utm_y = models.FloatField(null=True, blank=True)
    w84_utm_z = models.FloatField(null=True, blank=True)
    means_z = models.CharField(max_length=254, null=True, blank=True)
    
    data_sourc = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='xy_metology_pic',blank=True,null=True)
    geom = models.PointField(srid=4326)

    def __unicode__(self):
        return self.id_field

    def get_absolute_url(self):
        return reverse('xy_metologys', args=[])


class Metology_inf(models.Model):
    surveyer_name = models.CharField(max_length=254, blank=True)
    survey_date = models.DateField(null=True, blank=True)
    gps_number = models.IntegerField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    present_condition = models.CharField(max_length=254, blank=True, null=True)
    obs_item = models.CharField(max_length=254, blank=True, null=True)
    meas_frequency = models.CharField(max_length=254, blank=True, null=True)
    meas_type = models.CharField(max_length=254, blank=True, null=True)
    condition_of_station = models.CharField(max_length=254, blank=True)
    improvement_point = models.CharField(max_length=254, blank=True, null=True)
    xy_metology = models.OneToOneField(XY_Metology, on_delete=models.CASCADE, related_name='metology_inf')

    def __unicode__(self):
        return self.surveyer_name


def add_metology_inf(sender, **kwarg):
    if kwarg['created']:
        xy_metology_inf = Metology_inf.objects.create(xy_metology=kwarg['instance'])


post_save.connect(add_metology_inf, sender=XY_Metology)


class airpressure(models.Model):
    obs_datetime = models.DateField()
    daily_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='airpressures')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.daily_avg


class evaporation_daily(models.Model):
    obs_date = models.DateField()
    evap_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='evaporation_dailys')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.evap_mm


class evaporation_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_evap_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='evaporation_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.monthly_evap_avg


class humidity_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    avg_hum_from_daily = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='humidity_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class humidity_daily(models.Model):
    obs_date = models.DateField()
    daily_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_time = models.CharField(max_length=255, blank=True, null=True)
    min_time = models.CharField(max_length=255, blank=True, null=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='humidity_dailys')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.daily_max


class temperature_daily(models.Model):
    obs_date = models.DateField()
    daily_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_time = models.IntegerField(blank=True, null=True)
    min_time = models.IntegerField(blank=True, null=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='temperature_dailys')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.daily_min


class temperature_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    avg_temp_from_daily = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='temperature_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class precipitation_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_precipitaion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    calculated_value = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='precipitation_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class precipitation_annual(models.Model):
    year = models.CharField(max_length=50,null=False,blank=False)
    annual_precipitation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    annual_avg_precipitation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='precipitation_annuals')

    class Meta:
        unique_together = (('waterpoint','year'),)

    def __unicode__(self):
        return self.remarks


class precipitation_daily(models.Model):
    obs_date = models.DateField()
    prcp_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    data_source = models.CharField(max_length=254, blank=True, null=True)
    other_source = models.CharField(max_length=254, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='precipitation_dailys')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.remarks


class wind_daily(models.Model):
    obs_datetime = models.DateField()
    daily_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    data_source = models.CharField(max_length=254, blank=True)
    other_source = models.CharField(max_length=254, blank=True)
    remarks = models.CharField(max_length=254, blank=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='wind_dailys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class wind_monthly(models.Model):
    obs_datetime = models.DateField()
    avg_monthly_wind_from_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='wind_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks

    meas_method = models.CharField(max_length=254)


class sunshine_daily(models.Model):
    obs_date = models.DateField()
    rad_mj_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rad_max_w_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_time = models.CharField(max_length=250, blank=True, null=True)
    duration_hr = models.CharField(max_length=250, blank=True, null=True)
    meas_method = models.CharField(max_length=250, blank=True, null=True)
    data_source = models.CharField(max_length=245, blank=True, null=True)
    other_source = models.CharField(max_length=245, blank=True, null=True)
    rad_avg_w_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rad_min_w_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=245, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='sunshine_dailys')

    class Meta:
        unique_together = (('obs_date', 'waterpoint'),)
        ordering = ('obs_date',)

    def __unicode__(self):
        return self.remarks


class snowdepth(models.Model):
    obs_datetime = models.DateField()
    dailysnowdepth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=50, blank=True, null=True)
    data_source = models.CharField(max_length=245, blank=True, null=True)
    other_source = models.CharField(max_length=245, blank=True, null=True)
    remarks = models.CharField(max_length=245, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='snowdepths')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class snowfall(models.Model):
    obs_datetime = models.DateField()
    dailysnowfall = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meas_method = models.CharField(max_length=50, blank=True, null=True)
    data_source = models.CharField(max_length=245, blank=True, null=True)
    other_source = models.CharField(max_length=245, blank=True, null=True)
    remarks = models.CharField(max_length=245, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Metology, on_delete=models.CASCADE, related_name='snowfalls')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks
