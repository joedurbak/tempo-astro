import os

# import gcn
import numpy as np
from pandas import DataFrame
from astropy import units

BASEDIR = os.path.dirname(__file__)
print(BASEDIR)
AIRMASS_LIMIT = 2.0
MARKDOWN = True
DCT_LOC_PICKLE = 'salt_loc.pickle'
DCT_ASTROPLAN_LOC_PICKLE = 'salt_astroplan_loc.pickle'
ARCHIVED_XML_DIR = os.path.join(BASEDIR, "processed_xml")
OUTPUT_HTML_DIR = os.path.join(BASEDIR, "output_html")
TEMPLATE_HTML_DIR = os.path.join(BASEDIR, "html_templates")
OBSLIST_DIR = os.path.join(BASEDIR, "observation_lists")
LOCATION_NAME = "Sutherland"
AIRMASS_ORG_LOCATION = 'salt'
OBSERVABLE_TIME_MINIMUM_MINUTES = 15
MAX_RA_DEC_OFFSET_ARCMIN = 37
MIN_RA_DEC_OFFSET_ARCMIN = 4

OBSERVATION_LIST_DEFAULTS = {
    'Observer(PI institute)': 'NASA',
    'GridType': 'all_sky_grid',
    'ObjectType': 'ToO',
    'RA(h:m:s)': '00:00:00.0',
    'DEC(d:m:s)': '+00:00:00.0',
    'RAoffset(")': 0,
    'DECoffset(")': 0,
    'Filter1': 'Open',
    'Filter2': 'J',
    'DitherType': 'Random',
    'DitherRadius(")': 90,
    'DitherPhase(°)': 0,
    'DitherTotal': 30,
    'Images': 1,
    'IntegrationTime(s)': 60.06,
    'PIName': 'NASA_ToO_team',
    'TargetName': 'GCN_alert',
    'SpecificTime': '',
    'Priority': 'High',
    'Comment': ''
}

_max_tiling_time_s = 60 * 60 * 2
_tile_time_s = 10 * 10 * 2
_n_tiles = int(_max_tiling_time_s / _tile_time_s)
_fov_sq_deg = 1.56
_max_tile_area = _fov_sq_deg * _n_tiles
MAX_ERROR_RADIUS = (np.sqrt(_max_tile_area/np.pi)) * units.deg
print('MAX_ERROR_RADIUS', MAX_ERROR_RADIUS)
MIN_TILE_ERROR_RADIUS = 0.5*units.deg

FALSE_FLAGS = [
        "./What/Group/Param[@name='StarTrack_Lost_Lock']",
        "./What/Group/Param[@name='Def_NOT_a_GRB']"
]
TRUE_FLAGS = []

HTML_TEMPLATES_DICT = {
    'astro_coords_html': 'astro_coords.html',
    'author_html': 'author.html',
    'authors_html': 'authors.html',
    'citation_html': 'citation.html',
    'citations_html': 'citations.html',
    'event_ivorn_html': 'event_ivorn.html',
    'event_ivorns_html': 'event_ivorns.html',
    'field_html': 'field.html',
    'fields_html': 'fields.html',
    'how_html': 'how.html',
    'inference_html': 'inference.html',
    'inferences_html': 'inferences.html',
    'observation_location_html': 'observation_location.html',
    'observatory_location_html': 'observatory_location.html',
    'param_html': 'param.html',
    'params_html': 'params.html',
    'position2d_html': 'position2d.html',
    'position3d_html': 'position3d.html',
    'reference_html': 'reference.html',
    'references_html': 'references.html',
    'table_html': 'table.html',
    'tables_html': 'tables.html',
    'time_instant_html': 'time_instant.html',
    'voevent_html': 'voevent.html',
    'what_html': 'what.html',
    'wherewhen_html': 'wherewhen.html',
    'who_html': 'who.html',
    'why_html': 'why.html',
    'icon_html': 'icon.html',
    'modal_html': 'modal.html',
    'groups_html': 'groups.html',
    'group_html': 'group.html',
    'container_html': 'container.html',
    'simple_row_html': 'simple_row.html',
}

if MARKDOWN:
    for k, v in HTML_TEMPLATES_DICT.items():
        HTML_TEMPLATES_DICT[k] = v.replace('.html', '.md')
    OUTPUT_HTML_DIR = "output_md"
    TEMPLATE_HTML_DIR = "markdown"

for k, v in HTML_TEMPLATES_DICT.items():
    HTML_TEMPLATES_DICT[k] = os.path.join(TEMPLATE_HTML_DIR, v)

for directory in [ARCHIVED_XML_DIR, OUTPUT_HTML_DIR]:
    if not os.path.isdir(directory):
        os.makedirs(directory)

_observations = [
    # (filter1, filter2, total_exposure_time_seconds, exposure_time_per_frame)
    ('Open', 'J', 30*60, 60),
    ('Open', 'H', 30*60, 11.44),
    # ('Open', 'Y', 30*60, 20),
    # ('Z', 'Open', 30*60, 20)
]

OBSERVATIONS = DataFrame(_observations)
OBSERVATIONS.columns = ('filter1', 'filter2', 'total_exposure_time_seconds', 'exposure_time_per_frame')
_total_observation_time = OBSERVATIONS.total_exposure_time_seconds.sum()
_total_telescope_time = _total_observation_time * 2

_message = 'Observation list contains the following exposures:\n\n'
_message += '```\n' + str(OBSERVATIONS.to_markdown()) + '\n```\n'
_message += '*Some notes*\n'

site = 'https://docs.google.com/forms/d/e/1FAIpQLSeXhoZNJcR8_4zFdiFDUNi-Q2kV9oZuTB-PrJUWwrXBZCSgFQ/viewform?usp=sharing'
_message += '  - To observe this target, submit observation list csv to the PRIME proposal submission site: {}\n'.format(
    site
)
_message += '  - Next, send a message to the telescope operator in obs-request channel'
_message += ' on the PRIME discord to ensure they are aware of the sumbitted ToO\n'
_message += '  - Total telescope time, {} minutes, is ~2x total exposure time for all filters, {} minutes.\n'.format(
    int(_total_telescope_time/60), int(_total_observation_time/60)
)
_message += '  - If desired, it is recommended to edit the exposure time by altering the DitherTotal field in the csv\n'
_message += '  - When adding new lines to the observation list csv, the BlockID values must be unique\n'
_message += '  - Filter1 options are Open, Z, Narrow and Dark\n'
_message += '  - Filter2 options are Y, J, H and Open\n'
_message += '  - If you have trouble reaching the observer, try calling the observatory: +27 231000191'

SLACK = {
    'initial_message': "GCN Alert! More info incoming\n\nObservatory weather: https://suthweather.saao.ac.za/",
    'slack_token': os.environ.get('SLACKTOKEN', 'NA'),
    # 'slack_channel': 'C06APCA2H99',  # bot_testing
    'slack_channel': 'C06A8KNSV0X',  # gcn
    'observation_list_message': _message
}

GCN = {
    'client_id': os.environ.get('GCNCLIENTID', ''),
    'client_secret': os.environ.get('GCNCLIENTSECRET', ''),
    'topics': [
        'gcn.classic.voevent.FERMI_GBM_ALERT',
        'gcn.classic.voevent.FERMI_GBM_FIN_POS',
        'gcn.classic.voevent.FERMI_GBM_TRANS',
        'gcn.classic.voevent.FERMI_LAT_MONITOR',
        'gcn.classic.voevent.FERMI_LAT_POS_DIAG',
        'gcn.classic.voevent.FERMI_LAT_POS_INI',
        'gcn.classic.voevent.FERMI_LAT_POS_UPD',
        'gcn.classic.voevent.FERMI_LAT_TRANS',
        'gcn.classic.voevent.SWIFT_BAT_GRB_LC',
        'gcn.classic.voevent.SWIFT_BAT_SCALEDMAP',
        'gcn.classic.voevent.SWIFT_BAT_TRANS',
        'gcn.classic.voevent.SWIFT_XRT_POSITION',
        'gcn.notices.svom.voevent.grm',
        'gcn.notices.svom.voevent.eclairs',
        'gcn.notices.svom.voevent.mxt',
        'gcn.notices.icecube.lvk_nu_track_search',
        'igwn.gwalert',
        'gcn.notices.swift.bat.guano',
        'gcn.notices.einstein_probe.wxt.alert',
        'gcn.classic.voevent.IPN_POS',
    ]
}

gcn_testing = False

if gcn_testing:
    GCN['topics'] = [
        'gcn.classic.voevent.SWIFT_ACTUAL_POINTDIR',
        # 'gcn.classic.voevent.SWIFT_BAT_ALARM_LONG',
        # 'gcn.classic.voevent.SWIFT_BAT_ALARM_SHORT',
        # 'gcn.classic.voevent.SWIFT_BAT_GRB_ALERT',
        'gcn.classic.voevent.SWIFT_BAT_GRB_LC',
        # 'gcn.classic.voevent.SWIFT_BAT_GRB_LC_PROC',
        'gcn.classic.voevent.SWIFT_BAT_GRB_POS_ACK',
        # 'gcn.classic.voevent.SWIFT_BAT_GRB_POS_NACK',
        'gcn.classic.voevent.SWIFT_BAT_GRB_POS_TEST',
        # 'gcn.classic.voevent.SWIFT_BAT_KNOWN_SRC',
        # 'gcn.classic.voevent.SWIFT_BAT_MONITOR',
        'gcn.classic.voevent.SWIFT_BAT_QL_POS',
        'gcn.classic.voevent.SWIFT_BAT_SCALEDMAP',
        # 'gcn.classic.voevent.SWIFT_BAT_SLEW_POS',
        # 'gcn.classic.voevent.SWIFT_BAT_SUB_THRESHOLD',
        # 'gcn.classic.voevent.SWIFT_BAT_SUBSUB',
        'gcn.classic.voevent.SWIFT_BAT_TRANS',
        'gcn.classic.voevent.SWIFT_FOM_OBS',
        # 'gcn.classic.voevent.SWIFT_FOM_PPT_ARG_ERR',
        # 'gcn.classic.voevent.SWIFT_FOM_SAFE_POINT',
        # 'gcn.classic.voevent.SWIFT_FOM_SLEW_ABORT',
        'gcn.classic.voevent.SWIFT_POINTDIR',
        'gcn.classic.voevent.SWIFT_SC_SLEW',
        'gcn.classic.voevent.SWIFT_TOO_FOM',
        'gcn.classic.voevent.SWIFT_TOO_SC_SLEW',
        'gcn.classic.voevent.SWIFT_UVOT_DBURST',
        'gcn.classic.voevent.SWIFT_UVOT_DBURST_PROC',
        'gcn.classic.voevent.SWIFT_UVOT_EMERGENCY',
        'gcn.classic.voevent.SWIFT_UVOT_FCHART',
        'gcn.classic.voevent.SWIFT_UVOT_FCHART_PROC',
        'gcn.classic.voevent.SWIFT_UVOT_POS',
        'gcn.classic.voevent.SWIFT_UVOT_POS_NACK',
        'gcn.classic.voevent.SWIFT_XRT_CENTROID',
        # 'gcn.classic.voevent.SWIFT_XRT_EMERGENCY',
        'gcn.classic.voevent.SWIFT_XRT_IMAGE',
        'gcn.classic.voevent.SWIFT_XRT_IMAGE_PROC',
        'gcn.classic.voevent.SWIFT_XRT_LC',
        'gcn.classic.voevent.SWIFT_XRT_POSITION',
        'gcn.classic.voevent.SWIFT_XRT_SPECTRUM',
        'gcn.classic.voevent.SWIFT_XRT_SPECTRUM_PROC',
        'gcn.classic.voevent.SWIFT_XRT_SPER',
        'gcn.classic.voevent.SWIFT_XRT_SPER_PROC',
        'gcn.classic.voevent.SWIFT_XRT_THRESHPIX',
        'gcn.classic.voevent.SWIFT_XRT_THRESHPIX_PROC'
    ]

VERIFY_SSL = False
