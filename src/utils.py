import csv
import re
from typing import Callable
from urllib.parse import urlparse

from fastapi import HTTPException


def add_contact_email(metadata: dict, contact_email: str) -> dict:
    """ Adds a contact email to dataverse JSON.

    If metadata exported from a Dataverse is missing the contact email,
    add_contact_email can be used to add a contact email.

    :param contact_email: Standard contact email to use.
    :param metadata: Dataverse JSON that is missing the contact email.
    :return: dataverse JSON with the contact email added.
    """
    fields = metadata['datasetVersion']['metadataBlocks']['citation'][
        'fields']
    dataset_contact = next((field for field in fields if
                            field.get('typeName') == 'datasetContact'), None)
    if dataset_contact:
        for dataset_contact in dataset_contact["value"]:
            dataset_contact["datasetContactEmail"] = {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": contact_email
            }
    else:
        fields.append({
            "typeName": "datasetContact",
            "multiple": True,
            "typeClass": "compound",
            "value": [
                {
                    "datasetContactEmail": {
                        "typeName": "datasetContactEmail",
                        "multiple": False,
                        "typeClass": "primitive",
                        "value": contact_email
                    }
                }
            ]
        })
    return metadata


def csv_to_dict(filename: str) -> dict:
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # skip header row if present
        return {row[1]: row[0] for row in reader if len(row) >= 2}


def get_field(typename: str, fields: list) -> dict:
    """ Get the field dictionary for a given field type from a list of fields.

    :param typename: The type name of the field.
    :param fields: The list of fields to search in.
    :return: The field dictionary matching the given type name, or {}.
    """
    field_dict = next((field for field in fields if
                       field.get('typeName') == typename), {})
    return field_dict


def get_fields(typename: str, fields: list) -> list:
    """ Get the field dictionary list for a given field type from a fields set.

    :param typename: The type name of the field.
    :param fields: The list of fields to search in.
    :return: The list of field dictionary matching the given type name, or {}.
    """
    matching_fields = [field for field in fields if
                       field.get('typeName') == typename]
    return matching_fields


def add_doi_to_dab_link(metadata: dict, doi: str):
    """ Adds DOI to dab link, but only if dab link is in the metadata.
    """
    dab_url = "https://dab.surf.nl/dataset?pid="
    if 'dataAccessPlace' in metadata['datasetVersion']:
        metadata['datasetVersion'][
            'dataAccessPlace'] = f"<a href=\"{dab_url}{doi}\">{dab_url}{doi}</a>"


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
        elif re.search(r'/by-nd/4\.0', license_string):
            dataset_lic = "CC BY-ND 4.0"
        elif re.search(r'zero/1\.0', license_string):
            dataset_lic = "CC0 1.0"
    elif re.search(r'10\.17026/fp39-0x58', license_string):
        dataset_lic = "DANS Licence"
    return dataset_lic


def refine_field_primitive_to_multiple(metadata, metadataBlock, field):
    metadataBlocks = metadata['datasetVersion']['metadataBlocks']
    if metadataBlock in metadataBlocks:
        fields = metadataBlocks[metadataBlock]['fields']

        field_to_refine = get_field(field, fields)
        if field_to_refine and field_to_refine['multiple'] is False:
            field_to_refine['multiple'] = True
            field_to_refine['value'] = [field_to_refine['value']]


def extract_doi_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'https' and parsed_url.netloc == 'doi.org':
        return f'doi:{parsed_url.path.lstrip("/")}'
    raise HTTPException(status_code=400,
                        detail="DOI is not structured correctly.")
