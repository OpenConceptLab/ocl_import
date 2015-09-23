from csv_to_json_concept import csv_to_json_concept

csv_filename = 'OCL_Datatypes/OCL_Datatypes.csv'
id_column = 'name'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Datatype'},
    {'concept_field':'datatype', 'value':'N/A'},
    {'concept_field':'external_id', 'column':'external_id'},
]
name_columns = [
    {'column':'name', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
    {'column':'name_2', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'hl7_abbreviation', 'locale':'en', 'locale_preferred':False, 'name_type':'HL7 Abbreviation'},
]
desc_columns = [
    {'column':'description', 'locale':'en', 'locale_preferred':"True"},
]
extra_columns = []

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
