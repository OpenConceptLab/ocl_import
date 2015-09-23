from csv_to_json_concept import csv_to_json_concept

csv_filename = 'OCL_Locales/locales.csv'
id_column = 'ISO-639-2.1'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Locale'},
    {'concept_field':'datatype', 'value':'N/A'},
]
name_columns = [
    {'column':'en_name_preferred', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
    {'column':'en_name_non_preferred_1', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'en_name_non_preferred_2', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'en_name_non_preferred_3', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'en_name_non_preferred_4', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'en_name_non_preferred_5', 'locale':'en', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'fr_name_preferred', 'locale':'fr', 'locale_preferred':"True", 'name_type':'Fully Specified'},
    {'column':'fr_name_non_preferred_1', 'locale':'fr', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'fr_name_non_preferred_2', 'locale':'fr', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'fr_name_non_preferred_3', 'locale':'fr', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'fr_name_non_preferred_4', 'locale':'fr', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'fr_name_non_preferred_5', 'locale':'fr', 'locale_preferred':False, 'name_type':'Designated Synonym'},
    {'column':'ISO-639-2.1', 'locale':'en', 'locale_preferred':False, 'name_type':'ISO 639-2'},
    {'column':'ISO-639-2.2', 'locale':'en', 'locale_preferred':False, 'name_type':'ISO 639-2 Non-preferred'},
    {'column':'ISO-639-1', 'locale':'en', 'locale_preferred':False, 'name_type':'ISO 639-1'},
]
desc_columns = []
extra_columns = []

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
