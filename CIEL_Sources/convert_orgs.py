from csv_to_json_concept import csv_to_json_concept

csv_filename = 'CIEL_Sources/orgs.csv'
id_column = 'org_short_name'
standard_columns = [
    {'concept_field':'type', 'value':'Organization'},
    {'concept_field':'id', 'column':'org_short_name'},
    {'concept_field':'name', 'column':'org_full_name'},
    {'concept_field':'website', 'column':'website'},
    {'concept_field':'company', 'column':'company_name'},
    {'concept_field':'location', 'column':'location'},
]
name_columns = [
    #{'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
    #{'column':'description', 'locale':'en', 'locale_preferred':"True"},
]
extra_columns = [
	{'value_column':'extra: resource_about', 'key':'about'}
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
