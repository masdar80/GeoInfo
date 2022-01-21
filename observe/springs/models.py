from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class XY_Spring(models.Model):
    id_field = models.CharField(max_length=254,primary_key=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.jpg',upload_to='xy_spring_pic')

    geom = models.MultiPointField(srid=4326)

    def __unicode__(self):
        return self.id_field

    def __str__(self):
        return self.id_field
    def get_absolute_url(self):
        return reverse('xy_springs',args=[])

class Spring_inf(models.Model):
    surveyer_name = models.CharField(max_length=254,null=True,blank=True)
    survey_date = models.DateField(null=True,blank=True)
    gps_number = models.CharField(max_length=50,null=True,blank=True)
    water_use = models.CharField(max_length=20,null=True,blank=True)
    open_date = models.DateField(null=True,blank=True)
    close_date=models.DateField(null=True,blank=True)
    present_spring_statuse=models.CharField(max_length=254,null=True,blank=True)
    spring_ownership = models.CharField(max_length=254,null=True,blank=True)
    measurment_items=models.CharField(max_length=254,null=True,blank=True)
    labo_qual_analysis_frequency=models.CharField(max_length=254,null=True,blank=True)
    type_of_automatic_sensor=models.CharField(max_length=254,null=True,blank=True)
    equipped_with_stuff_gauge=models.CharField(max_length=254,null=True,blank=True)
    field_measur_freq_dryseason =models.CharField(max_length=254,null=True,blank=True)
    field_measur_freq_rainyseason=models.CharField(max_length=254,null=True,blank=True)
    measure_type_head=models.CharField(max_length=254,null=True,blank=True)
    measure_type_quality=models.CharField(max_length=254,null=True,blank=True)
    aquifer_litho_code =models.CharField(max_length=254,null=True,blank=True)
    condition_of_station=models.CharField(max_length=254,null=True,blank=True)
    improvement_point=models.CharField(max_length=254,null=True,blank=True)
    xy_spring = models.OneToOneField(XY_Spring, on_delete=models.CASCADE,related_name = 'spring_inf',)

    def __str__(self):
        return self.gps_number

def add_spring_inf(sender,**kwarg):
    if kwarg['created']:
        xy_spring_inf = Spring_inf.objects.create(xy_spring= kwarg['instance'])
post_save.connect(add_spring_inf,sender=XY_Spring)

class springdischarge_anual(models.Model):
    obs_datetime = models.CharField(max_length=10,null=False,blank=False)
    anual_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    waterpoint = models.ForeignKey(XY_Spring, on_delete=models.CASCADE, related_name='springdischarge_anuals')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)

    def __unicode__(self):
        return self.remarks
class springdischarge_avg_anual(models.Model):
    obs_datetime = models.DateField()
    avg_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    max_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    min_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    remarks = models.CharField(max_length=50,null=True,blank=True)
    waterpoint = models.ForeignKey(XY_Spring, on_delete=models.CASCADE, related_name='springdischarge_avg_anuals')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
        return self.remarks


class springdischarge_monthly(models.Model):
    obs_datetime = models.DateField()
    monthly_avg_discharge = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    monthly_total = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    meas_method = models.CharField(max_length=250,blank=True,null=True)
    data_source = models.CharField(max_length=250,blank=True,null=True)
    other_source = models.CharField(max_length=250,blank=True,null=True)
    remarks = models.CharField(max_length=250,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Spring, on_delete=models.CASCADE,related_name='springdischarge_monthlys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
         return self.remarks
class springdischarge_avg_monthly(models.Model):
    month = models.CharField(max_length=5,null=False,blank=False)
    avg_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    max_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    min_discharge = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    remarks = models.CharField(max_length=20,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Spring, on_delete=models.CASCADE, related_name='springdischarge_avg_monthlys')

    class Meta:
        unique_together = (('month', 'waterpoint'),)

    def __unicode__(self):
        return self.remarks
class springdischarge_daily(models.Model):
    obs_datetime = models.DateField()
    stage_m = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    rc_id = models.CharField(max_length=50,null=True,blank=True)
    discharge_m3_sec = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    meas_method = models.CharField(max_length=50,blank=True,null=True)
    data_source = models.CharField(max_length=50,blank=True,null=True)
    other_source = models.CharField(max_length=50,blank=True,null=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    waterpoint = models.ForeignKey(XY_Spring, on_delete=models.CASCADE,related_name='springdischarge_dailys')

    class Meta:
        unique_together = (('obs_datetime', 'waterpoint'),)
        ordering = ('obs_datetime',)

    def __unicode__(self):
         return self.remarks

