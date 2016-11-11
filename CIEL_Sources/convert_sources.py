from csv_to_json_concept import csv_to_json_concept

csv_filename = 'CIEL_Sources/sources.csv'
id_column = 'short_code'
standard_columns = [
    {'concept_field':'short_code', 'column':'short_code'},
    {'concept_field':'type', 'column':'repository_type'},
    {'concept_field':'owner', 'column':'owner'},
    {'concept_field':'owner_type', 'column':'owner_type'},
    {'concept_field':'name', 'column':'name'},
    {'concept_field':'full_name', 'column':'full_name'},
    {'concept_field':'description', 'column':'description'},
    {'concept_field':'source_type', 'column':'source_type'},
    {'concept_field':'public_access', 'column':'public_access'},
    {'concept_field':'website', 'column':'website'},
    {'concept_field':'default_locale', 'column':'default_locale'},
    {'concept_field':'supported_locales', 'column':'supported_locales'},
    {'concept_field':'external_id', 'column':'external_id'},
]
name_columns = [
    #{'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
    #{'column':'description', 'locale':'en', 'locale_preferred':"True"},
]
extra_columns = [
	{'value_column':'extra: hl7_code', 'key':'hl7_code'}
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
