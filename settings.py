'''
Settings for OCL Flexible JSON Importer
'''


# File to be imported
file_path = 'import_file.json'

# API Token of the user account to use for importing
api_token = 'api_token_goes_here'

# URL root
api_url_showcase = 'https://api.openconceptlab.org'
api_url_staging = 'https://api.staging.openconceptlab.org'
api_url_production = 'http://api.showcase.openconceptlab.org'
api_url_root = api_url_staging

# Set to True to allow updates to existing objects
do_update_if_exists = False

# Test mode -- set to True to process the file without actually importing
test_mode = True
