from django.urls import path
from observe.rivers import views
from observe.wells.views import all_xy_wells
from observe.springs.views import all_xy_springs
from observe.metologys.views import all_xy_metologys,generate_pdf

from observe.rivers.views import (
    RiverListView, RiverCreate, RiverUpdate, RiverDelete,export_filtered_rivers_csv,
    river_inf_update_form,export_filtered_rivers_xls
)
from observe.wells.views import (
    WellListView, WellCreate, WellUpdate, WellDelete,export_filtered_wells_csv,export_filtered_wells_xls
)
from observe.springs.views import (
    SpringListView, SpringCreate, SpringUpdate,
    SpringDelete,export_filtered_springs_csv,export_filtered_springs_xls,import_spring_readings
)
from observe.metologys.views import (
    MetologyListView, MetologyCreate, MetologyUpdate, MetologyDelete,export_filtered_metologys_csv,
    export_filtered_metologys_xls,metology_inf_update_form
)
from observe.waters.views import waterchemistrysurvey_stationCreate,waterchemistrysurvey_stationDelete,\
    waterchemistrysurvey_stationListView,waterchemistrysurvey_stationUpdate,all_waterchemistrysurvey_station,\
    watersample_delete,watersample_list,watersample_form,fieldparameter_form,fieldparameter_delete,fieldparameter_list,\
eutrophication2_form,eutrophication2_delete,eutrophication2_list,heavymetals_rareelement_form,heavymetals_rareelement_list,\
    heavymetals_rareelement_delete,hydrochemical_list,hydrochemical_form,hydrochemical_delete,toxic_substances_delete,\
    toxic_substances_form,toxic_substances_list,othercommon_parameters_delete,othercommon_parameters_form,othercommon_parameters_list
from observe.pumpings.views import continious_dischage_list, continious_dischage_delete,continious_dischage_form,step_drawdown_form,step_drawdown_list,\
    step_drawdown_delete,    pumptest_obswell_delete,pumptest_obswell_form,pumping_pmp_form,\
    pumping_pmp_delete,pumptest_obswell_list,pumping_pmp_list,WaterpointCreate,WaterpointDelete,WaterpointListView,\
    WaterpointUpdate,all_waterpoint_pump,pumptest_pumpwell_delete, \
    pumptest_pumpwell_form, pumptest_pumpwell_list,recovery_test_delete,\
    recovery_test_form,recovery_test_list


from observe.rivers.views import  HomePageView,export_discharge_survey,river_rss_Pdf,river_rsd_Pdf,river_rds_up_Pdf,river_rds_low_Pdf,river_rfm_Pdf,\
    river_rdd_Pdf,river_rdm_Pdf,river_rda_Pdf,river_rsd_create_form,river_rsd_update_form,river_rvelocity_Pdf,river_rh_Pdf,river_rq_Pdf,\
river_rdd_list,river_rdd_create_form,river_rdd_update_form,river_rdd_delete,river_rdm_list,river_rdm_create_form,river_rdm_update_form,river_rdm_delete,river_rda_list,river_rda_create_form,river_rda_update_form,river_rda_delete,\
river_rhq_list,river_rhq_create_form,river_rhq_update_form,river_rhq_delete, river_rfm_list,river_rfm_create_form,river_rfm_update_form,river_rfm_delete,river_rds_list,river_rds_create_form,river_rds_update_form,river_rds_delete,\
river_rss_list,river_rss_create_form,river_rss_update_form,river_rss_delete,\
export_discharge_survey,export_river_discharge_annual,river_rdd_multi_delete,river_sectiondata_multi_delete,\
river_sectionareasurvey_multi_delete,river_discharge_monthly_multi_delete,riverdischarge_anuall_multi_delete,\
riverflowmessure_multi_delete,river_surface_hq_multi_delete,river_discharge_survey_multi_delete,\
export_river_discharge_monthly,import_river_readings,export_riverflowmeasure,export_sectionareasurvey,export_sectiondata,export_surface_hq,river_rsd_delete,river_rsd_list
from observe.springs.views import spring_sda_create_form,spring_sda_update_form,spring_sda_list,spring_sda_delete,spring_sdaa_delete,spring_sdam_create_form,spring_sdam_update_form,\
    spring_sdaa_create_form,spring_sdaa_update_form,spring_sdam_list,spring_sdaa_list,spring_sdam_delete,spring_sdd_delete,spring_sdm_delete,spring_sdd_create_form,spring_sdd_update_form\
    ,spring_sdd_list,spring_sdm_list,spring_sdm_create_form,spring_sdm_update_form,export_spring_discharge_anually,export_spring_discharge_avg_anually,export_spring_discharge_avg_monthly,\
    export_spring_discharge_daily,export_spring_discharge_monthly,spring_sdaa_Pdf,spring_sda_Pdf,\
    spring_sdam_Pdf,spring_sdd_Pdf,spring_sdm_Pdf,spring_inf_update_form,spring_sdm_multi_delete,spring_sdd_multi_delete,\
spring_sdam_multi_delete,spring_sdaa_multi_delete,spring_sda_multi_delete,spring_sdaa_multi_delete
from observe.metologys.views import metology_air_delete,metology_air_create_form,metology_air_update_form,metology_air_list,metology_ed_delete,metology_ed_create_form,metology_ed_update_form,\
    metology_ed_list,metology_em_delete,metology_em_update_form,metology_em_create_form,metology_em_list,metology_hd_delete,metology_hd_update_form,metology_hd_create_form,metology_hd_list,metology_hm_delete\
    ,metology_hm_create_form,metology_hm_update_form,metology_hm_list,metology_pa_delete,metology_pm_update_form,metology_pa_create_form,metology_pa_update_form,metology_pa_list,metology_pd_delete,\
    metology_pd_create_form,metology_pd_update_form,metology_pd_list,td_min_Pdf,td_max_Pdf,td_avg_Pdf,tm_min_Pdf,tm_avg_Pdf,tm_max_Pdf,\
    metology_pm_delete,metology_pm_create_form,metology_pm_list,metology_sd_delete,metology_sd_create_form,metology_sd_update_form,metology_sd_list,metology_td_delete,metology_td_create_form,metology_td_update_form,\
    metology_td_list,metology_tm_delete,metology_tm_create_form,metology_tm_update_form,metology_tm_list,metology_wd_delete,metology_wd_update_form,metology_wd_create_form,metology_wd_list,metology_wm_delete,\
    metology_wm_create_form,metology_wm_update_form,metology_wm_list,export_evaporation_daily,export_airpressur,export_evaporation_monthly,export_humidity_daily,export_humidity_monthly,\
    export_temperature_monthly,export_temperature_daily,export_precipitation_annual,export_precipitation_daily,export_precipitation_monthly,export_sunshine_daily,\
    export_wind_daily,export_wind_monthly,air_avg_Pdf,air_max_Pdf,air_min_Pdf,report_xy_metologys,ed_Pdf,em_Pdf,hm_max_Pdf,hm_min_Pdf,hm_avg_Pdf,\
    hd_avg_Pdf,hd_min_Pdf,hd_max_Pdf,wd_avg_Pdf,wd_max_Pdf,wd_min_Pdf,wm_avg_Pdf,pd_Pdf,pa_Pdf,pm_Pdf,\
    sd_rad_max_Pdf,sd_rad_min_Pdf,sd_rad_mj_Pdf,metology_air_multi_delete,metology_ed_multi_delete,metology_em_multi_delete,\
metology_tm_multi_delete,metology_td_multi_delete,metology_wd_multi_delete,metology_wm_multi_delete,metology_pd_multi_delete,\
metology_pm_multi_delete,metology_hm_multi_delete,metology_hd_multi_delete,metology_sd_multi_delete,metology_pa_multi_delete,\
metology_snowfall_list,metology_snowfall_update_form,metology_snowfall_create_form,metology_snowfall_delete,export_snowfall,\
snowfall_Pdf,metology_snowdepth_list,metology_snowdepth_create_form,metology_snowdepth_update_form,metology_snowdepth_delete,\
export_snowdepth,snowdepth_Pdf,metology_snowfall_multi_delete,metology_snowdepth_multi_delete,import_metology_readings



from observe.wells.views import well_gwl_list,well_gwl_delete,well_gwl_create_form,well_gwl_update_form,well_gwlm_delete,well_gwlm_create_form,well_gwlm_update_form,well_gwlm_list,\
    well_agw_delete,well_agw_create_form,well_agw_update_form,well_agw_list,well_wq_create_form,well_wq_update_form,well_wq_list,well_wq_delete,well_wtl_create_form,\
    well_wtl_update_form,well_wtl_delete,well_wtl_list,well_gwl_Pdf,well_gwlm_Pdf,well_wq_ph_Pdf,well_wq_ec_ms_Pdf,well_wtl_Pdf,well_inf_update_form,\
    well_drill_delete,well_drill_create_form,well_drill_update_form,well_drill_list,export_drilling,export_casing,export_lithologging,export_packing,export_well_auto_groundwater,export_well_groundwaterlevel_manuals,\
    export_well_groundwaterlevels,export_welllogging,export_welltoplevel,export_wells_quality,well_casing_delete,well_casing_create_form,well_casing_update_form,well_casing_list,\
    well_packing_delete,well_packing_create_form,well_packing_update_form,well_packing_list,well_wl_create_form,well_wl_update_form,well_wl_list,well_wl_delete,well_ll_create_form,\
    well_ll_update_form,well_ll_delete,well_ll_list,well_drill_Pdf,well_casing_Pdf,well_packing_Pdf,well_packing_create_form,well_packing_update_form,\
    well_ld_delete,well_ld_create_form,well_ld_update_form,well_ld_list,well_lp_delete,well_lp_create_form,well_lp_update_form,well_lp_list,well_agw_level_Pdf,\
    well_agw_depth_Pdf,well_gwd_Pdf,well_log_pdf,well_ll_Pdf,import_well_readings,well_ll_multi_delete,\
well_drill_multi_delete,well_packing_multi_delete,well_casing_multi_delete,well_gwl_multi_delete,well_gwlm_multi_delete,\
well_agw_multi_delete,well_wq_multi_delete,well_wtl_multi_delete,well_wl_multi_delete



from django.conf.urls.static import static
from django.conf import settings


urlpatterns =   [
    #########river#########
    path('river/<id_field>/riverinf_update/', river_inf_update_form, name='riverinf-update'),
    path('river/<id_field>/rdd-form/', river_rdd_create_form, name='rdd-form-insert'),
    path('river/<id_field>/rdd-list/', river_rdd_list, name='rdd-list'),
    path('river/<id_field>/rdd-form/<int:id>/update', river_rdd_update_form, name='rdd-form-update'),
    path('river/<id_field>/rdd-form/<int:id>/delete', river_rdd_delete, name='rdd-form-delete'),
    path('river/<id_field>/rdd-list/export', river_rdd_multi_delete, name='rdd-export'),
    path('river/<id_field>/rdd_pdf/', river_rdd_Pdf, name='rdd_pdf'),
    path('river/<id_field>/rdd-list/delete-all', river_rdd_multi_delete, name='delete-rdd-all'),

                    ################rdm###########
    path('river/<id_field>/rdm-form/', river_rdm_create_form, name='rdm-form-insert'),
    path('river/<id_field>/rdm-list/', river_rdm_list, name='rdm-list'),
    path('river/<id_field>/rdm-form/<int:id>/update', river_rdm_update_form, name='rdm-form-update'),
    path('river/<id_field>/rdm-form/<int:id>/delete', river_rdm_delete, name='rdm-form-delete'),
    path('river/<id_field>/rdm-list/export', export_river_discharge_monthly, name='rdm-export'),
    path('river/<id_field>/rdm_pdf/', river_rdm_Pdf, name='rdm_pdf'),
    path('river/<id_field>/rdm-list/delete-all', river_discharge_monthly_multi_delete, name='delete-rdm-all'),

                    #######################
    path('river/<id_field>/rda-form/', river_rda_create_form, name='rda-form-insert'),
    path('river/<id_field>/rda-list/', river_rda_list, name='rda-list'),
    path('river/<id_field>/rda-form/<int:id>/update', river_rda_update_form, name='rda-form-update'),
    path('river/<id_field>/rda-form/<int:id>/delete', river_rda_delete, name='rda-form-delete'),
    path('river/<id_field>/rda-list/export', export_river_discharge_annual, name='rda-export'),
    path('river/<id_field>/rda_pdf/', river_rda_Pdf, name='rda_pdf'),
    path('river/<id_field>/rda-list/delete-all', riverdischarge_anuall_multi_delete,name='delete-rda-all'),

                    #####################rfm
    path('river/<id_field>/rfm-form/', river_rfm_create_form, name='rfm-form-insert'),
    path('river/<id_field>/rfm-list/', river_rfm_list, name='rfm-list'),
    path('river/<id_field>/rfm-form/<int:id>/update', river_rfm_update_form, name='rfm-form-update'),
    path('river/<id_field>/rfm-form/<int:id>/delete', river_rfm_delete, name='rfm-form-delete'),
    path('river/<id_field>/rfm-list/export', export_riverflowmeasure, name='rfm-export'),
    path('river/<id_field>/rfm_pdf/', river_rfm_Pdf, name='rfm_pdf'),
    path('river/<id_field>/rfm-list/delete-all', riverflowmessure_multi_delete, name='delete-rfm-all'),

                    #########################surface_hq####
    path('river/<id_field>/rhq-form/', river_rhq_create_form, name='rhq-form-insert'),
    path('river/<id_field>/rhq-list/', river_rhq_list, name='rhq-list'),
    path('river/<id_field>/rhq-form/<int:id>/update', river_rhq_update_form, name='rhq-form-update'),
    path('river/<id_field>/rhq-form/<int:id>/delete', river_rhq_delete, name='rhq-form-delete'),
    path('river/<id_field>/rhq-list/export', export_surface_hq, name='rhq-export'),
  path('river/<id_field>/rh-pdf/', river_rh_Pdf, name='rh-pdf'),
path('river/<id_field>/rq-pdf/', river_rq_Pdf, name='rq-pdf'),
path('river/<id_field>/r-velocity-pdf/', river_rvelocity_Pdf, name='r-velocity-pdf'),
      path('river/<id_field>/rhq-list/delete-all', river_surface_hq_multi_delete, name='delete-rhq-all'),

                    ######################discharge_survey
    path('river/<id_field>/rds-form/', river_rds_create_form, name='rds-form-insert'),
    path('river/<id_field>/rds-list/', river_rds_list, name='rds-list'),
    path('river/<id_field>/rds-form/<int:id>/update', river_rds_update_form, name='rds-form-update'),
    path('river/<id_field>/rds-form/<int:id>/delete', river_rds_delete, name='rds-form-delete'),
    path('river/<id_field>/rds-list/export', export_discharge_survey, name='rds-export'),
    path('river/<id_field>/rds-up-pdf/', river_rds_up_Pdf, name='rds-up-pdf'),
    path('river/<id_field>/rds-low-pdf/', river_rds_low_Pdf, name='rds-low-pdf'),
    path('river/<id_field>/rds-list/delete-all', river_discharge_survey_multi_delete, name='delete-rds-all'),

                    ######################sectionarea_survey
    path('river/<id_field>/rss-form/', river_rss_create_form, name='rss-form-insert'),
    path('river/<id_field>/rss-list/', river_rss_list, name='rss-list'),
    path('river/<id_field>/rss-form/<int:id>/update', river_rss_update_form, name='rss-form-update'),
    path('river/<id_field>/rss-form/<int:id>/delete', river_rss_delete, name='rss-form-delete'),
    path('river/<id_field>/rss-list/export', export_sectionareasurvey, name='rss-export'),
    path('river/<id_field>/rss_pdf/', river_rss_Pdf, name='rss_pdf'),
    path('river/<id_field>/rss-list/delete-all', river_sectionareasurvey_multi_delete,name='delete-rss-all'),

     path('river/<id_field>/rsd-form/', river_rsd_create_form, name='rsd-form-insert'),
    path('river/<id_field>/rsd-list/', river_rsd_list, name='rsd-list'),
    path('river/<id_field>/rsd-form/<int:id>/update', river_rsd_update_form, name='rsd-form-update'),
    path('river/<id_field>/rsd-form/<int:id>/delete', river_rsd_delete, name='rsd-form-delete'),
    path('river/<id_field>/rsd-list/export', export_sectiondata, name='rsd-export'),
    path('river/<id_field>/rsd_pdf/', river_rsd_Pdf, name='rsd_pdf'),
    path('river/<id_field>/rds-list/delete-all', river_sectiondata_multi_delete,name='delete-rds-all'),

                    #######################springs##############
    path('spring/<id_field>/springinf_update/', spring_inf_update_form, name='springinf-update'),

    path('spring/<id_field>/sdd-form/', spring_sdd_create_form, name='sdd-form-insert'),
    path('spring/<id_field>/sdd-list/', spring_sdd_list, name='sdd-list'),
    path('spring/<id_field>/sdd-form/<int:id>/update', spring_sdd_update_form, name='sdd-form-update'),
    path('spring/<id_field>/sdd-form/<int:id>/delete', spring_sdd_delete, name='sdd-form-delete'),
    path('spring/<id_field>/sdd-list/export', export_spring_discharge_daily, name='sdd-export'),
    path('spring/<id_field>/sdd-pdf/', spring_sdd_Pdf, name='sdd-pdf'),
    path('spring/<id_field>/sdd-list/delete-all', spring_sdd_multi_delete, name='delete-sdd-all'),

                    ################sdm###########
    path('spring/<id_field>/sdm-form/', spring_sdm_create_form, name='sdm-form-insert'),
    path('spring/<id_field>/sdm-list/', spring_sdm_list, name='sdm-list'),
    path('spring/<id_field>/sdm-form/<int:id>/update', spring_sdm_update_form, name='sdm-form-update'),
    path('spring/<id_field>/sdm-form/<int:id>/delete', spring_sdm_delete, name='sdm-form-delete'),
    path('spring/<id_field>/sdm-list/export', export_spring_discharge_monthly, name='sdm-export'),
    path('spring/<id_field>/sdm-pdf/', spring_sdm_Pdf, name='sdm-pdf'),
    path('spring/<id_field>/sdm-list/delete-all', spring_sdm_multi_delete, name='delete-sdm-all'),

                    #######################sda
    path('spring/<id_field>/sda-form/', spring_sda_create_form, name='sda-form-insert'),
    path('spring/<id_field>/sda-list/', spring_sda_list, name='sda-list'),
    path('spring/<id_field>/sda-form/<int:id>/update', spring_sda_update_form, name='sda-form-update'),
    path('spring/<id_field>/sda-form/<int:id>/delete', spring_sda_delete, name='sda-form-delete'),
    path('spring/<id_field>/sda-list/export', export_spring_discharge_anually, name='sda-export'),
path('spring/<id_field>/sda-pdf/', spring_sda_Pdf, name='sda-pdf'),
    path('spring/<id_field>/sda-list/delete-all', spring_sda_multi_delete, name='delete-sda-all'),

                    #####################sdam
    path('spring/<id_field>/sdam-form/', spring_sdam_create_form, name='sdam-form-insert'),
    path('spring/<id_field>/sdam-list/', spring_sdam_list, name='sdam-list'),
    path('spring/<id_field>/sdam-form/<int:id>/update', spring_sdam_update_form, name='sdam-form-update'),
    path('spring/<id_field>/sdam-form/<int:id>/delete', spring_sdam_delete, name='sdam-form-delete'),
    path('spring/<id_field>/sdam-list/export', export_spring_discharge_avg_monthly, name='sdam-export'),
path('spring/<id_field>/sdam-pdf/', spring_sdam_Pdf, name='sdam-pdf'),
    path('spring/<id_field>/sdam-list/delete-all', spring_sdam_multi_delete, name='delete-sdam-all'),

                    #########################sdaa####

    path('spring/<id_field>/sdaa-form/', spring_sdaa_create_form, name='sdaa-form-insert'),
    path('spring/<id_field>/sdaa-list/', spring_sdaa_list, name='sdaa-list'),
    path('spring/<id_field>/sdaa-form/<int:id>/update', spring_sdaa_update_form, name='sdaa-form-update'),
    path('spring/<id_field>/sdaa-form/<int:id>/delete', spring_sdaa_delete, name='sdaa-form-delete'),
    path('spring/<id_field>/sdaa-list/export', export_spring_discharge_avg_anually, name='sdaa-export'),
    path('spring/<id_field>/sdaa-pdf/', spring_sdaa_Pdf, name='sdaa-pdf'),
    path('spring/<id_field>/sdaa-list/delete-all', spring_sdaa_multi_delete, name='delete-sdaa-all'),

                    ################## metology #################


    path('metology/<id_field>/metologyinf_update', metology_inf_update_form,name='metologyinf-update'),

    path('metology/<id_field>/air-form/', metology_air_create_form, name='air-form-insert'),
    path('metology/<id_field>/air-list/', metology_air_list, name='air-list'),
    path('metology/<id_field>/air-form/<int:id>/update', metology_air_update_form, name='air-form-update'),
    path('metology/<id_field>/air-form/<int:id>/delete', metology_air_delete, name='air-form-delete'),
    path('metology/<id_field>/air-list/export', export_airpressur, name='air-export'),
    path('metology/<id_field>/air-list/delete-all', metology_air_multi_delete, name='delete-air-all'),
    #path('metology/<id_field>/pdf/', air_Pdf,name='pdf'),
   path('metology/air-report/', report_xy_metologys,name='air-report'),
   path('metology/<id_field>/air_avg_pdf/', air_avg_Pdf,name='air_avg_pdf'),
path('metology/<id_field>/air_max_pdf/', air_max_Pdf,name='air_max_pdf'),
path('metology/<id_field>/air_min_pdf/', air_min_Pdf,name='air_min_pdf'),

############################snowfall########

path('metology/<id_field>/metologyinf_update', metology_inf_update_form,name='metologyinf-update'),

    path('metology/<id_field>/snowfall-form/', metology_snowfall_create_form, name='snowfall-form-insert'),
    path('metology/<id_field>/snowfall-list/', metology_snowfall_list, name='snowfall-list'),
    path('metology/<id_field>/snowfall-form/<int:id>/update', metology_snowfall_update_form, name='snowfall-form-update'),
    path('metology/<id_field>/snowfall-form/<int:id>/delete', metology_snowfall_delete, name='snowfall-form-delete'),
    path('metology/<id_field>/snowfall-list/export', export_snowfall, name='snowfall-export'),
    path('metology/<id_field>/snowfall-list/delete-all', metology_snowfall_multi_delete, name='delete-snowfall-all'),
   path('metology/<id_field>/snowfall_pdf/', snowfall_Pdf,name='snowfall_pdf'),



                    ###########################

############################snowdepth########

path('metology/<id_field>/metologyinf_update', metology_inf_update_form,name='metologyinf-update'),

    path('metology/<id_field>/snowdepth-form/', metology_snowdepth_create_form, name='snowdepth-form-insert'),
    path('metology/<id_field>/snowdepth-list/', metology_snowdepth_list, name='snowdepth-list'),
    path('metology/<id_field>/snowdepth-form/<int:id>/update', metology_snowdepth_update_form, name='snowdepth-form-update'),
    path('metology/<id_field>/snowdepth-form/<int:id>/delete', metology_snowdepth_delete, name='snowdepth-form-delete'),
    path('metology/<id_field>/snowdepth-list/export', export_snowdepth, name='snowdepth-export'),
    path('metology/<id_field>/snowdepth-list/delete-all', metology_snowdepth_multi_delete, name='delete-snowdepth-all'),
   path('metology/<id_field>/snowdepth_pdf/', snowdepth_Pdf,name='snowdepth_pdf'),



                    ###########################
    path('metology/<id_field>/td-form/', metology_td_create_form, name='td-form-insert'),
    path('metology/<id_field>/td-list/', metology_td_list, name='td-list'),
    path('metology/<id_field>/td-form/<int:id>/update', metology_td_update_form, name='td-form-update'),
    path('metology/<id_field>/td-form/<int:id>/delete', metology_td_delete, name='td-form-delete'),
    path('metology/<id_field>/td-list/export', export_temperature_daily, name='td-export'),
    path('metology/<id_field>/td_avg_pdf/', td_avg_Pdf,name='td_avg_Pdf'),
    path('metology/<id_field>/td_min_Pdf/', td_min_Pdf,name='td_min_Pdf'),
    path('metology/<id_field>/td_max_Pdf/', td_max_Pdf,name='td_max_Pdf'),
    path('metology/<id_field>/td-list/delete-all', metology_td_multi_delete, name='delete-td-all'),

                    #######################
    path('metology/<id_field>/ed-form/', metology_ed_create_form, name='ed-form-insert'),
    path('metology/<id_field>/ed-list/', metology_ed_list, name='ed-list'),
    path('metology/<id_field>/ed-form/<int:id>/update', metology_ed_update_form, name='ed-form-update'),
    path('metology/<id_field>/ed-form/<int:id>/delete', metology_ed_delete, name='ed-form-delete'),
    path('metology/<id_field>/ed-list/export', export_evaporation_daily, name='ed-export'),
    path('metology/<id_field>/ed_pdf/', ed_Pdf, name='ed_pdf'),
    path('metology/<id_field>/ed-list/delete-all', metology_ed_multi_delete, name='delete-ed-all'),

                    ###########################
    path('metology/<id_field>/em-form/', metology_em_create_form, name='em-form-insert'),
    path('metology/<id_field>/em-list/', metology_em_list, name='em-list'),
    path('metology/<id_field>/em-form/<int:id>/update', metology_em_update_form, name='em-form-update'),
    path('metology/<id_field>/em-form/<int:id>/delete', metology_em_delete, name='em-form-delete'),
    path('metology/<id_field>/em-list/export', export_evaporation_monthly, name='em-export'),
    path('metology/<id_field>/em_pdf/', em_Pdf, name='em_pdf'),
    path('metology/<id_field>/em-list/delete-all', metology_em_multi_delete, name='delete-em-all'),

                    ###############
    path('metology/<id_field>/tm-form/', metology_tm_create_form, name='tm-form-insert'),
    path('metology/<id_field>/tm-list/', metology_tm_list, name='tm-list'),
    path('metology/<id_field>/tm-form/<int:id>/update', metology_tm_update_form, name='tm-form-update'),
    path('metology/<id_field>/tm-form/<int:id>/delete', metology_tm_delete, name='tm-form-delete'),
    path('metology/<id_field>/tm-list/export', export_temperature_monthly, name='tm-export'),
    path('metology/<id_field>/tm_avg_Pdf/', tm_avg_Pdf, name='tm_avg_Pdf'),

    path('metology/<id_field>/tm_min_Pdf/', tm_min_Pdf, name='tm_min_Pdf'),
    path('metology/<id_field>/tm_max_Pdf/', tm_max_Pdf, name='tm_max_Pdf'),
    path('metology/<id_field>/tm-list/delete-all', metology_tm_multi_delete, name='delete-tm-all'),

                    #####################
    path('metology/<id_field>/hm-form/', metology_hm_create_form, name='hm-form-insert'),
    path('metology/<id_field>/hm-list/', metology_hm_list, name='hm-list'),
    path('metology/<id_field>/hm-form/<int:id>/update', metology_hm_update_form, name='hm-form-update'),
    path('metology/<id_field>/hm-form/<int:id>/delete', metology_hm_delete, name='hm-form-delete'),
    path('metology/<id_field>/hm-list/export', export_humidity_monthly, name='hm-export'),
    path('metology/<id_field>/hm_avg_Pdf/', hm_avg_Pdf, name='hm_avg_Pdf'),

    path('metology/<id_field>/hm_min_Pdf/', hm_min_Pdf, name='hm_min_Pdf'),
    path('metology/<id_field>/hm_max_Pdf/', hm_max_Pdf, name='hm_max_Pdf'),
    path('metology/<id_field>/hm-list/delete-all', metology_hm_multi_delete, name='delete-hm-all'),

                    #############################
    path('metology/<id_field>/hd-form/', metology_hd_create_form, name='hd-form-insert'),
    path('metology/<id_field>/hd-list/', metology_hd_list, name='hd-list'),
    path('metology/<id_field>/hd-form/<int:id>/update', metology_hd_update_form, name='hd-form-update'),
    path('metology/<id_field>/hd-form/<int:id>/delete', metology_hd_delete, name='hd-form-delete'),
    path('metology/<id_field>/hd-list/export', export_humidity_daily, name='hd-export'),
    path('metology/<id_field>/hd_max_Pdf/', hd_max_Pdf, name='hd_max_Pdf'),
    path('metology/<id_field>/hd_avg_Pdf/', hd_avg_Pdf, name='hd_avg_Pdf'),
    path('metology/<id_field>/hd_min_Pdf/', hd_min_Pdf, name='hd_min_Pdf'),
    path('metology/<id_field>/hd-list/delete-all', metology_hd_multi_delete, name='delete-hd-all'),

                    ######################
    path('metology/<id_field>/wd-form/', metology_wd_create_form, name='wd-form-insert'),
    path('metology/<id_field>/wd-list/', metology_wd_list, name='wd-list'),
    path('metology/<id_field>/wd-form/<int:id>/update', metology_wd_update_form, name='wd-form-update'),
    path('metology/<id_field>/wd-form/<int:id>/delete', metology_wd_delete, name='wd-form-delete'),
    path('metology/<id_field>/wd-list/export', export_wind_daily, name='wd-export'),
    path('metology/<id_field>/wd_avg_Pdf/', wd_avg_Pdf, name='wd_avg_Pdf'),
    path('metology/<id_field>/wd_max_Pdf/', wd_max_Pdf, name='wd_max_Pdf'),
    path('metology/<id_field>/wd_min_Pdf/', wd_min_Pdf, name='wd_min_Pdf'),
    path('metology/<id_field>/wd-list/delete-all', metology_wd_multi_delete, name='delete-wd-all'),

                    ######################
    path('metology/<id_field>/wm-form/', metology_wm_create_form, name='wm-form-insert'),
    path('metology/<id_field>/wm-list/', metology_wm_list, name='wm-list'),
    path('metology/<id_field>/wm-form/<int:id>/update', metology_wm_update_form, name='wm-form-update'),
    path('metology/<id_field>/wm-form/<int:id>/delete', metology_wm_delete, name='wm-form-delete'),
    path('metology/<id_field>/wm-list/export', export_wind_monthly, name='wm-export'),
    path('metology/<id_field>/wm_avg_Pdf/', wm_avg_Pdf, name='wm_avg_Pdf'),
    path('metology/<id_field>/wm-list/delete-all', metology_wm_multi_delete, name='delete-wm-all'),

                    #######################springs##############

    path('metology/<id_field>/pd-form/', metology_pd_create_form, name='pd-form-insert'),
    path('metology/<id_field>/pd-list/', metology_pd_list, name='pd-list'),
    path('metology/<id_field>/pd-form/<int:id>/update', metology_pd_update_form, name='pd-form-update'),
    path('metology/<id_field>/pd-form/<int:id>/delete', metology_pd_delete, name='pd-form-delete'),
    path('metology/<id_field>/pd-list/export', export_precipitation_daily, name='pd-export'),
     path('metology/<id_field>/pd_Pdf/', pd_Pdf, name='pd_Pdf'),
    path('metology/<id_field>/pd-list/delete-all', metology_pd_multi_delete, name='delete-pd-all'),

                    ###########################
    path('metology/<id_field>/pm-form/', metology_pm_create_form, name='pm-form-insert'),
    path('metology/<id_field>/pm-list/', metology_pm_list, name='pm-list'),
    path('metology/<id_field>/pm-form/<int:id>/update', metology_pm_update_form, name='pm-form-update'),
    path('metology/<id_field>/pm-form/<int:id>/delete', metology_pm_delete, name='pm-form-delete'),
    path('metology/<id_field>/pm-list/export', export_precipitation_monthly, name='pm-export'),
    path('metology/<id_field>/pm_Pdf/', pm_Pdf, name='pm_Pdf'),
    path('metology/<id_field>/pm-list/delete-all', metology_pm_multi_delete, name='delete-pm-all'),

                    #######################sda
    path('metology/<id_field>/pa-form/', metology_pa_create_form, name='pa-form-insert'),
    path('metology/<id_field>/pa-list/', metology_pa_list, name='pa-list'),
    path('metology/<id_field>/pa-form/<int:id>/update', metology_pa_update_form, name='pa-form-update'),
    path('metology/<id_field>/pa-form/<int:id>/delete', metology_pa_delete, name='pa-form-delete'),
    path('metology/<id_field>/pa-list/export', export_precipitation_annual, name='pa-export'),
    path('metology/<id_field>/pa_Pdf/', pa_Pdf, name='pa_Pdf'),
    path('metology/<id_field>/pa-list/delete-all', metology_pa_multi_delete, name='delete-pa-all'),

                    #####################sdam
    path('metology/<id_field>/sd-form/', metology_sd_create_form, name='sd-form-insert'),
    path('metology/<id_field>/sd-list/', metology_sd_list, name='sd-list'),
    path('metology/<id_field>/sd-form/<int:id>/update', metology_sd_update_form, name='sd-form-update'),
    path('metology/<id_field>/sd-form/<int:id>/delete', metology_sd_delete, name='sd-form-delete'),
    path('metology/<id_field>/sd-list/export', export_sunshine_daily, name='sd-export'),
    path('metology/<id_field>/sd_Pdf/', sd_rad_max_Pdf, name='sd_Pdf'),
    path('metology/<id_field>/sd_min_Pdf/', sd_rad_min_Pdf, name='sd_min_Pdf'),
    path('metology/<id_field>/sd_mj_Pdf/', sd_rad_mj_Pdf, name='sd_mj_Pdf'),
    path('metology/<id_field>/sd-list/delete-all', metology_sd_multi_delete, name='delete-sd-all'),

                    #########################sdaa####
    path('well/<id_field>/wellinf_update/', well_inf_update_form, name='wellinf_update'),

    path('well/<id_field>/gwl-form/', well_gwl_create_form, name='gwl-form-insert'),
    path('well/<id_field>/gwl-list/', well_gwl_list, name='gwl-list'),
    path('well/<id_field>/gwl-form/<int:id>/update', well_gwl_update_form, name='gwl-form-update'),
    path('well/<id_field>/gwl-form/<int:id>/delete', well_gwl_delete, name='gwl-form-delete'),
    path('well/<id_field>/gwl-list/export', export_well_groundwaterlevels, name='gwl-export'),
    path('well/<id_field>/gwl-pdf/', well_gwl_Pdf, name='gwl-pdf'),
    path('well/<id_field>/gwd-pdf/', well_gwd_Pdf, name='gwd-pdf'),
    path('well/<id_field>/gwl-list/delete-all', well_gwl_multi_delete, name='delete-gwl-all'),

                    path('well/<id_field>/gwlm-form/', well_gwlm_create_form, name='gwlm-form-insert'),
    path('well/<id_field>/gwlm-list/', well_gwlm_list, name='gwlm-list'),
    path('well/<id_field>/gwlm-form/<int:id>/update', well_gwlm_update_form, name='gwlm-form-update'),
    path('well/<id_field>/gwlm-form/<int:id>/delete', well_gwlm_delete, name='gwlm-form-delete'),
    path('well/<id_field>/gwlm-list/export', export_well_groundwaterlevel_manuals, name='gwlm-export'),
    path('well/<id_field>/gwlm-pdf/', well_gwlm_Pdf, name='gwlm-pdf'),
    path('well/<id_field>/gwlm-list/delete-all', well_gwlm_multi_delete, name='delete-gwlm-all'),

                    path('well/<id_field>/agw-form/', well_agw_create_form, name='agw-form-insert'),
    path('well/<id_field>/agw-list/', well_agw_list, name='agw-list'),
    path('well/<id_field>/agw-form/<int:id>/update', well_agw_update_form, name='agw-form-update'),
    path('well/<id_field>/agw-form/<int:id>/delete', well_agw_delete, name='agw-form-delete'),
    path('well/<id_field>/agw-list/export', export_well_auto_groundwater, name='agw-export'),
    path('well/<id_field>/agw-level-pdf/', well_agw_level_Pdf, name='agw-level-pdf'),
    path('well/<id_field>/agw-depth-pdf/', well_agw_depth_Pdf, name='agw-depth-pdf'),
    path('well/<id_field>/agw-list/delete-all', well_agw_multi_delete, name='delete-agw-all'),

                    path('well/<id_field>/wq-form/', well_wq_create_form, name='wq-form-insert'),
    path('well/<id_field>/wq-list/', well_wq_list, name='wq-list'),
    path('well/<id_field>/wq-form/<int:id>/update', well_wq_update_form, name='wq-form-update'),
    path('well/<id_field>/wq-form/<int:id>/delete', well_wq_delete, name='wq-form-delete'),
    path('well/<id_field>/wq-list/export', export_wells_quality, name='wq-export'),
    path('well/<id_field>/wq-ph-pdf/', well_wq_ph_Pdf, name='wq-ph-pdf'),
path('well/<id_field>/wq-ec-ms-m-pdf/', well_wq_ec_ms_Pdf, name='wq-ec-ms-m-pdf'),
    path('well/<id_field>/wq-list/delete-all', well_wq_multi_delete, name='delete-wq-all'),

                    path('well/<id_field>/wtl-form/', well_wtl_create_form, name='wtl-form-insert'),
    path('well/<id_field>/wtl-list/', well_wtl_list, name='wtl-list'),
    path('well/<id_field>/wtl-form/<int:id>/update', well_wtl_update_form, name='wtl-form-update'),
    path('well/<id_field>/wtl-form/<int:id>/delete', well_wtl_delete, name='wtl-form-delete'),
    path('well/<id_field>/wtl-list/export', export_welltoplevel, name='wtl-export'),
    path('well/<id_field>/wtl-pdf/', well_wtl_Pdf, name='wtl-pdf'),
    path('well/<id_field>/wtl-list/delete-all', well_wtl_multi_delete, name='delete-wtl-all'),

                    path('well/<id_field>/drill-form/', well_drill_create_form, name='drill-form-insert'),
    path('well/<id_field>/drill-list/', well_drill_list, name='drill-list'),
    path('well/<id_field>/drill-form/<int:id>/update', well_drill_update_form, name='drill-form-update'),
    path('well/<id_field>/drill-form/<int:id>/delete', well_drill_delete, name='drill-form-delete'),
    path('well/<id_field>/drill-list/export', export_drilling, name='drill-export'),
    path('well/<id_field>/drill-pdf/', well_drill_Pdf, name='drill-pdf'),
    path('well/<id_field>/drill-list/delete-all', well_drill_multi_delete, name='delete-drill-all'),

    path('well/<id_field>/casing-form/', well_casing_create_form, name='casing-form-insert'),
    path('well/<id_field>/casing-list/', well_casing_list, name='casing-list'),
    path('well/<id_field>/casing-form/<int:id>/update', well_casing_update_form, name='casing-form-update'),
    path('well/<id_field>/casing-form/<int:id>/delete', well_casing_delete, name='casing-form-delete'),
    path('well/<id_field>/casing-list/export', export_casing, name='casing-export'),
    path('well/<id_field>/casing-pdf/', well_casing_Pdf, name='casing-pdf'),
    path('well/<id_field>/g-list/delete-all', well_casing_multi_delete, name='delete-casing-all'),

    path('well/<id_field>/packing-form/', well_packing_create_form, name='packing-form-insert'),
    path('well/<id_field>/packing-list/', well_packing_list, name='packing-list'),
    path('well/<id_field>/packing-form/<int:id>/update', well_packing_update_form, name='packing-form-update'),
    path('well/<id_field>/packing-form/<int:id>/delete', well_packing_delete, name='packing-form-delete'),
    path('well/<id_field>/packing-list/export', export_packing, name='packing-export'),
    path('well/<id_field>/packing-pdf/', well_packing_Pdf, name='packing-pdf'),
    path('well/<id_field>/packing-list/delete-all', well_packing_multi_delete, name='delete-packing-all'),

    path('well/<id_field>/wl-form/', well_wl_create_form, name='wl-form-insert'),
    path('well/<id_field>/wl-list/', well_wl_list, name='wl-list'),
    path('well/<id_field>/wl-form/<int:id>/update', well_wl_update_form, name='wl-form-update'),
    path('well/<id_field>/wl-form/<int:id>/delete', well_wl_delete, name='wl-form-delete'),
    path('well/<id_field>/wl-list/export', export_welllogging, name='wl-export'),
    path('well/<id_field>/wl-pdf/', well_log_pdf, name='wl-pdf'),
                    path('well/<id_field>/wl-list/delete-all', well_wl_multi_delete, name='delete-wl-all'),

                    path('well/<id_field>/ll-form/', well_ll_create_form, name='ll-form-insert'),
    path('well/<id_field>/ll-list/', well_ll_list, name='ll-list'),
    path('well/<id_field>/ll-form/<int:id>/update', well_ll_update_form, name='ll-form-update'),
    path('well/<id_field>/ll-form/<int:id>/delete', well_ll_delete, name='ll-form-delete'),
    path('well/<id_field>/ll-list/export', export_lithologging, name='ll-export'),
    path('well/<id_field>/ll-pdf', well_ll_Pdf, name='ll-pdf'),
                    path('well/<id_field>/ll-list/delete-all', well_ll_multi_delete, name='delete-ll-all'),

                    path('well/<id_field>/ld-form/', well_ld_create_form, name='ld-form-insert'),
    path('well/<id_field>/ld-list/', well_ld_list, name='ld-list'),
    path('well/<id_field>/ld-form/<int:id>/update', well_ld_update_form, name='ld-form-update'),
    path('well/<id_field>/ld-form/<int:id>/delete', well_ld_delete, name='ld-form-delete'),
                    # path('well/<id_field>/ld-list/delete-all', well_ld_multi_delete, name='delete-ld-all'),

                    path('well/<id_field>/lp-form/', well_lp_create_form, name='lp-form-insert'),
    path('well/<id_field>/lp-list/', well_lp_list, name='lp-list'),
    path('well/<id_field>/lp-form/<int:id>/update', well_lp_update_form, name='lp-form-update'),
    path('well/<id_field>/lp-form/<int:id>/delete', well_lp_delete, name='lp-form-delete'),

                    ##############################################
    # path('test/success/', SuccessView.as_view(), name='success_view'),
    path('', HomePageView.as_view(),name='home'),
    path('import/', views.import_data, name='import'),
    path('xy_rivers/', views.all_xy_rivers, name='xy_rivers'),
    # path('river/<id_field>/', views.river_point_details, name='rdetails'),


    path('points_data/', views.waterpoints_datasets, name='points'),
    path('xy_river_data/', views.xy_river_datasets, name='river_points'),
    # path('xy_spring_data/', views.xy_spring_datasets, name='spring_points'),
    path('xy_wells/', all_xy_wells, name='xy_wells'),
    path('xy_wells/import/', import_well_readings, name='import-well'),
    path('xy_springs/import/', import_spring_readings, name='import-spring'),
    path('xy_rivers/import/', import_river_readings, name='import-river'),

                    path('xy_springs/', all_xy_springs, name='xy_springs'),
    path('xy_metologys/', all_xy_metologys, name='xy_metologys'),
    path('xy_metologys/import/',import_metology_readings,name='import-metology'),


    path('export/metology/csv/', export_filtered_metologys_csv, name='metologys_csv'),
    path('export/metology/xls/', export_filtered_metologys_xls, name='metologys_xls'),
    path('export/well/csv/', export_filtered_wells_csv, name='wells_csv'),
    path('export/well/xls/', export_filtered_wells_xls, name='wells_xls'),
    path('export/spring/csv/', export_filtered_springs_csv, name='springs_csv'),
    path('export/spring/xls/', export_filtered_springs_xls, name='springs_xls'),
    path('export/river/csv/', export_filtered_rivers_csv, name='rivers_csv'),
    path('export/river/xls/', export_filtered_rivers_xls, name='rivers_xls'),

    ################################





    path('river_points', RiverListView.as_view(), name='river_points'),
    path('create/river/', RiverCreate.as_view(template_name = 'observe/river_form.html'), name='river-create'),
    path('update/river/<pk>', RiverUpdate.as_view(template_name = 'observe/river_form.html'), name='river-update'),
    path('delete/river/<pk>', RiverDelete.as_view(), name='river-delete'),

    path('well_points', WellListView.as_view(), name='well_points'),
    path('create/well/', WellCreate.as_view(template_name = 'observe/well_form.html'), name='well-create'),
    path('update/well/<pk>', WellUpdate.as_view(template_name = 'observe/well_form.html'), name='well-update'),
    path('delete/well/<pk>', WellDelete.as_view(), name='well-delete'),

    path('spring_points', SpringListView.as_view(), name='spring_points'),
    path('create/spring/', SpringCreate.as_view(template_name = 'observe/spring_form.html'), name='spring-create'),
    path('update/spring/<pk>', SpringUpdate.as_view(template_name = 'observe/spring_form.html'), name='spring-update'),
    path('delete/spring/<pk>', SpringDelete.as_view(), name='spring-delete'),

    path('metology_points', MetologyListView.as_view(), name='metology_points'),
    path('create/metology/', MetologyCreate.as_view(template_name = 'observe/metology_form.html'), name='metology-create'),
    path('update/metology/<pk>', MetologyUpdate.as_view(template_name = 'observe/metology_form.html'), name='metology-update'),

    path('delete/metology/<pk>', MetologyDelete.as_view(template_name='observe/xy_metology_confirm_delete.html'), name='metology-delete'),

##########################
    path('waterpoints', all_waterpoint_pump, name='waterpoints'),
    path('create/waterpoint/', WaterpointCreate.as_view(template_name = 'observe/waterpoint_form.html'), name='waterpoint-create'),
    path('update/waterpoint/<int:pk>', WaterpointUpdate.as_view(template_name = 'observe/waterpoint_form.html'), name='waterpoint-update'),
    path('delete/waterpoint/<int:pk>', WaterpointDelete.as_view(), name='waterpoint-delete'),

    path('pumping/<int:waterpoint_id>/pump-form/', pumping_pmp_form, name='pump-form-insert'),
    path('pumping/<int:waterpoint_id>/pump-list/', pumping_pmp_list, name='pump-list'),
    path('pumping/<int:waterpoint_id>/pump-form/<int:id>/update', pumping_pmp_form, name='pump-form-update'),
    path('pumping/<int:waterpoint_id>/pump-form/<int:id>/delete', pumping_pmp_delete, name='pump-form-delete'),

    #################

    path('pumping/<int:pumping_id>/pump-obswell-form/', pumptest_obswell_form, name='pump-obswell-form-insert'),
    path('pumping/<int:pumping_id>/pump-obswell-list/', pumptest_obswell_list, name='pump-obswell-list'),
    path('pumping/<int:pumping_id>/pump-obswell-form/<int:id>/update', pumptest_obswell_form, name='pump-obswell-form-update'),
    path('pumping/<int:pumping_id>/pump-obswell-form/<int:id>/delete', pumptest_obswell_delete, name='pump-obswell-form-delete'),

    ###############

    path('pumping/<int:pumping_id>/pump-pumpwell-form/', pumptest_pumpwell_form, name='pump-pumpwell-form-insert'),
    path('pumping/<int:pumping_id>/pump-pumpwell-list/', pumptest_pumpwell_list, name='pump-pumpwell-list'),
    path('pumping/<int:pumping_id>/pump-pumpwell-form/<int:id>/update', pumptest_pumpwell_form,name='pump-pumpwell-form-update'),
    path('pumping/<int:pumping_id>/pump-pumpwell-form/<int:id>/delete', pumptest_pumpwell_delete,name='pump-pumpwell-form-delete'),

    ###############

    path('pumping/<int:pumping_id>/step-drawdown-form/', step_drawdown_form, name='step-drawdown-form-insert'),
    path('pumping/<int:pumping_id>/step-drawdown-list/', step_drawdown_list, name='step-drawdown-list'),
    path('pumping/<int:pumping_id>/step-drawdown-form/<int:id>/update', step_drawdown_form,name='step-drawdown-form-update'),
    path('pumping/<int:pumping_id>/step-drawdown-form/<int:id>/delete', step_drawdown_delete,name='step-drawdown-form-delete'),

    ###############
    path('pumping/<int:pumping_id>/continious-dischage-form/', continious_dischage_form, name='continious-dischage-form-insert'),
    path('pumping/<int:pumping_id>/continious-dischage-list/', continious_dischage_list, name='continious-dischage-list'),
    path('pumping/<int:pumping_id>/continious-dischage-form/<int:id>/update', continious_dischage_form,name='continious-dischage-form-update'),
    path('pumping/<int:pumping_id>/continious-dischage-form/<int:id>/delete', continious_dischage_delete,name='continious-dischage-form-delete'),

    ##############
    path('pumping/<int:pumping_id>/recovery-test-form/', recovery_test_form,
         name='recovery-test-form-insert'),
    path('pumping/<int:pumping_id>/recovery-test-list/', recovery_test_list,
         name='recovery-test-list'),
    path('pumping/<int:pumping_id>/recovery-test-form/<int:id>/update', recovery_test_form,
         name='recovery-test-form-update'),
    path('pumping/<int:pumping_id>/recovery-test-form/<int:id>/delete', recovery_test_delete,
         name='recovery-test-form-delete'),
    ######################


    path('stations', all_waterchemistrysurvey_station, name='stations'),
    path('create/waterstation/', waterchemistrysurvey_stationCreate.as_view(template_name = 'observe/water_station_form.html'), name='waterstation-create'),
    path('update/waterstation/<pk>', waterchemistrysurvey_stationUpdate.as_view(template_name = 'observe/water_station_form.html'), name='waterstation-update'),
    path('delete/waterstation/<pk>', waterchemistrysurvey_stationDelete.as_view(template_name = 'observe/water_station_confirm_delete.html'), name='waterstation-delete'),

path('waterstation/<waterchemistrysurvey_station_id>/watersample-form/', watersample_form, name='watersample-form-insert'),
    path('waterstation/<waterchemistrysurvey_station_id>/watersample-list/', watersample_list, name='watersample-list'),
    path('waterstation/<waterchemistrysurvey_station_id>/watersample-form/<sample_id>/update', watersample_form,name='watersample-form-update'),
    path('waterstation/<waterchemistrysurvey_station_id>/watersample-form/<sample_id>/delete', watersample_delete,name='watersample-form-delete'),

    path('waterstation/<watersampling_id>/fieldparameter-form/', fieldparameter_form, name='fieldparameter-form-insert'),
    path('waterstation/<watersampling_id>/fieldparameter-list/', fieldparameter_list, name='fieldparameter-list'),
    path('waterstation/<watersampling_id>/fieldparameter-form/<int:id>/update', fieldparameter_form,name='fieldparameter-form-update'),
    path('waterstation/<watersampling_id>/fieldparameter-form/<int:id>/delete', fieldparameter_delete,name='fieldparameter-form-delete'),

   path('waterstation/<int:watersampling_id>/eutrophication2-form/', eutrophication2_form, name='eutrophication2-form-insert'),
   path('waterstation/<int:watersampling_id>/eutrophication2-list/', eutrophication2_list, name='eutrophication2-list'),
   path('waterstation/<int:watersampling_id>/eutrophication2-form/<int:id>/update', eutrophication2_form,name='eutrophication2-form-update'),
   path('waterstation/<int:watersampling_id>/eutrophication2-form/<int:id>/delete', eutrophication2_delete,name='eutrophication2-form-delete'),

path('waterstation/<int:watersampling_id>/heavymetals-rareelement-form/', heavymetals_rareelement_form, name='heavymetals-rareelement-form-insert'),
   path('waterstation/<int:watersampling_id>/heavymetals-rareelement-list/', heavymetals_rareelement_list, name='heavymetals-rareelement-list'),
   path('waterstation/<int:watersampling_id>/heavymetals-rareelement-form/<int:id>/update', heavymetals_rareelement_form,name='heavymetals-rareelement-form-update'),
   path('waterstation/<int:watersampling_id>/heavymetals-rareelement-form/<int:id>/delete', heavymetals_rareelement_delete,name='heavymetals-rareelement-form-delete'),

path('waterstation/<int:watersampling_id>/hydrochemical-form/', hydrochemical_form, name='hydrochemical-form-insert'),
   path('waterstation/<int:watersampling_id>/hydrochemical-list/', hydrochemical_list, name='hydrochemical-list'),
   path('waterstation/<int:watersampling_id>/hydrochemical-form/<int:id>/update', hydrochemical_form,name='hydrochemical-form-update'),
   path('waterstation/<int:watersampling_id>/hydrochemical-form/<int:id>/delete', hydrochemical_delete,name='hydrochemical-form-delete'),

path('waterstation/<int:watersampling_id>/othercommon-parameters-form/', othercommon_parameters_form, name='othercommon-parameters-form-insert'),
   path('waterstation/<int:watersampling_id>/othercommon-parameters-list/', othercommon_parameters_list, name='othercommon-parameters-list'),
   path('waterstation/<int:watersampling_id>/othercommon-parameters-form/<int:id>/update', othercommon_parameters_form,name='othercommon-parameters-form-update'),
   path('waterstation/<int:watersampling_id>/othercommon-parameters-form/<int:id>/delete', othercommon_parameters_delete,name='othercommon-parameters-form-delete'),

path('waterstation/<int:watersampling_id>/toxic-substances-form/', toxic_substances_form, name='toxic-substances-form-insert'),
   path('waterstation/<int:watersampling_id>/toxic-substances-list/', toxic_substances_list, name='toxic-substances-list'),
   path('waterstation/<int:watersampling_id>/toxic-substances-form/<int:id>/update', toxic_substances_form,name='toxic-substances-form-update'),
   path('waterstation/<int:watersampling_id>/toxic-substances-form/<int:id>/delete', toxic_substances_delete,name='toxic-substances-form-delete'),

################33

    path('metology/<id_field>/air-list/create-pdf', generate_pdf, name='create-pdf'),
                ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
