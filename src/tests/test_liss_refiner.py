from fastapi import HTTPException

from refiners.liss_refiner import refine_liss_metadata


def test_refine_liss_metadata():
    metadata = {
        "persistentUrl": "10.1234/example-doi",
        "datasetVersion": {
            "dataAccessPlace": "<a href=\"https://dab.surf.nl\">https://dab.surf.nl</a>",
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "topicClassValue",
                            "value": "Social Sciences (LISS)"
                        },
                        {
                            "typeName": "distributorName",
                            "value": "CentERdata"
                        }
                    ]
                }
            }
        }
    }

    # Expected updated values
    expected_dab_url = "https://dab.surf.nl/dataset?pid=10.1234/example-doi"
    expected_topic = "Social Sciences"
    expected_distributor_name = "Centerdata"

    # Call the function to test
    updated_metadata = refine_liss_metadata(metadata)

    # Assertions
    assert updated_metadata["datasetVersion"]["dataAccessPlace"] == \
           f'<a href="{expected_dab_url}">{expected_dab_url}</a>'
    assert \
        updated_metadata["datasetVersion"]["metadataBlocks"]["citation"][
            "fields"][
            0]["value"] == expected_topic
    assert \
        updated_metadata["datasetVersion"]["metadataBlocks"]["citation"][
            "fields"][
            1]["value"] == expected_distributor_name


def test_refine_liss_metadata_doi_missing():
    # Test case where DOI is missing
    metadata = {
        "datasetVersion": {
            "dataAccessPlace": "<a href=\"https://dab.surf.nl\">https://dab.surf.nl</a>",
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "topicClassValue",
                            "value": "Social Sciences (LISS)"
                        },
                        {
                            "typeName": "distributorName",
                            "value": "CentERdata"
                        }
                    ]
                }
            }
        }
    }

    # Expect an HTTPException with status 400
    try:
        refine_liss_metadata(metadata)
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "DOI is missing from the metadata"
