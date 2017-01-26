'''
csv_to_json_flex.py -- Convert CSV to OCL-formatted JSON flex file
'''
import csv
import json
import re


class ocl_csv_to_json_flex:
    ''' Class to convert CSV file to OCL-formatted JSON flex file '''

    DEF_CORE_FIELDS = 'core_fields'
    DEF_SUB_RESOURCES = 'subresources'
    DEF_KEY_VALUE_PAIRS = 'key_value_pairs'

    INTERNAL_MAPPING_ID = 'Internal'
    EXTERNAL_MAPPING_ID = 'External'
    INVALID_CHARS = ' `~!@#$%^&*()_+-=[]{}\|;:"\',/<>?'
    REPLACE_CHAR = '-'


    def __init__(self, csv_filename, csv_resource_definitions,
                 verbose=False, include_type_attribute=True):
        ''' Initialize ocl_csv_to_json_flex object '''
        self.csv_filename = csv_filename
        self.csv_resource_definitions = csv_resource_definitions
        self.verbose = verbose
        self.include_type_attribute = include_type_attribute

    def process_by_row(self):
        ''' Processes the CSV file applying all definitions to each row before moving to the next row '''
        with open(self.csv_filename) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for csv_row in csv_reader:
                for csv_resource_def in self.csv_resource_definitions:
                    self.process_csv_row_with_definition(csv_row, csv_resource_def)

    def process_by_definition(self):
        ''' Processes the CSV file by looping through it entirely once for each definition '''
        for csv_resource_def in self.csv_resource_definitions:
            with open(self.csv_filename) as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for csv_row in csv_reader:
                    self.process_csv_row_with_definition(csv_row, csv_resource_def)

    def process_csv_row_with_definition(self, csv_row, csv_resource_def):
        ''' Process individual CSV row with the provided CSV resource definition '''

        # Optionally skip if specified column is empty
        if ('skip_if_empty_column' in csv_resource_def and
                csv_resource_def['skip_if_empty_column'] and
                csv_resource_def['skip_if_empty_column'] in csv_row and
                csv_row[csv_resource_def['skip_if_empty_column']] == ''):
            if self.verbose:
                print 'SKIPPING: ', csv_resource_def['definition_name']
            return

        # Set the resource type
        ocl_resource = {}
        if self.include_type_attribute:
            ocl_resource['type'] = csv_resource_def['resource_type']

        # Resource ID column
        has_id_column = False
        id_column = None
        if 'id_column' in csv_resource_def and csv_resource_def['id_column']:
            has_id_column = True
            id_column = csv_resource_def['id_column']
            if id_column not in csv_row or not csv_row[id_column]:
                raise Exception('ID column %s not set or empty in row %s' % (id_column, csv_row))
            ocl_resource['id'] = self.format_identifier(csv_row[id_column])

        # Core fields
        if self.DEF_CORE_FIELDS in csv_resource_def and csv_resource_def[self.DEF_CORE_FIELDS]:
            for field_def in csv_resource_def[self.DEF_CORE_FIELDS]:
                if 'resource_field' not in field_def:
                    raise Exception('Expected key "resource_field" in standard column definition, but none found: %s' % field_def)
                if 'column' in field_def:
                    ocl_resource[field_def['resource_field']] = csv_row[field_def['column']]
                elif 'value' in field_def:
                    ocl_resource[field_def['resource_field']] = field_def['value']
                else:
                    raise Exception('Expected "column" or "value" key in standard column definition, but none found: %s' % field_def)

        # Dictionary columns
        if self.DEF_SUB_RESOURCES in csv_resource_def and csv_resource_def[self.DEF_SUB_RESOURCES]:
            for group_name in csv_resource_def[self.DEF_SUB_RESOURCES]:
                ocl_resource[group_name] = []
                for dict_def in csv_resource_def[self.DEF_SUB_RESOURCES][group_name]:
                    current_dict = {}
                    for field_def in dict_def:
                        if 'resource_field' not in field_def:
                            raise Exception('Expected key "resource_field" in subresource definition, but none found: %s' % field_def)
                        if 'column' in field_def:
                            current_dict[field_def['resource_field']] = csv_row[field_def['column']]
                        elif 'value' in field_def:
                            current_dict[field_def['resource_field']] = field_def['value']
                        else:
                            raise Exception('Expected "column" or "value" key in subresource definition, but none found: %s' % field_def)
                    if current_dict:
                        ocl_resource[group_name].append(current_dict)

        # Key value pairs
        if self.DEF_KEY_VALUE_PAIRS in csv_resource_def and csv_resource_def[self.DEF_KEY_VALUE_PAIRS]:
            for group_name in csv_resource_def[self.DEF_KEY_VALUE_PAIRS]:
                ocl_resource[group_name] = {}
                for kvp_def in csv_resource_def[self.DEF_KEY_VALUE_PAIRS][group_name]:
                    # Key
                    key = None
                    if 'key' in kvp_def and kvp_def['key']:
                        key = kvp_def['key']
                    elif 'key_column' in kvp_def and kvp_def['key_column']:
                        if kvp_def['key_column'] in csv_row and csv_row[kvp_def['key_column']]:
                            key = csv_row[kvp_def['key_column']]
                        else:
                            raise Exception('key_column "%s" must be non-empty in CSV within key_value_pair: %s' % (kvp_def['key_column'], kvp_def))
                    else:
                        raise Exception('Expected "key" or "key_column" key in key_value_pair definition, but neither found: %s' % kvp_def)

                    # Value
                    if 'value' in kvp_def:
                        value = kvp_def['value']
                    elif 'value_column' in kvp_def and kvp_def['value_column']:
                        if kvp_def['value_column'] in csv_row:
                            value = csv_row[kvp_def['value_column']]
                        else:
                            raise Exception('value_column "%s" does not exist in CSV for key_value_pair: %s' % (kvp_def['value_column'], kvp_def))
                    else:
                        raise Exception('Expected "value" or "value_column" key in key_value_pair definition, but neither found: %s' % kvp_def)

                    # Set the key-value pair
                    ocl_resource[group_name][key] = value

        # Output
        print json.dumps(ocl_resource)


    def format_identifier(self, unformatted_id):
        ''' Format a string according to the OCL ID rules '''
        formatted_id = list(unformatted_id)
        for index in range(len(unformatted_id)):
            if unformatted_id[index] in self.INVALID_CHARS:
                formatted_id[index] = self.REPLACE_CHAR
        return ''.join(formatted_id)

