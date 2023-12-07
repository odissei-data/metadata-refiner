from refiners.cid_refiner import refine_cid_metadata


def test_refine_cid_metadata():
    input_data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "distributionDate",
                            "typeClass": "primitive",
                            "multiple": True,
                            "value": "2023-10-29T07:58:43.398551"
                        }
                    ]
                }
            }
        }
    }

    expected_output = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "distributionDate",
                            "typeClass": "primitive",
                            "multiple": True,
                            "value": "2023-10-29"
                        }
                    ]
                }
            }
        }
    }

    refined_metadata = refine_cid_metadata(input_data)

    assert refined_metadata == expected_output
