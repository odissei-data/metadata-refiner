import re

from utils import add_contact_email


def refine_dataverse_nl_metadata(metadata: dict) -> dict:
    metadata = add_contact_email(metadata, "portal@odissei.nl")

    if 'metadataLanguage' in metadata and metadata[
        'metadataLanguage'] == 'undefined':
        del metadata['metadataLanguage']

    metadata_blocks = metadata['datasetVersion']['metadataBlocks']
    dataset_version = {'metadataBlocks': metadata_blocks}
    if 'termsOfUse' in metadata['datasetVersion']:
        dataset_version['termsOfUse'] = metadata['datasetVersion'][
            'termsOfUse']
    if 'termsOfAccess' in metadata['datasetVersion']:
        dataset_version['termsOfAccess'] = metadata['datasetVersion'][
            'termsOfAccess']

    if 'license' in metadata['datasetVersion'] and metadata['datasetVersion'][
        'license'] != 'NONE':
        dataset_version['license'] = format_license(
            metadata['datasetVersion']['license']
        )
    metadata['datasetVersion'] = dataset_version

    return metadata


def format_license(ds_license):
    if ds_license == 'CC0':
        ds_license = 'CC0 1.0'
    elif 'uri' in ds_license:
        ds_license = retrieve_license_name(ds_license['uri'])
    return ds_license


def retrieve_license_name(license_string):
    dataset_lic = ''
    if re.search(r'creativecommons', license_string):
        if re.search(r'/by/4\.0', license_string):
            dataset_lic = "CC BY 4.0"
        elif re.search(r'/by-nc/4\.0', license_string):
            dataset_lic = "CC BY-NC 4.0"
        elif re.search(r'/by-sa/4\.0', license_string):
            dataset_lic = "CC BY-SA 4.0"
        elif re.search(r'/by-nc-sa/4\.0', license_string):
            dataset_lic = "CC BY-NC-SA 4.0"
        elif re.search(r'/by-nc-nd/4\.0', license_string):
            dataset_lic = "CC BY-NC-ND 4.0"
        elif re.search(r'zero/1\.0', license_string):
            dataset_lic = "CC0 1.0"
    elif re.search(r'10\.17026/fp39-0x58', license_string):
        dataset_lic = "DANS Licence"
    return dataset_lic
