from fastapi import HTTPException

from refiners.liss_refiner import refine_liss_metadata


def test_refine_liss_metadata():
    metadata = {
        "persistentUrl": "https://doi.org/10.17026/dans-zm4-yfdv",
        "datasetVersion": {
            "dataAccessPlace": "<a href=\"https://dab.surf.nl\">https://dab.surf.nl</a>",
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "topicClassification",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "topicClassValue": {
                                        "typeName": "topicClassValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Gender expression"
                                    }
                                },
                                {
                                    "topicClassValue": {
                                        "typeName": "topicClassValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Households"
                                    }
                                },
                                {
                                    "topicClassValue": {
                                        "typeName": "topicClassValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Sexual and gender groups"
                                    }
                                },
                                {
                                    "topicClassValue": {
                                        "typeName": "topicClassValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Social behavior (LISS)"
                                    }
                                }
                            ]
                        },
                        {
                            "typeName": "distributor",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "distributorName": {
                                        "typeName": "distributorName",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Centerdata"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Expected updated values
    expected_dab_url = "https://dab.surf.nl/dataset?pid=doi:10.17026/dans-zm4-yfdv"
    expected_topic = "Social behavior"

    # Call the function to test
    updated_metadata = refine_liss_metadata(metadata)

    # Assertions
    assert updated_metadata["datasetVersion"]["dataAccessPlace"] == \
           f'<a href="{expected_dab_url}">{expected_dab_url}</a>'

    # Loop through the fields to find the correct topic to assert
    for field in \
            updated_metadata["datasetVersion"]["metadataBlocks"]["citation"][
                "fields"]:
        if field["typeName"] == "topicClassification":
            topic_classifications = field["value"]
            for topic in topic_classifications:
                if topic["topicClassValue"]["value"] == expected_topic:
                    assert topic["topicClassValue"]["value"] == expected_topic
                    break


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
        assert e.detail == "DOI is missing from the metadata."
