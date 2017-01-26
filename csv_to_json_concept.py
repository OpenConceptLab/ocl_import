"""
csv_to_json_mapping.py -- Convert CSV to OCL-formatted JSON concepts file
"""
import csv
import json
import re


def csv_to_json_concept(csv_filename, id_column, standard_columns=None,
                        name_columns=None, desc_columns=None, extra_columns=None):
    """ Convert CSV to OCL-formatted JSON concepts file """

    with open(csv_filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for csv_row in csv_reader:
            concept = {}

            # Concept ID column
            if id_column not in csv_row or not csv_row[id_column]:
                raise Exception('ID column %s not set or empty in row %s' % (id_column, csv_row))
            concept['id'] = format_identifier(csv_row[id_column])

            # Standard columns
            if standard_columns:
                for col in standard_columns:
                    if 'concept_field' not in col:
                        raise Exception('Expected key "concept_field" in standard column definition, but none found: %s' % col)
                    if 'column' in col:
                        concept[col['concept_field']] = csv_row[col['column']]
                    elif 'value' in col:
                        concept[col['concept_field']] = col['value']
                    else:
                        raise Exception('Expected "column" or "value" key in standard column definition, but none found: %s' % col)

            # Name columns
            if name_columns:
                concept['names'] = []
                for col in name_columns:
                    new_concept_name = col.copy()
                    new_concept_name['name'] = csv_row[col['column']]
                    del new_concept_name['column']
                    if new_concept_name['name']:
                        concept['names'].append(new_concept_name)

            # Description columns
            if desc_columns:
                concept['descriptions'] = []
                for col in desc_columns:
                    new_desc = col.copy()
                    new_desc['description'] = csv_row[col['column']]
                    del new_desc['column']
                    if new_desc['description']:
                        concept['descriptions'].append(new_desc)

            # Extra columns
            if extra_columns:
                concept['extras'] = {}
                for col in extra_columns:
                    new_extra_key = None
                    new_extra_value = None
                    if 'key_column' in col:
                        new_extra_key = csv_row[col['key_column']]
                    elif 'key' in col:
                        new_extra_key = col['key']
                    else:
                        raise Exception('Expected "key_column" or "key" key in extra column definition, but none found: %s' % col)
                    if 'value_column' in col:
                        new_extra_value = csv_row[col['value_column']]
                    elif 'value' in col:
                        new_extra_value = col['value']
                    else:
                        raise Exception('Expected "value_column" or "value" key in extra column definition, but none found: %s' % col)
                    concept['extras'][new_extra_key] = new_extra_value

            # Output
            print json.dumps(concept)

def format_identifier(unformatted_id):
    INVALID_CHARS = ' `~!@#$%^&*()_+-=[]{}\|;:"\',/<>?'
    REPLACE_CHAR = '-'
    formatted_id = list(unformatted_id)
    for index in range(len(unformatted_id)):
        if unformatted_id[index] in INVALID_CHARS:
            formatted_id[index] = REPLACE_CHAR
    return ''.join(formatted_id)
