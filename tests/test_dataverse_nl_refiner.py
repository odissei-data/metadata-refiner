from dataverse_nl_refiner import refine_dataverse_nl_metadata, \
    retrieve_license_name, format_license
from utils import add_contact_email


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


def test_refine_dataverse_nl_metadata():
    metadata = {
        "datasetVersion": {
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
            "license": "CC0"
        }
    }
    refined_metadata = refine_dataverse_nl_metadata(metadata)
    assert refined_metadata["datasetVersion"]["metadataBlocks"] == \
           metadata["datasetVersion"]["metadataBlocks"]
    assert refined_metadata["datasetVersion"]["termsOfUse"] == \
           metadata["datasetVersion"]["termsOfUse"]
    assert refined_metadata["datasetVersion"]["termsOfAccess"] == \
           metadata["datasetVersion"]["termsOfAccess"]
    assert refined_metadata["datasetVersion"]["license"] == "CC0 1.0"

    metadata = {
        "datasetVersion": {
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
        }
    }

    refined_metadata = refine_dataverse_nl_metadata(metadata)
    assert refined_metadata["datasetVersion"]["metadataBlocks"] == \
           metadata["datasetVersion"]["metadataBlocks"]
    assert "termsOfUse" not in refined_metadata["datasetVersion"]
    assert "termsOfAccess" not in refined_metadata["datasetVersion"]
    assert "license" not in refined_metadata["datasetVersion"]


def test_add_contact_email():
    # Test adding contact email to existing metadata
    metadata = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "datasetContactName": {
                                        "typeName": "datasetContactName",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "John Doe"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    contact_email = "test@example.com"
    updated_metadata = add_contact_email(metadata, contact_email)
    assert updated_metadata["datasetVersion"]["metadataBlocks"][
               "citation"]["fields"][0]["value"][0]["datasetContactEmail"][
               "value"] == contact_email

    # Test adding contact email to missing metadata
    metadata = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [

                    ]
                }
            }
        }
    }
    updated_metadata = add_contact_email(metadata, contact_email)
    assert updated_metadata["datasetVersion"]["metadataBlocks"][
               "citation"]["fields"][0]["value"][0]["datasetContactEmail"][
               "value"] == contact_email
