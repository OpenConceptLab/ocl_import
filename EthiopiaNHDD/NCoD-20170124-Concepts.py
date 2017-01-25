from csv_to_json_concept import csv_to_json_concept

csv_filename = 'EthiopiaNHDD/NCoD-20170124.csv'
id_column = 'concept_id'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Diagnosis'},
    {'concept_field':'datatype', 'value':'None'},
    {'concept_field':'type', 'value':'Concept'},
    {'concept_field':'owner', 'value':'EthiopiaNHDD'},
    {'concept_field':'owner_type', 'value':'Organization'},
    {'concept_field':'source', 'value':'NCoD'},
]
name_columns = [
    {'column':'Final-Name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
]
extra_columns = [
    {'value_column':'ICD10-Block', 'key':'ICD10-Block'},
    {'value_column':'ICD10-Chapter', 'key':'ICD10-Chapter'},
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
