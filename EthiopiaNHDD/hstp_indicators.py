from csv_to_json_concept import csv_to_json_concept

csv_filename = 'EthiopiaMoh/hstp_indicators.csv'
id_column = 'Indicator ID'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Indicator'},
    {'concept_field':'datatype', 'column':'Datatype'},
]
name_columns = [
    {'column':'Indicator Title', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = []
extra_columns = [
    {'value_column':'Indicator Type', 'key':'Indicator Type'},
    {'value_column':'HSTP Category 1', 'key':'HSTP-Category-1'},
    {'value_column':'HSTP Category 2', 'key':'HSTP-Category-2'},
    {'value_column':'Baseline', 'key':'Baseline'},
    {'value_column':'Yearly Target 1', 'key':'Yearly-Target-1'},
    {'value_column':'Yearly Target 2', 'key':'Yearly-Target-2'},
    {'value_column':'Yearly Target 3', 'key':'Yearly-Target-3'},
    {'value_column':'Yearly Target 4', 'key':'Yearly-Target-4'},
    {'value_column':'Yearly Target 5', 'key':'Yearly-Target-5'},
    {'value_column':'Data Source', 'key':'Data Source'},
    {'value_column':'Periodicity', 'key':'Periodicity'},
    {'value_column':'Level of Data Collection', 'key':'Level of Data Collection'},
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
