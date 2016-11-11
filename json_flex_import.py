'''
OCL Flexible JSON Importer -- 
Script that uses the OCL API to import multiple resource types from a JSON lines file.
Resources currently supported: Sources

Deviations from OCL API responses:
* Sources/Collections:
    - "supported_locales" response is a list, but only a comma-separated string is supported when posted
'''
import json
import requests
from pprint import pprint


api_token_showcase_root = ''
api_token_showcase_paynejd = ''
api_token_staging_root = '23c5888470d4cb14d8a3c7f355f4cdb44000679a'
api_token_staging_paynejd = 'a61ba53ed7b8b26ece8fcfc53022b645de0ec055'
api_token_production_root = '230e6866c2037886909c58d8088b1a5e7cabc74b'
api_token_production_paynejd = '950bd651dc4ee29d6bcee3e6dacfe7834bb0f881'


file_path = 'CIEL_Sources/sources.json'
api_token = api_token_production_root
api_url_root = 'https://api.openconceptlab.org'
test_mode = False


class ocl_json_flex_import:
    ''' Class to flexibly import multiple resource types into OCL from JSON Lines files '''

    OBJ_TYPE_USER = 'User'
    OBJ_TYPE_ORGANIZATION = 'Organization'
    OBJ_TYPE_SOURCE = 'Source'
    OBJ_TYPE_COLLECTION = 'Collection'
    OBJ_TYPE_CONCEPT = 'Concept'
    OBJ_TYPE_MAPPING = 'Mapping'
    OBJ_TYPE_REFERENCE = 'Reference'

    obj_def = {
        OBJ_TYPE_SOURCE: {
            "id_field": "id",
            "url_name": "sources",
            "has_owner": True,
            "has_source": False,
            "allowed_fields": ["id", "short_code", "name", "full_name", "description", "source_type", "custom_validation_schema", "public_access", "default_locale", "supported_locales", "website", "extras", "external_id"],
        },
    }
    '''
        OBJ_TYPE_COLLECTION: {
            "id_field": "id",
            "url_name": "collections",
            "has_owner": True,
            "has_source": False,
            "allowed_fields": ["name", "full_name", "description", "collection_type", "custom_validation_schema", "public_access", "default_locale", "supported_locales", "website", "extras", "external_id"],
        },
        OBJ_TYPE_CONCEPT: {
            "id_field": "id",
            "url_name": "concepts",
            "has_owner": True,
            "has_source": True,
        }
    }
    '''


    def __init__(self, file_path='', api_url_root='', api_token='', test_mode=False):
        self.file_path = file_path
        self.api_token = api_token
        self.api_url_root = api_url_root
        self.test_mode = test_mode


    def process(self):
        # Loop through each JSON object in the file
        with open(file_path) as json_file:
            for json_line_raw in json_file:
                json_line_obj = json.loads(json_line_raw)
                if "type" in json_line_obj:
                    obj_type = json_line_obj.pop("type")
                    if obj_type in self.obj_def.keys():
                        self.process_object(obj_type, json_line_obj)
                    else:
                        print "SKIPPING: Unrecognized 'type' attribute '" + obj_type + "' for object: " + json_line_raw
                else:
                    print "SKIPPING: No 'type' attribute: " + json_line_raw
                print "\n\n\n"


    def process_object(self, obj_type, obj):
        # Grab the ID
        obj_id = None
        if self.obj_def["Source"]["id_field"] in obj:
            obj_id = obj[self.obj_def["Source"]["id_field"]]

        # Grab owner info
        has_owner = False
        obj_owner_url = None
        if self.obj_def["Source"]["has_owner"]:
            has_owner = True
            if "owner_url" in obj:
                # relative url
                obj_owner_url = obj.pop("owner_url")
                obj.pop("owner", None)
                obj.pop("owner_type", None)

            elif "owner" in obj and "owner_type" in obj:
                obj_owner_type = obj.pop("owner_type")
                obj_owner = obj.pop("owner")
                if obj_owner_type == 'Organization':
                    obj_owner_url = "/orgs/" + obj_owner
                elif obj_owner_url == 'User':
                    obj_owner_url = "/users/" + obj_owner
                else:
                    #throw error
                    pass

            else:
                #throw error
                pass

        # Grab the source info
        has_source = False
        obj_source = None
        if self.obj_def["Source"]["has_source"]:
            #has_source = True
            pass
        else:
            pass

        # Pull out the fields that aren't allowed
        obj_not_allowed = {}
        for k in obj.keys():
            if k in self.obj_def["Source"]["allowed_fields"]:
                #print "Allowed: " + k
                pass
            else:
                obj_not_allowed[k] = obj.pop(k)

        # Route to the appropriate method for type-based handling
        if obj_type == self.OBJ_TYPE_CONCEPT:
            self.process_concept(obj)
        elif obj_type == self.OBJ_TYPE_SOURCE:
            self.process_source(obj_type, obj_id, obj_owner_url, obj, obj_not_allowed)
        elif obj_type == self.OBJ_TYPE_ORGANIZATION:
            self.process_organization(obj)
        elif obj_type == self.OBJ_TYPE_MAPPING:
            self.process_mapping(obj)
        elif obj_type == self.OBJ_TYPE_COLLECTION:
            self.process_collection(obj)
        elif obj_type == self.OBJ_TYPE_REFERENCE:
            self.process_reference(obj)


    def process_concept(self, json_obj, obj_id=None):
        #print(json_obj["datatype"])
        pass


    def process_mapping(self, json_obj, obj_id=None):
        #print(json_obj["from_concept"])
        pass


    def process_reference(self, json_obj, obj_id=None):
        #print(json_obj["expression"])
        pass


    def process_source(self, obj_type, obj_id, obj_owner_url, obj, obj_not_allowed):
        # Prepare the API request
        new_obj_url = obj_owner_url + '/' + self.obj_def[obj_type]["url_name"] + "/"
        obj_url = new_obj_url + obj_id + "/"
        headers = {
            'Authorization': 'Token ' + self.api_token,
            'Content-Type': 'application/json'
        }

        # Display some debug info
        print " ----- " + obj_url + " ----- "
        print "** Allowed Fields: **"
        print json.dumps(obj)
        print "** Removed Fields: **"
        print json.dumps(obj_not_allowed)

        # Check if it exists: GET self.api_url_root + obj_url
        r1 = requests.get(self.api_url_root + obj_url, headers=headers)
        if r1.status_code == requests.codes.ok:
            # Object exists, so skip for now -- in the future, can optionally perform an update
            print "** SKIPPING: Object already exists at: " + self.api_url_root + obj_url
        elif r1.status_code == requests.codes.not_found:
            # Object does not exist, so create it
            print "** Object does not exist at: " + self.api_url_root + obj_url

            # Make sure that the owner exists, and skip if not
            r2 = requests.get(self.api_url_root + obj_owner_url + '/', headers=headers)
            if r2.status_code == requests.codes.ok:
                print "** Owner exists: " + obj_owner_url + '/ -- we can move forward' 
            else:
                print "** SKIPPING: Owner does not exist: " + obj_owner_url
                return

            # Create the object
            print "POST " + self.api_url_root + new_obj_url + '  ' + json.dumps(obj)
            if not self.test_mode:
                r3 = requests.post(self.api_url_root + new_obj_url, headers=headers, data=json.dumps(obj))
                if r3.status_code == requests.codes.created:
                    print "CREATED 201"
                    print r3.text
                else:
                    print r3.headers
                    print r3.text
                    r3.raise_for_status()
        else:
            print "** SKIPPING: Something happened with status code: " + r1.status_code


    def process_collection(self, json_obj, obj_id=None):
        #print(obj["name"])
        pass


    def process_organization(self, json_obj, obj_id=None):
        #print(obj["name"])
        pass


ocl_importer = ocl_json_flex_import(
    file_path=file_path, api_token=api_token,
    api_url_root=api_url_root, test_mode=test_mode)
ocl_importer.process()
