from csv_to_json_concept import csv_to_json_concept

csv_filename = 'EthiopiaMoh/hmis_indicators.csv'
id_column = 'Indicator ID'
standard_columns = [
    {'concept_field':'concept_class', 'value':'Indicator'},
    {'concept_field':'datatype', 'column':'Datatype'},
]
name_columns = [
    {'column':'Indicator Title', 'locale':'en', 'locale_preferred':"True", 'name_type':'Fully Specified'},
]
desc_columns = [
    {'column':'Definition', 'locale':'en', 'locale_preferred':"True"},
]
extra_columns = [
    {'value_column':'Formula: Numerator', 'key':'Numerator'},
    {'value_column':'Formula: Denominator', 'key':'Denominator'},
    {'value_column':'Formula: Multiplier', 'key':'Multiplier'},
    {'value_column':'Interpretation', 'key':'Interpretation'},
    {'value_column':'Disaggregation', 'key':'Disaggregation'},
    {'value_column':'Primary Sources', 'key':'Primary Sources'},
    {'value_column':'Reporting Frequency', 'key':'Reporting Frequency'},
    {'value_column':'Applicable Reporting Units', 'key':'Applicable Reporting Units'},
    {'value_column':'HMIS Category 1', 'key':'HMIS-Category-1'},
    {'value_column':'HMIS Category 2', 'key':'HMIS-Category-2'},
    {'value_column':'HMIS Category 3', 'key':'HMIS-Category-3'},
    {'value_column':'HMIS Category 4', 'key':'HMIS-Category-4'},
]

csv_to_json_concept(
    csv_filename, id_column, standard_columns=standard_columns,
    name_columns=name_columns, desc_columns=desc_columns, extra_columns=extra_columns)
