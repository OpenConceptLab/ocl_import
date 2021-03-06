from csv_to_json_mapping import csv_to_json_mapping

INTENAL_MAPPING_ID = 'Internal'
EXTERNAL_MAPPING_ID = 'External'
csv_filename = 'EthiopiaMoh/NCoD-Sample.csv'


csv_resource_definitions = [
	{
		'definition_name':'NCoD Concept',
		'resource_type':'Concept',
		'id_column':'concept_id',
		'standard_columns':[
		    {'concept_field':'concept_class', 'value':'Diagnosis'},
		    {'concept_field':'datatype', 'value':'None'},
		],
		'name_columns':[
		    {'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
		],
		'desc_columns':[],
		'extra_columns':[
		    {'value_column':'extra_icd10_block', 'key':'ICD-10 Block'},
		    {'value_column':'extra_icd10_chapter', 'key':'ICD-10 Chapter'},
		]
	},
	{
		'definition_name':'Mapping to CIEL',
		'resource_type':'Mapping',
		'id_column':None,
		'internal_external': {'value':INTENAL_MAPPING_ID},
		'standard_columns': [
			{'mapping_field':'from_concept_url', 'column':'ncod_concept_url'},
			{'mapping_field':'map_type', 'column':'ciel_map_type'},
			{'mapping_field':'to_concept_url', 'column':'ciel_concept_url'},
		]
	},
	{
		'definition_name':'Mapping to ICD-10',
		'resource_type':'Mapping',
		'id_column':None,
		'internal_external': {'value':EXTERNAL_MAPPING_ID},
		'standard_columns': [
			{'mapping_field':'from_concept_url', 'column':'ncod_concept_url'},
			{'mapping_field':'map_type', 'column':'ciel_map_type'},
			{'mapping_field':'to_concept_url', 'column':'ciel_concept_url'},
		]
	}
]

standard_columns = [
    {'mapping_field':'from_concept_url', 'column':'ncod_concept_url'},
    {'mapping_field':''}
    {'mapping_field':'from_concept_url', 'column':'from_concept_url'},
    {'mapping_field':'extras', 'value':'None'},
]
name_columns = [
    {'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
]
extra_columns = [
    {'value_column':'extra_icd10_block', 'key':'ICD-10 Block'},
    {'value_column':'extra_icd10_chapter', 'key':'ICD-10 Chapter'},
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
