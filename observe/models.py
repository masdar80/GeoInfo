from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

from django.contrib.gis.db import models
class Waterpoint(models.Model):
    waterfacilitypoint_id = models.CharField(max_length=254)
    city = models.CharField(max_length=254, blank=True)
    agency = models.CharField(max_length=254, blank=True)
    gov = models.CharField(max_length=254, blank=True)
    type = models.CharField(max_length=254, blank=True)
    town = models.CharField(max_length=254, blank=True)
    site = models.CharField(max_length=254, blank=True)
    village = models.CharField(max_length=254, blank=True)
    basin = models.CharField(max_length=254, blank=True)
    coordinate_x = models.FloatField(null=True)
    coordinate_y = models.FloatField(null=True)
    coordinate_z = models.CharField(max_length=254, blank=True)
    w84_lon_deg = models.FloatField(null=True)
    w84_lon_min = models.FloatField(null=True)
    w84_lon_sec = models.CharField(max_length=254, blank=True)
    w84_utm_zone = models.CharField(max_length=254, blank=True)
    w84_utm_x = models.FloatField(null=True)
    w84_utm_y = models.FloatField(null=True)
    w84_utm_z = models.FloatField(null=True)
    remarks=  models.CharField(max_length=254, blank=True)
    geom = models.MultiPointField(srid=4326)
    def __unicode__(self):
        return self.id_field

    def __str__(self):
        return self.type
    def get_absolute_url(self):
        return reverse('waterpoints',args=[])

#############start waters ###########

class waterchemistrysurvey_station(models.Model):
    id_pk = models.CharField(max_length=254, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    english_name=models.CharField(max_length=254,null=True,blank=True)
    arabic_name=models.CharField(max_length=254,null=True,blank=True)
    sourcetype=models.CharField(max_length=254,null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)
    sourcetype = models.CharField(max_length=254, null=True,blank=True)
    owner = models.CharField(max_length=254, null=True,blank=True)
    agency = models.CharField(max_length=254, null=True,blank=True)
    mohafaza = models.CharField(max_length=254, null=True,blank=True)
    montika = models.CharField(max_length=254, null=True,blank=True)
    nahia = models.CharField(max_length=254, null=True,blank=True)
    village = models.CharField(max_length=254, null=True,blank=True)
    sub_basin = models.CharField(max_length=254, null=True,blank=True)
    w84_lon_deg = models.FloatField( null=True,blank=True)
    w84_lon_min = models.FloatField( null=True,blank=True)
    w84_lon_sec = models.FloatField( null=True,blank=True)
    w84_lat_deg  = models.FloatField( null=True,blank=True)
    w84_lat_min   = models.FloatField( null=True,blank=True)
    w84_lat_sec= models.FloatField( null=True,blank=True)
    w84_utm_x   = models.FloatField( null=True,blank=True)
    w84_utm_y    = models.FloatField( null=True,blank=True)
    w84_utm_z    = models.FloatField( null=True,blank=True)
    w84_utm_zone= models.CharField(max_length=254,null=True,blank=True)
    stm_x   = models.CharField(max_length=254, null=True,blank=True)
    stm_y   = models.CharField(max_length=254, null=True,blank=True)
    stm_z   = models.CharField(max_length=254, null=True,blank=True)
    geom = models.MultiPointField(srid=4326)

    def __unicode__(self):
            return self.arabic_name
    def get_absolute_url(self):
        return reverse('stations',args=[])

class watersampling(models.Model):
    date=models.DateField()
    sample_id = models.CharField(max_length=254, primary_key=True)

    sample_datetime=models.DateField(null=True,blank=True)
    taste_datetime = models.DateField(null=True,blank=True)
    analysis_type = models.CharField(max_length=254, null=True,blank=True)
    laboratory_name = models.CharField(max_length=254, null=True,blank=True)
    remarks = models.CharField(max_length=254, null=True,blank=True)
    waterchemistrysurvey_station = models.ForeignKey(waterchemistrysurvey_station, on_delete=models.CASCADE, related_name='watersamplings')
    class Meta:
        unique_together = (('date', 'sample_id'),)
        ordering = ('-date',)
class fieldparameter(models.Model):
    date=models.DateField()
    temperature_c=models.CharField(max_length=254,null=True,blank=True)
    do_mg_l=models.FloatField(null=True,blank=True)
    ph=models.FloatField(null=True,blank=True)
    do_per_cent = models.FloatField(null=True,blank=True)
    cond_ms_cm = models.FloatField(max_length=254, null=True,blank=True)
    turbidity_ntu = models.CharField(max_length=254, null=True,blank=True)
    smell = models.CharField(max_length=254, null=True,blank=True)
    color = models.CharField(max_length=254, null=True,blank=True)
    taste = models.CharField(max_length=254, null=True,blank=True)
    flow_rate = models.CharField(max_length=254, null=True,blank=True)
    redox = models.CharField(max_length=254, null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='fieldparameters')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class eutrophication2(models.Model):
    date = models.DateField()
    bod_mg_l = models.CharField(max_length=254, null=True,blank=True)
    cod_mg_l = models.CharField(max_length=254, null=True,blank=True)
    do_mg_l = models.CharField(max_length=254, null=True,blank=True)
    ss = models.CharField(max_length=254, null=True,blank=True)
    ph = models.CharField(max_length=254, null=True,blank=True)
    ec = models.CharField(max_length=254, null=True,blank=True)
    alkalinity = models.CharField(max_length=254, null=True,blank=True)
    nh3_mg_l = models.CharField(max_length=254, null=True,blank=True)
    nh4_mg_l = models.CharField(max_length=254, null=True,blank=True)
    po4 = models.CharField(max_length=254, null=True,blank=True)
    no2 = models.CharField(max_length=254, null=True,blank=True)
    oil = models.CharField(max_length=254, null=True,blank=True)
    t_n = models.CharField(max_length=254, null=True,blank=True)
    t_p = models.CharField(max_length=254, null=True,blank=True)
    toc = models.CharField(max_length=254, null=True,blank=True)
    si = models.CharField(max_length=254, null=True,blank=True)
    h2s = models.CharField(max_length=254, null=True,blank=True)
    remarks = models.CharField(max_length=254, null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='eutrophication2s')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class heavymetals_rareelement(models.Model):
    date = models.DateField()
    Cd = models.CharField(max_length=254, null=True,blank=True)
    Pb = models.CharField(max_length=254, null=True,blank=True)
    Cu = models.CharField(max_length=254, null=True,blank=True)
    Cr = models.CharField(max_length=254, null=True,blank=True)
    Ni = models.CharField(max_length=254, null=True,blank=True)
    Mn = models.CharField(max_length=254, null=True,blank=True)
    Fe = models.CharField(max_length=254, null=True,blank=True)
    Al = models.CharField(max_length=254, null=True,blank=True)
    Zn = models.CharField(max_length=254,null=True,blank=True)
    AS = models.CharField(max_length=254, null=True,blank=True)
    Be = models.CharField(max_length=254,null=True,blank=True)
    cn = models.CharField(max_length=254, null=True,blank=True)
    Li = models.CharField(max_length=254,null=True,blank=True)
    Hg = models.CharField(max_length=254, null=True,blank=True)
    Mo = models.CharField(max_length=254, null=True,blank=True)
    Se = models.CharField(max_length=254,null=True,blank=True)
    Ba = models.CharField(max_length=254, null=True,blank=True)
    Ag = models.CharField(max_length=254, null=True,blank=True)
    units = models.CharField(max_length=254, null=True,blank=True)
    remarks = models.CharField(max_length=254, null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='heavymetals_rareelements')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class hydrochemical(models.Model):
    date = models.DateField()
    hard_total_mg_l = models.FloatField( null=True,blank=True)
    hard_lime_mg_l = models.FloatField( null=True,blank=True)
    hard_mag_mg_l = models.FloatField( null=True,blank=True)
    tds_mg_l = models.FloatField( null=True,blank=True)
    ca_mg_l = models.FloatField(null=True,blank=True)
    mg_mg_l = models.FloatField( null=True,blank=True)
    na_mg_l = models.FloatField( null=True,blank=True)
    k_mg_l = models.FloatField( null=True,blank=True)
    so4_mg_l = models.FloatField(null=True,blank=True)
    free_cl_mg_l = models.FloatField( null=True,blank=True)
    cl_mg_l = models.FloatField( null=True,blank=True)
    hco3_mg_l = models.FloatField(null=True,blank=True)
    co3_mg_l = models.FloatField( null=True,blank=True)
    o18_mg_l = models.FloatField( null=True,blank=True)
    h2_mg_l = models.FloatField(null=True,blank=True)
    he_mg_l = models.FloatField( null=True,blank=True)
    h3_mg_l = models.FloatField( null=True,blank=True)
    c14_mg_l = models.FloatField( null=True,blank=True)
    ra_mg_l = models.FloatField( null=True,blank=True)
    estemated_waterage = models.CharField(max_length=254, null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='hydrochemicals')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class toxic_substances(models.Model):
    date = models.DateField()
    phenol = models.FloatField( null=True,blank=True)
    benzen = models.FloatField( null=True,blank=True)
    mbas = models.FloatField(null=True,blank=True)
    b = models.FloatField(null=True,blank=True)
    f = models.FloatField(null=True,blank=True)
    bhc_a = models.FloatField( null=True,blank=True)
    bhc_b = models.FloatField( null=True,blank=True)
    abs = models.FloatField(null=True,blank=True)
    aox = models.FloatField(null=True,blank=True)
    pcb = models.FloatField(null=True,blank=True)
    dioxin = models.FloatField( null=True,blank=True)
    chlorodan_a = models.FloatField(null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='toxic_substancess')

    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class othercommon_parameters(models.Model):
    date = models.DateField()
    tss_mg_l = models.FloatField( null=True)
    p_mg_l = models.FloatField( null=True,blank=True)
    s_mg_l = models.FloatField( null=True,blank=True)
    u_mg_l = models.FloatField( null=True,blank=True)
    sr_mg_l = models.FloatField( null=True,blank=True)
    co_mg_l = models.FloatField( null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='othercommon_parameterss')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)
class biological(models.Model):
    date = models.DateField()
    coliform_t7a_100ml = models.CharField(max_length=254,null=True,blank=True)
    sodmons_t7a_100ml = models.CharField(max_length=254, null=True,blank=True)
    bsodomonas_t7a_24hour = models.CharField(max_length=254,null=True,blank=True)
    bacteria = models.CharField(max_length=254,null=True,blank=True)
    ferments_number = models.CharField(max_length=254,null=True,blank=True)
    helmenth_eggs = models.CharField(max_length=254,null=True,blank=True)
    watersampling = models.ForeignKey(watersampling, on_delete=models.CASCADE, related_name='biologicals')
    class Meta:
        unique_together = (('date', 'id'),)
        ordering = ('-date',)

##################start pumping############

class pumping(models.Model):
    pmp_pumpdepth=models.FloatField(null=True,blank=True)
    pmp_startdatetime=models.DateField(null=True,blank=True)
    pmp_enddatetime = models.DateField(null=True,blank=True)
    pmp_time=models.DateTimeField()
    pmp_discharge=models.FloatField(null=True,blank=True)
    pmp_pumptype= models.CharField(max_length=254,null=True,blank=True)
    pmp_generatortype= models.CharField(max_length=254,null=True,blank=True)
    pmp_dischargemethod= models.CharField(max_length=254,null=True,blank=True)
    pmp_capacitydevice= models.CharField(max_length=254,null=True,blank=True)
    pmp_manometertype= models.CharField(max_length=254,null=True,blank=True)
    waterpoint  = models.ForeignKey(Waterpoint, on_delete=models.CASCADE, related_name='pumpings')

class pumptest_obswell(models.Model):
    pto_depth = models.FloatField(null=True,blank=True)
    pto_diameter = models.FloatField(null=True,blank=True)
    pto_swl = models.FloatField(null=True,blank=True)
    pto_distance = models.FloatField(null=True,blank=True)
    pto_reflevel = models.FloatField(null=True,blank=True)
    pumping = models.ForeignKey(pumping, on_delete=models.CASCADE, related_name='pumptest_obswells')

    def __unicode__(self):
        return self.pto_reflevel
    ##############3

class pumptest_pumpwell(models.Model):
    pumptest_interval_from = models.DateField(null=True,blank=True)
    pumptest_interval_to = models.DateField(null=True,blank=True)
    pumptest_swl = models.FloatField(null=True,blank=True)
    pumptest_diameter = models.FloatField(null=True,blank=True)
    pumping = models.ForeignKey(pumping, on_delete=models.CASCADE, related_name='pumptest_pumpwells')
    class Meta:
        unique_together = (('pumptest_interval_from', 'id'),)
        ordering = ('-pumptest_interval_from',)
    def __unicode__(self):
        return self.pumptest_swl

class step_drawdown(models.Model):
    sdd_datetime =models.DateField()
    sdd_accumulatetime = models.DateField(null=True,blank=True)
    pumptest_interval_to = models.FloatField(null=True,blank=True)
    sdd_discharge = models.FloatField(null=True,blank=True)
    sdd_waterdepth = models.FloatField(null=True,blank=True)
    sdd_drawdown = models.FloatField(null=True,blank=True)
    pumping = models.ForeignKey(pumping, on_delete=models.CASCADE, related_name='step_drawdowns')

    class Meta:
        unique_together = (('sdd_datetime', 'id'),)
        ordering = ('-sdd_datetime',)

    def __unicode__(self):
        return self.pumptest_interval_to

class continious_dischage(models.Model):
    cds_date = models.DateField()
    cds_accumulate = models.FloatField(null=True,blank=True)
    cds_depth = models.FloatField(null=True,blank=True)
    cds_time = models.FloatField(null=True,blank=True)
    cds_drawdown = models.FloatField(null=True,blank=True)
    pumping = models.ForeignKey(pumping, on_delete=models.CASCADE, related_name='continious_dischages')
    class Meta:
        unique_together = (('cds_date', 'id'),)
        ordering = ('-cds_date',)

    def __unicode__(self):
        return self.pumptest_interval_to

class recovery_test(models.Model):
    rct_datetime = models.DateField()
    rct_waterdepth = models.FloatField(null=True,blank=True)
    rct_drawdown = models.FloatField(null=True,blank=True)
    pumping = models.ForeignKey(pumping, on_delete=models.CASCADE, related_name='recovery_tests')
    class Meta:
        unique_together = (('rct_datetime', 'id'),)
        ordering = ('-rct_datetime',)
    def __unicode__(self):
            return self.rct_waterdepth
###############start geophisics

class geophysicalproject(models.Model):
    gpp_name=models.CharField(max_length=254,null=True,blank=True)
    gpp_owner=models.CharField(max_length=254,null=True,blank=True)
    gpp_type=models.CharField(max_length=254,null=True,blank=True)
    gpp_startdate=models.DateField(null=True)

    def __unicode__(self):
        return self.gpp_name

class geophysicalsurvey(models.Model):
    gps_datetime = models.DateField(null=True)
    gps_method = models.CharField(max_length=254,null=True,blank=True)
    spec_obs_equipment= models.CharField(max_length=254,null=True,blank=True)
    gps_surveyor=models.CharField(max_length=254,null=True,blank=True)
    geophysicalproject = models.ForeignKey(geophysicalproject, on_delete=models.CASCADE, related_name='geophysicalsurveys')
    def __unicode__(self):
        return self.spec_obs_equipment

class vertical_electric_sounding(models.Model):
    ves_pointname = models.CharField(max_length=254,null=True,blank=True)
    ves_configuaration = models.CharField(max_length=254, null=True,blank=True)
    ves_linedirection = models.CharField(max_length=254,null=True,blank=True)
    ves_coordinatex = models.FloatField(null=True,blank=True)
    ves_coordinatey=models.FloatField(null=True,blank=True)
    ves_coordinatez=models.FloatField(null=True,blank=True)
    geophysicalsurvey = models.ForeignKey(geophysicalsurvey, on_delete=models.CASCADE,
                                           related_name='vertical_electric_soundings')

class ves_result_ap(models.Model):
    ves_data_point = models.CharField(max_length=254, null=True,blank=True)
    vdt_depth=models.FloatField(null=True,blank=True)
    vdt_sresistivity=models.FloatField(null=True,blank=True)
    vertical_electric_sounding = models.ForeignKey(vertical_electric_sounding, on_delete=models.CASCADE, related_name='ves_result_aps')

class ves_result_sp(models.Model):
    vdt_point = models.CharField(max_length=254,null=True,blank=True)
    vdt_depth=models.FloatField(null=True,blank=True)
    vdt_sresistivity=models.FloatField(null=True,blank=True)
    vertical_electric_sounding = models.ForeignKey(vertical_electric_sounding, on_delete=models.CASCADE, related_name='ves_result_sps')
class profiling_electric_sounding_re(models.Model):
    gps_datetime = models.DateField(null=True,blank=True)
    rpf_line = models.CharField(max_length=254,null=True,blank=True)
    rpf_startx= models.FloatField(null=True,blank=True)
    rpf_starty = models.FloatField(null=True,blank=True)
    rpf_startz = models.FloatField(null=True,blank=True)
    rpf_endx = models.FloatField(null=True,blank=True)
    rpf_endy = models.FloatField(null=True,blank=True)
    rpf_endz = models.FloatField(null=True,blank=True)
    rpf_length = models.FloatField(null=True,blank=True)
    gps_surveyor=models.CharField(max_length=254,null=True,blank=True)
    geophysicalsurvey = models.ForeignKey(geophysicalsurvey, on_delete=models.CASCADE, related_name='profiling_electric_sounding_re')
    def __unicode__(self):
        return self.spec_obs_equipment

class profiling_electric_sounding_da(models.Model):
    rpd_datax = models.FloatField(null=True,blank=True)
    rpd_datay = models.FloatField(null=True,blank=True)
    rpd_datay= models.FloatField(null=True,blank=True)
    profiling_electric_sounding_re = models.ForeignKey(profiling_electric_sounding_re, on_delete=models.CASCADE, related_name='profiling_electric_sounding_das')
    def __unicode__(self):
        return self.rpd_datax


