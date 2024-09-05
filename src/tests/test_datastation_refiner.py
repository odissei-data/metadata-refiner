from refiners.datastation_refiner import add_doi_to_dab_link
from utils import format_license, retrieve_license_name, \
    refine_field_primitive_to_multiple


def test_add_doi_to_dab_link():
    metadata = {
        "datasetVersion": {
            "dataAccessPlace": "<a href=\"https://dab.surf.nl\">https://dab.surf.nl</a>",
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "author",
                            "value": "Doe, John"
                        },
                        {
                            "typeName": "title",
                            "value": "Example Dataset"
                        }
                    ]
                },
            },
            "termsOfUse": "terms_of_use",
            "termsOfAccess": "terms_of_access",
            "license": "CC0",
            "datasetPersistentId": "10.1234/example-doi"
        }
    }

    # Expected URL
    expected_dab_url = "https://dab.surf.nl/dataset?pid=10.1234/example-doi"

    # Call the function to test
    add_doi_to_dab_link(metadata,
                        metadata["datasetVersion"]["datasetPersistentId"])
    # Assertions
    assert metadata["datasetVersion"]["dataAccessPlace"] == \
           f'<a href="{expected_dab_url}">{expected_dab_url}</a>'

def test_format_license():
    assert format_license('CC0') == 'CC0 1.0'
    assert format_license({
        'uri': 'https://creativecommons.org/licenses/by/4.0/'
    }) == 'CC BY 4.0'
    assert format_license({
        'uri': 'https://creativecommons.org/licenses/by-nc/4.0/'
    }) == 'CC BY-NC 4.0'
    assert format_license({
        'uri': 'https://creativecommons.org/licenses/by-sa/4.0/'
    }) == 'CC BY-SA 4.0'
    assert format_license({
        'uri': 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
    }) == 'CC BY-NC-SA 4.0'
    assert format_license({
        'uri': 'https://creativecommons.org/publicdomain/zero/1.0/'
    }) == 'CC0 1.0'
    assert format_license({
        'uri': 'https://doi.org/10.17026/fp39-0x58'
    }) == 'DANS Licence'
    assert format_license({
        'uri': 'http://creativecommons.org/licenses/by-nc-nd/4.0'
    }) == 'CC BY-NC-ND 4.0'


def test_retrieve_license_name():
    assert retrieve_license_name(
        'https://creativecommons.org/licenses/by/4.0/') == 'CC BY 4.0'
    assert retrieve_license_name(
        'https://creativecommons.org/licenses/by-nc/4.0/') == 'CC BY-NC 4.0'
    assert retrieve_license_name(
        'https://creativecommons.org/licenses/by-sa/4.0/') == 'CC BY-SA 4.0'
    assert retrieve_license_name(
        'https://creativecommons.org/licenses/by-nc-sa/4.0/'
    ) == 'CC BY-NC-SA 4.0'
    assert retrieve_license_name(
        'https://creativecommons.org/publicdomain/zero/1.0/') == 'CC0 1.0'
    assert retrieve_license_name(
        'https://creativecommons.org/licenses/nonexistent/1.0/') == ''
    assert retrieve_license_name('') == ''


def test_refine_production_place_field():
    # Create a sample metadata dictionary with 'productionPlace' field.
    metadata = {
        'datasetVersion': {
            'metadataBlocks': {
                'citation': {
                    'fields': [
                        {
                            'typeName': 'productionPlace',
                            'multiple': False,
                            'typeClass': 'primitive',
                            'value': 'Netherlands'
                        }
                    ]
                }
            }
        }
    }

    # Call the function to refine the 'productionPlace' field.
    refine_field_primitive_to_multiple(metadata, 'citation', 'productionPlace')

    # Check if the field has been updated as expected.
    assert metadata['datasetVersion']['metadataBlocks']['citation']['fields'][0]['multiple'], True
    assert metadata['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value'], ['Netherlands']
