# ocl_import
This repository is intended to help generate OCL imports from a variety of 
sources, excluding OpenMRS (see the `ocl_ciel_import` repo for that).

Currently, there is a script that accepts CSV files and converts them to the
required JSON format that OCL uses to import concepts using the `import_concepts_to_source`
management command in the `oclapi` repo.

Additional scripts to generate other resource types, esp. mappings, and to accept
other source types may be developed.

Metadata sources, including Classes, Datatypes, Map Types, Name Types, and Source Types,
originate from the 2015-08-24 CIEL OpenMRS dictionary.

Locales come from the ISO 632.1 and 632.2 data sources.

WHO-ICD-10 were downloaded from the WHO ICD downloads section on 2015-03.
