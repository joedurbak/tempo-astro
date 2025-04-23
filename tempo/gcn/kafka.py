
from gcn_kafka import Consumer
from xmltodict import parse, unparse

from tempo.utils import settings
from tempo.utils.messages import xml_tag_loader, format_html, count_decimal_places, format_decimal_places, list_plus
from tempo.utils.coordinates import radec_to_altaz, TargetVisibilityAtDCT

GCN = settings.GCN
# notice_types = settings.INCLUDE_ALERT_MESSAGES
archived_xml_dir = settings.ARCHIVED_XML_DIR
output_html_dir = settings.OUTPUT_HTML_DIR
template_html_dir = settings.TEMPLATE_HTML_DIR

html_templates_dict = settings.HTML_TEMPLATES_DICT

class HTMLOutput:
    def __init__(
            self, xml_payload,
            voevent_html, who_html, what_html, wherewhen_html, how_html, why_html, citations_html, citation_html,
            reference_html, references_html, authors_html, author_html, param_html, params_html,
            table_html, tables_html, field_html, fields_html, observation_location_html, observatory_location_html,
            astro_coords_html, time_instant_html, position2d_html, position3d_html, inferences_html,
            inference_html, event_ivorn_html, event_ivorns_html, icon_html, modal_html, group_html, groups_html,
            container_html, simple_row_html
    ):
        self.xml_dict = parse(xml_payload)['voe:VOEvent']
        self.voevent_html = open(voevent_html, 'r').read()
        self.who_html = open(who_html, 'r').read()
        self.what_html = open(what_html, 'r').read()
        self.wherewhen_html = open(wherewhen_html, 'r').read()
        self.how_html = open(how_html, 'r').read()
        self.why_html = open(why_html, 'r').read()
        self.citations_html = open(citations_html, 'r').read()
        self.citation_html = open(citation_html, 'r').read()
        self.reference_html = open(reference_html, 'r').read()
        self.references_html = open(references_html, 'r').read()
        self.authors_html = open(authors_html, 'r').read()
        self.author_html = open(author_html, 'r').read()
        self.param_html = open(param_html, 'r').read()
        self.params_html = open(params_html, 'r').read()
        self.table_html = open(table_html, 'r').read()
        self.tables_html = open(tables_html, 'r').read()
        self.fields_html = open(fields_html, 'r').read()
        self.field_html = open(field_html, 'r').read()
        self.observation_location_html = open(observation_location_html, 'r').read()
        self.observatory_location_html = open(observatory_location_html, 'r').read()
        self.astro_coords_html = open(astro_coords_html, 'r').read()
        self.position2d_html = open(position2d_html, 'r').read()
        self.position3d_html = open(position3d_html, 'r').read()
        self.time_instant_html = open(time_instant_html, 'r').read()
        self.inferences_html = open(inferences_html, 'r').read()
        self.inference_html = open(inference_html, 'r').read()
        self.event_ivorn_html = open(event_ivorn_html, 'r').read()
        self.event_ivorns_html = open(event_ivorns_html, 'r').read()
        self.icon_html = open(icon_html, 'r').read()
        self.modal_html = open(modal_html, 'r').read()
        self.group_html = open(group_html, 'r').read()
        self.groups_html = open(groups_html, 'r').read()
        self.container_html = open(container_html, 'r').read()
        self.simple_row_html = open(simple_row_html, 'r').read()
        self.target_visibility = None
        self.html_output_name = ''

    def container_xml_to_html(self):
        context = {
            'VOEvent': self.voevent_xml_to_html(),
            'What_Description': xml_tag_loader(self.xml_dict, ('What', 'Description')),
            'Who_Date': xml_tag_loader(self.xml_dict, ('Who', 'Date')),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_unit': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', '@unit'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_Name1': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', 'Name1'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_Name2': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', 'Name2'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C1': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', 'Value2', 'C1'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C2': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', 'Value2', 'C2'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_Position2D_Error2Radius': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', 'Position2D', 'Error2Radius'
            )),
            'WhereWhen_ObservationLocation_AstroCoords_coord_system_id': xml_tag_loader(self.xml_dict, (
                'WhereWhen', 'ObsDataLocation', 'ObservationLocation', 'AstroCoords', '@coord_system_id'
            )),
            'ALT': '',
            'AZ': '',
            'CurrentlyVisible': '',
        }
        if context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Name1'].lower() == 'ra':
            ra = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C1']
            dec = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C2']
            error_radius = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Error2Radius']
        elif context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Name2'].lower() == 'ra':
            ra = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C2']
            dec = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Value2_C1']
            error_radius = context['WhereWhen_ObservationLocation_AstroCoords_Position2D_Error2Radius']
        else:
            return format_html(self.container_html, context)
        alt, az = radec_to_altaz(
            ra, dec, context['WhereWhen_ObservationLocation_AstroCoords_Position2D_unit']
        )
        dec_places = count_decimal_places(ra)
        alt = format_decimal_places(alt, dec_places)
        az = format_decimal_places(az, dec_places)
        context['ALT'], context['AZ'] = (alt, az)
        self.target_visibility = TargetVisibilityAtDCT(
            ra, dec, context['WhereWhen_ObservationLocation_AstroCoords_Position2D_unit'], error_radius
        )
        try:
            context['TargetIsUp'] = self.target_visibility.target_is_up
        except Exception as e:
            context['TargetIsUp'] = str(type(e))
        try:
            context['TargetRiseTime'] = self.target_visibility.target_rise_time.datetime
        except Exception as e:
            context['TargetRiseTime'] = str(type(e))
        try:
            context['TargetSetTime'] = self.target_visibility.target_set_time.datetime
        except Exception as e:
            context['TargetSetTime'] = str(type(e))
        try:
            context['TargetSetTime'] = self.target_visibility.target_set_time.datetime
        except Exception as e:
            context['TargetSetTime'] = str(type(e))
        context['TargetIsObservable'] = self.target_visibility.target_is_observable
        context['TwilightEvening'] = self.target_visibility.twilight_evening.datetime
        context['TwilightMorning'] = self.target_visibility.twilight_morning.datetime
        context['AirmassLimit'] = settings.AIRMASS_LIMIT
        context['TimeObservableMinutes'] = self.target_visibility.time_observable_minutes
        return format_html(self.container_html, context)

    def simple_row_xml_to_html(self, left_col_str, right_col_str):
        # if right_col_str == '':
        #     return ''
        return format_html(self.simple_row_html, {'LeftColStr': left_col_str, 'RightColStr': right_col_str})

    def voevent_xml_to_html(self):
        context = {
            "Who": self.who_xml_to_html(xml_tag_loader(self.xml_dict, ('Who', ))),
            "What": self.what_xml_to_html(xml_tag_loader(self.xml_dict, ('What', ))),
            "WhereWhen": self.wherewhen_xml_to_html(xml_tag_loader(self.xml_dict, ('WhereWhen', ))),
            "How": self.how_xml_to_html(xml_tag_loader(self.xml_dict, ('How', ))),
            "Why": self.why_xml_to_html(xml_tag_loader(self.xml_dict, ('Why', ))),
            "Citations": self.citations_xml_to_html(xml_tag_loader(self.xml_dict, ('Citations', ))),
            "Reference": self.references_xml_to_html(xml_tag_loader(self.xml_dict, ('Reference',))),
            "Description": xml_tag_loader(self.xml_dict, ('Description', )),
            "role": xml_tag_loader(self.xml_dict, ('@role', )),
            "ivorn": xml_tag_loader(self.xml_dict, ('@ivorn', )),
            'version': xml_tag_loader(self.xml_dict, ('@version', )),
        }
        return format_html(self.voevent_html, context)

    def who_xml_to_html(self, who_dict):
        context = {
            'AuthorIVORN': xml_tag_loader(who_dict, ('AuthorIVORN', )),
            'Date': xml_tag_loader(who_dict, ('Date', )),
            "Description": xml_tag_loader(who_dict, ('Description', )),
            "Reference": self.references_xml_to_html(xml_tag_loader(who_dict, ('Reference',))),
            "Authors": self.authors_xml_to_html(xml_tag_loader(who_dict, ('Author', ))),
        }
        pass
        context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
            context['Description'], 'whoModalDescription', 'description'
        )
        context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
            context['Reference'], 'whoModalDescription', 'description'
        )
        return format_html(self.who_html, context)

    def authors_xml_to_html(self, authors_list):
        markup = ""
        for author in list_plus(authors_list):
            context = {
                "title": xml_tag_loader(author, ('title', )),
                "shortName": xml_tag_loader(author, ('shortName',)),
                "contactName": xml_tag_loader(author, ('contactName',)),
                "contactEmail": xml_tag_loader(author, ('contactEmail',)),
                "contactPhone": xml_tag_loader(author, ('contactPhone',)),
                "contributor": xml_tag_loader(author, ('contributor',)),
            }
            markup += format_html(self.author_html, context)
        if markup == "":
            return markup
        context = {
            "Authors": markup,
        }
        return format_html(self.authors_html, context)

    def what_xml_to_html(self, what_dict):
        context = {
            'Params': self.params_xml_to_html(xml_tag_loader(what_dict, ('Param', ))),
            'Groups': self.groups_xml_to_html(xml_tag_loader(what_dict, ('Group', ))),
            'Tables': self.tables_xml_to_html(xml_tag_loader(what_dict, ('Table', ))),
            'Description': xml_tag_loader(what_dict, ('Description', )),
            'Reference': self.references_xml_to_html(xml_tag_loader(what_dict, ('Reference',))),
        }
        pass
        context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
            context['Description'], 'whatModalDescription', 'description'
        )
        context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
            context['Reference'], 'whatModalDescription', 'description'
        )
        return format_html(self.what_html, context)

    def params_xml_to_html(self, params_list, param_modal_id_prefix=""):
        markup = ""
        modals = ""
        params_list = list_plus(params_list)
        for param_index in range(len(params_list)):
            param = params_list[param_index]
            context = {
                "name": xml_tag_loader(param, ('@name', )),
                "value": xml_tag_loader(param, ('@value',)),
                "unit": xml_tag_loader(param, ('@unit',)),
                "ucd": xml_tag_loader(param, ('@ucd',)),
                'Description': xml_tag_loader(param, ('Description', )),
                'Reference': self.references_xml_to_html(xml_tag_loader(param, ('Reference',))),
            }
            pass  # TODO: figure out why I put this here...
            context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
                context['Description'], '{0}ParamModalDescription{1}'.format(param_modal_id_prefix, param_index),
                'description'
            )
            context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
                context['Reference'], '{0}ParamModalReferences{1}'.format(param_modal_id_prefix, param_index),
                'references'
            )
            markup += format_html(self.param_html, context)
            modals = modals + context['ReferenceModal'] + context['DescriptionModal']
        if markup == "":
            return markup
        context = {
            "Params": markup,
            "Modals": modals,
        }
        return format_html(self.params_html, context)

    def groups_xml_to_html(self, groups_list):
        markup = ""
        groups_list = list_plus(groups_list)
        for group_index in range(len(groups_list)):
            group = groups_list[group_index]
            context = {
                "name": xml_tag_loader(group, ('@name', )),
                "type": xml_tag_loader(group, ('@type',)),
                "Params": self.params_xml_to_html(xml_tag_loader(group, ('Param', )), "Group{0}".format(group_index)),
                'Description': xml_tag_loader(group, ('Description',)),
                'Reference': self.references_xml_to_html(xml_tag_loader(group, ('Reference',))),
            }
            pass
            context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
                context['Description'], 'GroupModalDescription{0}'.format(group_index),
                'description'
            )
            context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
                context['Reference'], 'GroupModalReferences{0}'.format(group_index),
                'references'
            )
            markup += format_html(self.group_html, context)
        if markup == "":
            return markup
        context = {
            "Groups": markup,
        }
        return format_html(self.groups_html, context)

    def tables_xml_to_html(self, tables_list,):
        markup = ""
        tables_list = list_plus(tables_list)
        for table_index in range(len(tables_list)):
            table = tables_list[table_index]
            context = {
                "Fields": self.fields_xml_to_html(xml_tag_loader(table, ('Field', )), "Table{0}".format(table_index)),
                "Data": unparse(xml_tag_loader(table, ('Data',))),
                "Params": self.params_xml_to_html(xml_tag_loader(table, ('Param', )), "Table{0}".format(table_index)),
                'Description': xml_tag_loader(table, ('Description',)),
                'Reference': self.references_xml_to_html(xml_tag_loader(table, ('Reference',))),
                "name": xml_tag_loader(table, ('@name',)),
                "type": xml_tag_loader(table, ('@type',)),
            }
            pass
            context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
                context['Description'], 'TableModalDescription{0}'.format(table_index),
                'description'
            )
            context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
                context['Reference'], 'TableModalReferences{0}'.format(table_index),
                'references'
            )
            context['FieldsModals'] = context['Fields'][1]
            context['Fields'] = context['Fields'][0]
            markup += format_html(self.table_html, context)
        if markup == "":
            return markup
        context = {
            "Tables": markup,
        }
        return format_html(self.tables_html, context)

    def fields_xml_to_html(self, fields_list, field_modal_id_prefix=""):
        markup = ""
        modals = ""
        fields_list = list_plus(fields_list)
        for field_index in range(len(fields_list)):
            field = fields_list[field_index]
            context = {
                'Description': xml_tag_loader(field, ('Description',)),
                'Reference': self.references_xml_to_html(xml_tag_loader(field, ('Reference',))),
                "name": xml_tag_loader(field, ('@name',)),
                "unit": xml_tag_loader(field, ('@unit',)),
                "ucd": xml_tag_loader(field, ('@ucd',)),
            }
            pass
            context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
                context['Description'], '{0}FieldModalDescription{1}'.format(field_modal_id_prefix, field_index),
                'description'
            )
            context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
                context['Reference'], '{0}FieldModalReferences{1}'.format(field_modal_id_prefix, field_index),
                'references'
            )
            markup += format_html(self.field_html, context)
            modals = modals + context['ReferenceModal'] + context['DescriptionModal']
        if markup == "":
            return markup
        context = {
            "Fields": markup,
        }
        return format_html(self.fields_html, context), modals

    def wherewhen_xml_to_html(self, wherewhen_dict):
        context = {
            'ObservatoryLocation': self.observatory_location_xml_to_html(
                xml_tag_loader(wherewhen_dict, ('ObsDataLocation', 'ObservatoryLocation'))
            ),
            'ObservationLocation': self.observation_location_xml_to_html(
                xml_tag_loader(wherewhen_dict, ('ObsDataLocation', 'ObservationLocation'))
            ),
            'Description': xml_tag_loader(wherewhen_dict, ('Description',)),
            'Reference': self.references_xml_to_html(xml_tag_loader(wherewhen_dict, ('Reference',))),
        }
        pass
        context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
            context['Description'], 'WhereWhenModalDescription',
            'description'
        )
        context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
            context['Reference'], 'WhereWhenModalReferences',
            'references'
        )
        return format_html(self.wherewhen_html, context)

    def observatory_location_xml_to_html(self, observatory_location_dict):
        context = {
            'AstroCoordSystem': xml_tag_loader(observatory_location_dict, ('AstroCoordSystem', '@id')),
            'AstroCoords': self.astro_coords_xml_to_html(
                xml_tag_loader(observatory_location_dict, ('AstroCoords',))
            ),
        }
        return format_html(self.observatory_location_html, context)

    def observation_location_xml_to_html(self, observation_location_dict):
        context = {
            'AstroCoordSystem': xml_tag_loader(observation_location_dict, ('AstroCoordSystem', '@id')),
            'AstroCoords': self.astro_coords_xml_to_html(
                xml_tag_loader(observation_location_dict, ('AstroCoords',))
            ),
        }
        return format_html(self.observation_location_html, context)

    def astro_coords_xml_to_html(self, astro_coords_dict):
        context = {
            'Time_TimeInstant': self.simple_row_xml_to_html('Time Instant', self.time_instant_xml_to_html(
                xml_tag_loader(astro_coords_dict, ('Time', 'TimeInstant')))
            ),
            'Time_Error': self.simple_row_xml_to_html(
                'Time Error', xml_tag_loader(astro_coords_dict, ('Time', 'Error'))
            ),
            'Time_unit': self.simple_row_xml_to_html('Time Unit', xml_tag_loader(astro_coords_dict, ('Time', '@unit'))),
            'Position2D': self.simple_row_xml_to_html(
                'Position 2D', self.position2d_xml_to_html(xml_tag_loader(astro_coords_dict, ('Position2D', )))
            ),
            'Position3D': self.simple_row_xml_to_html(
                'Position 3D', self.position3d_xml_to_html(xml_tag_loader(astro_coords_dict, ('Position3D', )))
            ),
            'coord_system_id': self.simple_row_xml_to_html(
                'Coordinate System ID', xml_tag_loader(astro_coords_dict, ('@coord_system_id', ))
            ),
        }
        return format_html(self.astro_coords_html, context)

    def time_instant_xml_to_html(self, time_instant_dict):
        context = {
            'ISOTime': xml_tag_loader(time_instant_dict, ('ISOTime', )),
            'TimeScale': xml_tag_loader(time_instant_dict, ('ISOTime',)),
            'TimeOffset': xml_tag_loader(time_instant_dict, ('TimeOffset',)),
        }
        return format_html(self.time_instant_html, context)

    def position2d_xml_to_html(self, position2d_dict):
        context = {
            'Name1': xml_tag_loader(position2d_dict, ('Name1', )),
            'Name2': xml_tag_loader(position2d_dict, ('Name2',)),
            'Value2_C1': xml_tag_loader(position2d_dict, ('Value2', 'C1')),
            'Value2_C2': xml_tag_loader(position2d_dict, ('Value2', 'C2')),
            'Error2Radius': xml_tag_loader(position2d_dict, ('Error2Radius', )),
            'unit': xml_tag_loader(position2d_dict, ('@unit',)),
        }
        return format_html(self.position2d_html, context)

    def position3d_xml_to_html(self, position3d_dict):
        context = {
            'Name1': xml_tag_loader(position3d_dict, ('Name1', )),
            'Name2': xml_tag_loader(position3d_dict, ('Name2',)),
            'Name3': xml_tag_loader(position3d_dict, ('Name3',)),
            'Value3_C1': xml_tag_loader(position3d_dict, ('Value2', 'C1')),
            'Value3_C2': xml_tag_loader(position3d_dict, ('Value2', 'C2')),
            'Value3_C3': xml_tag_loader(position3d_dict, ('Value2', 'C3')),
            'unit': xml_tag_loader(position3d_dict, ('@unit',))
        }
        return format_html(self.position3d_html, context)

    def how_xml_to_html(self, how_dict):
        context = {
            'Description': xml_tag_loader(how_dict, ('Description',)),
            'Reference': self.references_xml_to_html(xml_tag_loader(how_dict, ('Reference',))),
        }
        return format_html(self.how_html, context)

    def why_xml_to_html(self, why_dict):
        context = {
            'Description': xml_tag_loader(why_dict, ('Description',)),
            'Reference': self.references_xml_to_html(xml_tag_loader(why_dict, ('Reference',))),
            'Name': self.simple_row_xml_to_html('Name', xml_tag_loader(why_dict, ('Name',))),
            'Concept': self.simple_row_xml_to_html('Concept', xml_tag_loader(why_dict, ('Concept',))),
            'Inferences': self.inferences_xml_to_html(xml_tag_loader(why_dict, ('Inference',))),
            'importance': self.simple_row_xml_to_html('Importance', xml_tag_loader(why_dict, ('@importance',))),
            'expires': self.simple_row_xml_to_html('Expires', xml_tag_loader(why_dict, ('@expires',))),
        }
        pass
        context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
            context['Description'], 'whyModalDescription', 'description'
        )
        context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
            context['Reference'], 'whyModalDescription', 'description'
        )
        return format_html(self.why_html, context)

    def inferences_xml_to_html(self, inferences_list):
        markup = ""
        inferences_list = list_plus(inferences_list)
        for inference_index in range(len(inferences_list)):
            inference = inferences_list[inference_index]
            context = {
                'Description': xml_tag_loader(inference, ('Description',)),
                'Reference': self.references_xml_to_html(xml_tag_loader(inference, ('Reference',))),
                'Name': self.simple_row_xml_to_html('Name', xml_tag_loader(inference, ('Name',))),
                'Concept': self.simple_row_xml_to_html('Concept', xml_tag_loader(inference, ('Concept',))),
                'probability': self.simple_row_xml_to_html('Probability', xml_tag_loader(inference, ('@probability',))),
                'relation': self.simple_row_xml_to_html('Relation', xml_tag_loader(inference, ('@relation',))),
            }
            pass
            context['DescriptionIcon'], context['DescriptionModal'] = self.icon_modal_html(
                context['Description'], 'InferenceModalDescription{0}'.format(inference_index),
                'description'
            )
            context['ReferenceIcon'], context['ReferenceModal'] = self.icon_modal_html(
                context['Reference'], 'InferenceModalReferences{0}'.format(inference_index),
                'references'
            )
            markup += format_html(self.inference_html, context)
        if markup == "":
            return markup
        context = {
            "Inferences": markup,
        }
        return format_html(self.inferences_html, context)

    def citations_xml_to_html(self, citations_list):
        markup = ""
        for citation in list_plus(citations_list):
            context = {
                'Description': xml_tag_loader(citation, ('Description',)),
                'EventIVORNs': self.event_ivorns_xml_to_html(xml_tag_loader(citation, ('EventIVORN',))),
            }
            markup += format_html(self.citation_html, context)
        if markup == "":
            return markup
        context = {
            "Citations": markup,
        }
        return format_html(self.citations_html, context)

    def event_ivorns_xml_to_html(self, event_ivorns_list):
        markup = ""
        for event_ivorn in list_plus(event_ivorns_list):
            context = {
                'text': xml_tag_loader(event_ivorn, ('#text',)),
                'cite': xml_tag_loader(event_ivorn, ('@cite',)),
            }
            markup += format_html(self.event_ivorn_html, context)
        if markup == "":
            return markup
        context = {
            "Events": markup,
        }
        return format_html(self.event_ivorns_html, context)

    def references_xml_to_html(self, references_list):
        markup = ""
        for reference in list_plus(references_list):
            context = {
                'type': xml_tag_loader(reference, ('@type',)),
                'uri': xml_tag_loader(reference, ('@uri',)),
            }
            markup += format_html(self.reference_html, context)
        if markup == "":
            return markup
        context = {
            "References": markup,
        }
        return format_html(self.references_html, context)

    def icon_modal_html(self, modal_message, modal_id_str, icon_type):
        if modal_message == "":
            return "", ""
        if icon_type == 'description':
            icon_class = "glyphicon glyphicon-info-sign"
            modal_header = 'Description'
        else:
            icon_class = "glyphicon glyphicon-asterisk"
            modal_header = 'References'
        icon_context = {
            'ModalID': modal_id_str,
            'SpanClass': icon_class,
        }
        modal_context = {
            'Message': modal_message,
            'Header': modal_header,
            'ModalID': modal_id_str,
        }
        return format_html(self.icon_html, icon_context), format_html(self.modal_html, modal_context)


class BaseGCNObject(object):
    def __init__(self, message):
        self.message = message
        self.coordinates = None
        self.gcn_message = ''
        self.parse()
        self.format()

    def parse(self):
        pass

    def format(self):
        pass


class PointSourceObject(BaseGCNObject):
    pass


class ProbabilityMapObject(BaseGCNObject):
    pass


class VOEventObject(BaseGCNObject):
    pass



def get_kafka_consumer(topics=GCN['topics'], client_id=GCN['client_id'], client_secret=GCN['client_secret']):
    consumer = Consumer(client_id=client_id, client_secret=client_secret)
    consumer.subscribe(topics)
    return consumer


def parse_voevent_message(message):
    pass


def parse_message(message):
    return
