'''
OCL Flexible JSON Importer -- 
Script that uses the OCL API to import multiple resource types from a JSON lines file.
Configuration for individual resources can generally be set inline in the JSON.

Resources currently supported:
* Sources
* Organizations
* Concepts

Resources that will be supported in the future:
* Collections
* Mappings
* References

Deviations from OCL API responses:
* Sources/Collections:
    - "supported_locales" response is a list, but only a comma-separated string is supported when posted
'''

import json
import requests
import settings
import sys
from pprint import pprint


# Owner fields: ( owner AND owner_type ) OR ( owner_url )
# Repository fields: ( source ) OR ( source_url )
# Concept/Mapping field: ( id ) OR ( url )


class ImportError(Exception):
    """ Base exception for this module """
    pass

class UnexpectedStatusCodeError(ImportError):
    """ Exception raised for unexpected status code """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class InvalidOwnerError(ImportError):
    """ Exception raised when owner information is invalid """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class InvalidSourceError(ImportError):
    """ Exception raised when source information is invalid """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ocl_json_flex_import:
    ''' Class to flexibly import multiple resource types into OCL from JSON lines files using OCL API '''

    OBJ_TYPE_USER = 'User'
    OBJ_TYPE_ORGANIZATION = 'Organization'
    OBJ_TYPE_SOURCE = 'Source'
    OBJ_TYPE_COLLECTION = 'Collection'
    OBJ_TYPE_CONCEPT = 'Concept'
    OBJ_TYPE_MAPPING = 'Mapping'
    OBJ_TYPE_REFERENCE = 'Reference'

    obj_def = {
        OBJ_TYPE_ORGANIZATION: {
            "id_field": "id",
            "url_name": "orgs",
            "has_owner": False,
            "has_source": False,
            "allowed_fields": ["id", "company", "extras", "location", "name", "public_access", "website"]
        },
        OBJ_TYPE_SOURCE: {
            "id_field": "id",
            "url_name": "sources",
            "has_owner": True,
            "has_source": False,
            "allowed_fields": ["id", "short_code", "name", "full_name", "description", "source_type", "custom_validation_schema", "public_access", "default_locale", "supported_locales", "website", "extras", "external_id"],
        },
        OBJ_TYPE_CONCEPT: {
            "id_field": "id",
            "url_name": "concepts",
            "has_owner": True,
            "has_source": True,
            "allowed_fields": ["id", "external_id", "concept_class", "datatype", "names", "descriptions", "retired", "extras"],
        },
    }
    #    OBJ_TYPE_MAPPING: {
    #        "id_field": "id",
    #        "url_name": "mappings",
    #        "has_owner": True,
    #        "has_source": True,
    #        "allowed_fields": ["id", "short_code", "name", "full_name", "description", "source_type", "custom_validation_schema", "public_access", "default_locale", "supported_locales", "website", "extras", "external_id"],
    #    }


    def __init__(self, file_path='', api_url_root='', api_token='',
                 test_mode=False, do_update_if_exists=False):
        ''' Initialize the ocl_json_flex_import object '''

        self.file_path = file_path
        self.api_token = api_token
        self.api_url_root = api_url_root
        self.test_mode = test_mode
        self.do_update_if_exists = do_update_if_exists

        self.cache_obj_exists = {}

        # Prepare the headers
        self.api_headers = {
            'Authorization': 'Token ' + self.api_token,
            'Content-Type': 'application/json'
        }


    def process(self):
        ''' Processes an import file '''
        # Display global settings
        print "**** GLOBAL SETTINGS ****"
        print "    API Root URL:", self.api_url_root
        print "    API Token:", self.api_token
        print "    Import File:", self.file_path
        print "    Test Mode:", self.test_mode
        print ""

        # Loop through each JSON object in the file
        with open(self.file_path) as json_file:
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
                print "\n\n"


    def does_object_exist(self, obj_url):
        ''' Returns whether an object at the specified URL already exists '''

        # If obj existence cached, then just return True
        if obj_url in self.cache_obj_exists and self.cache_obj_exists[obj_url]:
            return True

        # Object existence not cached, so use API to check if it exists
        request_existence = requests.head(self.api_url_root + obj_url, headers=self.api_headers)
        if request_existence.status_code == requests.codes.ok:
            self.cache_obj_exists[obj_url] = True
            return True
        elif request_existence.status_code == requests.codes.not_found:
            return False
        else:
            raise UnexpectedStatusCodeError(
                "GET " + self.api_url_root + obj_url,
                "Unexpected status code returned: " + str(request_existence.status_code))


    def process_object(self, obj_type, obj):
        ''' Processes an individual document in the import file '''

        # Grab the ID
        obj_id = None
        if self.obj_def["Source"]["id_field"] in obj:
            obj_id = obj[self.obj_def["Source"]["id_field"]]

        # Set owner URL -- e.g. /users/johndoe/ OR /orgs/MyOrganization/
        # NOTE: Owner URL always ends with a forward slash
        has_owner = False
        obj_owner_url = None
        if self.obj_def[obj_type]["has_owner"]:
            has_owner = True
            if "owner_url" in obj:
                obj_owner_url = obj.pop("owner_url")
                obj.pop("owner", None)
                obj.pop("owner_type", None)
            elif "owner" in obj and "owner_type" in obj:
                obj_owner_type = obj.pop("owner_type")
                obj_owner = obj.pop("owner")
                if obj_owner_type == self.OBJ_TYPE_ORGANIZATION:
                    obj_owner_url = "/" + self.obj_def[self.OBJ_TYPE_ORGANIZATION]["url_name"] + "/" + obj_owner + "/"
                elif obj_owner_url == self.OBJ_TYPE_USER:
                    obj_owner_url = "/" + self.obj_def[self.OBJ_TYPE_USER]["url_name"] + "/" + obj_owner + "/"
                else:
                    raise InvalidOwnerError(obj, "Valid owner information required for object of type '" + obj_type + "'")
            else:
                raise InvalidOwnerError(obj, "Valid owner information required for object of type '" + obj_type + "'")

        # Set source URL -- e.g. /orgs/MyOrganization/sources/MySource/
        # NOTE: Source URL always ends with a forward slash
        has_source = False
        obj_source_url = None
        if self.obj_def[obj_type]["has_source"]:
            has_source = True
            if "source_url" in obj:
                obj_source_url = obj.pop("source_url")
                obj.pop("source", None)
            elif "source" in obj:
                obj_source_url = obj_owner_url + 'sources/' + obj.pop("source") + "/"
            else:
                raise InvalidSourceError(obj, "Valid source information required for object of type '" + obj_type + "'")

        # Build object URLs -- note that these always end with forward slashes
        if has_source:
            # Concept, mapping, reference, etc.
            new_obj_url = obj_source_url + self.obj_def[obj_type]["url_name"] + "/"
            obj_url = new_obj_url + obj_id + "/"
        elif has_owner:
            # Repository (Source or collection)
            new_obj_url = obj_owner_url + self.obj_def[obj_type]["url_name"] + "/"
            obj_url = new_obj_url + obj_id + "/"
        else:
            # Organization
            new_obj_url = '/' + self.obj_def[obj_type]["url_name"] + "/"
            obj_url = new_obj_url + obj_id + "/"

        # Pull out the fields that aren't allowed
        obj_not_allowed = {}
        for k in obj.keys():
            if k not in self.obj_def[obj_type]["allowed_fields"]:
                obj_not_allowed[k] = obj.pop(k)

        # Display some debug info
        print "**** " + self.api_url_root + obj_url + " ****"
        print "** Allowed Fields: **", json.dumps(obj)
        print "** Removed Fields: **", json.dumps(obj_not_allowed)

        # Check if owner exists
        if has_owner and obj_owner_url:
            try:
                if self.does_object_exist(obj_owner_url):
                    print "** INFO: Owner exists at: " + obj_owner_url
                else:
                    print "** SKIPPING: Owner does not exist at: " + obj_owner_url
                    return
            except UnexpectedStatusCodeError as e:
                print "** SKIPPING: Unexpected error occurred: ", e.expression, e.message
                return

        # Check if source exists
        if has_source and obj_source_url:
            try:
                if self.does_object_exist(obj_source_url):
                    print "** INFO: Source exists at: " + obj_source_url
                else:                
                    print "** SKIPPING: Source does not exist at: " + obj_source_url
                    return
            except UnexpectedStatusCodeError as e:
                print "** SKIPPING: Unexpected error occurred: ", e.expression, e.message
                return

        # Check if object already exists: GET self.api_url_root + obj_url
        print "GET " + self.api_url_root + obj_url
        try:
            obj_already_exists = self.does_object_exist(obj_url)
        except UnexpectedStatusCodeError as e:
            print "** SKIPPING: Unexpected error occurred: ", e.expression, e.message
            return
        if obj_already_exists and not self.do_update_if_exists:
            print "** SKIPPING: Object already exists at: " + self.api_url_root + obj_url
        elif obj_already_exists:
            print "** INFO: Object already exists at: " + self.api_url_root + obj_url
        else:
            print "** INFO: Object does not exist so we'll create it at: " + self.api_url_root + obj_url

        # TODO: Validate the JSON object

        # Create/update the object
        self.update_or_create(
            obj_type=obj_type, obj_id=obj_id,
            obj_owner_url=obj_owner_url, obj_source_url=obj_source_url,
            obj_url=obj_url, new_obj_url=new_obj_url,
            obj_already_exists=obj_already_exists,
            obj=obj, obj_not_allowed=obj_not_allowed)


    def update_or_create(self, obj_type='', obj_id='', obj_owner_url='', obj_source_url='',
                         obj_url='', new_obj_url='', obj_already_exists=False,
                         obj=None, obj_not_allowed=None):
        ''' Posts an object to the OCL API as either an update or create '''

        # Determine which URL to use based on whether or not object already exists
        if obj_already_exists:
            url = obj_url
        else:
            url = new_obj_url

        # Get out of here if in test mode
        if self.test_mode:
            print "[TEST MODE] POST " + self.api_url_root + url + '  ' + json.dumps(obj)
            return

        # Skip updates for now
        if obj_already_exists:
            print "[SKIPPING UPDATE] POST " + self.api_url_root + url + '  ' + json.dumps(obj)
            return

        # Create or update the object
        print "POST " + self.api_url_root + url + '  ' + json.dumps(obj)
        request_post = requests.post(self.api_url_root + url, headers=self.api_headers,
                                     data=json.dumps(obj))
        print "STATUS CODE:", request_post.status_code
        print request_post.headers
        print request_post.text
        request_post.raise_for_status()



ocl_importer = ocl_json_flex_import(
    file_path=settings.import_file_path, api_token=settings.api_token,
    api_url_root=settings.api_url_root, test_mode=settings.test_mode,
    do_update_if_exists=settings.do_update_if_exists)
ocl_importer.process()
