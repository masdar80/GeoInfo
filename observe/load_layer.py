import os
from django.contrib.gis.utils import LayerMapping
from observe.rivers.models import XY_River
from observe.metologys.models import XY_Metology
from observe.springs.models import XY_Spring
from observe.wells.models import XY_Well

waterpoint_mapping = {

    'id_field': 'id_field',
    'old_id': 'old_id',
    'sitename_a': 'sitename_a',
    'sitename_e': 'sitename_e',
    'type': 'type',
    'agency': 'agency',
    'mohafaza': 'mohafaza',
    'montika': 'montika',
    'nahia': 'nahia',
    'village': 'village',
    'sub_baisn': 'sub_baisn',
    # 'w84_lon_de': 'w84_lon_de',
    # 'w84_lon_mi': 'w84_lon_mi',
    # 'w84_lon_se': 'w84_lon_se',
    # 'x_dec': 'X_Dec',
    # 'w84_lat_de': 'w84_lat_de',
    # 'w84_lat_mi': 'w84_lat_mi',
    # 'w84_lat_se': 'w84_lat_se',
    # 'y_dec': 'Y_Dec',
    # 'w84_utm_zo': 'w84_utm_zo',
    'x': 'x',
    'y': 'y',
    'w84_utm_z': 'w84_utm_z',
    'means_z': 'means_z',
    'other_sour': 'other_sour',
    # 'y_1': 'Y_1',
    # 'x_1': 'X_1',
    # 'data_sourc': 'data_sourc',

    'geom': 'MULTIPOINT',

}
xy_river_mapping = {
    'id_field': 'id_field',
    'old_id': 'old_id',
    'sitename_a': 'sitename_a',
    'sitename_e': 'sitename_e',
    'type': 'type',
    'agency': 'agency',
    'mohafaza': 'mohafaza',
    'montika': 'montika',
    'nahia': 'nahia',
    'village': 'village',
    'sub_baisn': 'sub_baisn',

    'w84_utm_x': 'w84_utm_x',
    'w84_utm_y': 'w84_utm_y',
    'w84_utm_z': 'w84_utm_z',
    'means_z': 'means_z',

    'data_sourc': 'data_sourc',

    'geom': 'MULTIPOINT',

}
# xy_river_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data/ri-4.shp'))
# def run(verbose=True):
#     lm = LayerMapping(XY_River,xy_river_shp,xy_river_mapping,transform=False,encoding='utf-8')
#
#     lm.save(strict=True,verbose=verbose)
############################
#
xy_spring_mapping = {
    'id_field': 'id_field',
    'old_id': 'old_id',
    'sitename_a': 'sitename_a',
    'sitename_e': 'sitename_e',
    'type': 'type',
    'agency': 'agency',
    'mohafaza': 'mohafaza',
    'montika': 'montika',
    'nahia': 'nahia',
    'village': 'village',
    'sub_baisn': 'sub_baisn',
    'w84_utm_x': 'w84_utm_x',
    'w84_utm_y': 'w84_utm_y',
    'w84_utm_z': 'w84_utm_z',
    'means_z': 'means_z',
    'data_sourc': 'data_sourc',
    'geom': 'MULTIPOINT',

}
# xy_spring_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data/sp-3.shp'))
# def run(verbose=True):
#     lm = LayerMapping(XY_Spring,xy_spring_shp,xy_spring_mapping,transform=False,encoding='utf-8')
#     lm.save(strict=True,verbose=verbose)

# ############################
# #
xy_well_mapping = {
    'id_field': 'id_field',
    'old_id': 'old_id',
    'sitename_a': 'sitename_a',
    'sitename_e': 'sitename_e',
    'type': 'type',
    'agency': 'agency',
    'mohafaza': 'mohafaza',
    'montika': 'montika',
    'nahia': 'nahia',
    'village': 'village',
    'sub_baisn': 'sub_baisn',

    'w84_utm_x': 'w84_utm_x',
    'w84_utm_y': 'w84_utm_y',
    'w84_utm_z': 'w84_utm_z',
    'means_z': 'means_z',

    'data_sourc': 'data_sourc',
    'geom': 'POINT',
}
#
# xy_well_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/gw-3.shp'))
# def run(verbose=True):
#     lm = LayerMapping(XY_Well, xy_well_shp, xy_well_mapping, transform=False, encoding='utf-8')
#     lm.save(strict=True, verbose=verbose)


# ########################
# #
xy_metology_mapping = {
    'id_field': 'id_field',
    'old_id': 'old_id',
    'sitename_a': 'sitename_a',
    'sitename_e': 'sitename_e',
    'type': 'type',
    'agency': 'agency',
    'mohafaza': 'mohafaza',
    'montika': 'montika',
    'nahia': 'nahia',
    'village': 'village',
    'sub_baisn': 'sub_baisn',

    'w84_utm_x': 'w84_utm_x',
    'w84_utm_y': 'w84_utm_y',
    'w84_utm_z': 'w84_utm_z',
    'means_z': 'means_z',

    'data_sourc': 'data_sourc',
    'geom': 'POINT',
}

#
xy_metology_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/me-7.shp'))
def run(verbose=True):
    lm = LayerMapping(XY_Metology, xy_metology_shp, xy_metology_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
