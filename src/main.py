import re

from fastapi import FastAPI, HTTPException

from schema.input import RefinerInput

app = FastAPI()


@app.post('/dataverse-nl-metadata-refinement')
async def dataversenl_refinement(refiner_input: RefinerInput) -> dict:
    metadata = add_contact_email(refiner_input.metadata)
    metadata_blocks = metadata["datasetVersion"]['metadataBlocks']
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


@app.post('/cbs-metadata-refinement')
async def cbs_metadata_refinement(refiner_input: RefinerInput) -> dict:
    metadata = refiner_input.metadata
    try:
        fields = metadata['datasetVersion']['metadataBlocks']['citation'][
            'fields']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))
    alt_title_dict = next((field for field in fields if
                           field.get('typeName') == 'alternativeTitle'), {})

    try:
        alt_title = alt_title_dict['value']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))

    alt_title_dict['value'] = remove_jjjj_vv(alt_title)
    return metadata


def remove_jjjj_vv(alternative_title: str):
    # remove JJJJ and VV suffixes from end of string if they match the pattern
    if alternative_title.endswith('JJJJ'):
        if all(c.isupper() for c in alternative_title[-4:]):
            alternative_title = alternative_title[:-4]
    if alternative_title.endswith('VV'):
        if all(c.isupper() for c in alternative_title[-2:]):
            alternative_title = alternative_title[:-2]

    # remove JJJJ and VV suffixes surrounding "bus/BUS" or "tab/TAB"
    alternative_title = alternative_title.replace('JJJJbus', 'bus').replace(
        'VVbus', 'bus').replace('JJJJBUS', 'BUS').replace('VVBUS', 'BUS')
    alternative_title = alternative_title.replace('JJJJtab', 'tab').replace(
        'VVtab', 'tab').replace('JJJJTAB', 'TAB').replace('VVTAB', 'TAB')
    return alternative_title


def add_contact_email(metadata):
    """ Adds a contact email to dataverse JSON.

    If metadata exported from a Dataverse is missing the contact email,
    add_contact_email can be used to add a contact email.
    TODO: make the email value an env variable.

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
                "value": "portal@odissei.nl"
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
                        "value": "portal@odissei.nl"
                    }
                }
            ]
        })
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
        elif re.search(r'zero/1\.0', license_string):
            dataset_lic = "CC0 1.0"
    elif re.search(r'DANSLicence', license_string):
        dataset_lic = "DANS Licence"
    return dataset_lic
