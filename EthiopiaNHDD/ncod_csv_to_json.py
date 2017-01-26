from csv_to_json_flex import ocl_csv_to_json_flex


csv_filename = 'EthiopiaNHDD/NCoD-20170124.csv'


csv_resource_definitions = [
	{
		'definition_name':'NCoD Concept',
		'resource_type':'Concept',
		'id_column':'concept_id',
		'skip_if_empty_column':'concept_id',
		ocl_csv_to_json_flex.DEF_CORE_FIELDS:[
			{'resource_field':'concept_class', 'value':'Diagnosis'},
			{'resource_field':'datatype', 'value':'None'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'source', 'value':'NCoD'},
		],
		ocl_csv_to_json_flex.DEF_SUB_RESOURCES:{
			'names':[
				[
					{'resource_field':'name', 'column':'Final-Name'},
					{'resource_field':'locale', 'value':'en'},
					{'resource_field':'locale_preferred', 'value':'True'},
					{'resource_field':'name_type', 'value':'Fully Specified'},
				],
			],
			'descriptions':[]
		},
		ocl_csv_to_json_flex.DEF_KEY_VALUE_PAIRS:{
			'extras': [
				{'key':'ICD-10 Block', 'value_column':'ICD10-Block'},
				{'key':'ICD-10 Chapter', 'value_column':'ICD10-Chapter'},
			]
		}
	},
	{
		'definition_name':'External Mapping to ICD-10',
		'resource_type':'Mapping',
		'skip_if_empty_column':'ICD10 Map Code',
		'core_fields': [
			{'resource_field':'from_concept_url', 'column':'concept_url'},
			{'resource_field':'map_type', 'column':'ICD10 Map Type'},
			{'resource_field':'to_source_url', 'value':'/orgs/WHO/sources/ICD-10-WHO/'},
			{'resource_field':'to_concept_code', 'column':'ICD10 Map Code'},
			{'resource_field':'to_concept_name', 'column':'ICD10 Map Name'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'source', 'value':'NCoD'},
		]
	},
	{
		'definition_name':'Internal Mapping to CIEL',
		'resource_type':'Mapping',
		'skip_if_empty_column':'ciel_map_url',
		'core_fields': [
			{'resource_field':'from_concept_url', 'column':'concept_url'},
			{'resource_field':'map_type', 'value':'SAME-AS'},
			{'resource_field':'to_concept_url', 'column':'ciel_map_url'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'source', 'value':'NCoD'},
		]
	},
	{
		'definition_name':'NCoD Extended Edition',
		'resource_type':'Reference',
		'skip_if_empty_column':'Extended_ID',
		'core_fields': [
			{'resource_field':'expression', 'column':'concept_url'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'collection', 'value':'NCoD-Extended'},
		]
	},
	{
		'definition_name':'NCoD Compact Edition',
		'resource_type':'Reference',
		'skip_if_empty_column':'Compact_ID',
		'core_fields': [
			{'resource_field':'expression', 'column':'concept_url'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'collection', 'value':'NCoD-Compact'},
		]
	},
	{
		'definition_name':'NCoD Mini Edition',
		'resource_type':'Reference',
		'skip_if_empty_column':'Mini_ID',
		'core_fields': [
			{'resource_field':'expression', 'column':'concept_url'},
			{'resource_field':'owner', 'value':'EthiopiaNHDD'},
			{'resource_field':'owner-type', 'value':'Organization'},
			{'resource_field':'collection', 'value':'NCoD-Mini'},
		]
	},
]

csv_converter = ocl_csv_to_json_flex(csv_filename, csv_resource_definitions, verbose=False)
csv_converter.process_by_definition()

