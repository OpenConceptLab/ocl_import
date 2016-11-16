from csv_to_json_concept import csv_to_json_concept

csv_filename = 'EthiopiaNHDD/NCoD-Concepts.csv'
id_column = 'concept_id'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Diagnosis'},
    {'concept_field':'datatype', 'value':'None'},
]
name_columns = [
    {'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
]
extra_columns = [
    {'value_column':'extra_icd10_block', 'key':'ICD10-Block'},
    {'value_column':'extra_icd10_chapter', 'key':'ICD10-Chapter'},
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
