import os

import pytest
from fastapi import HTTPException
from cbs_refiner import remove_jjjj_vv, refine_cbs_metadata, refine_keywords
from utils import csv_to_dict


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def dsc_dict():
    return csv_to_dict(os.path.join(PROJECT_ROOT, "src/data", "DSC_table.csv"))


def test_remove_jjjj_vv():
    assert remove_jjjj_vv(
        'WoonbasePopulatieWoonruimtenJJJJVV') == 'WOONBASEPOPULATIEWOONRUIMTEN'
    assert remove_jjjj_vv('ABCJJJJVV') == 'ABC'
    assert remove_jjjj_vv('ABCVV') == 'ABC'
    assert remove_jjjj_vv('ABCJJJJTAB') == 'ABCTAB'
    assert remove_jjjj_vv('ABCVVTAB') == 'ABCTAB'
    assert remove_jjjj_vv('ABC') == 'ABC'
    assert remove_jjjj_vv('PWETSRGPERSOONJJJJBUSVV') == 'PWETSRGPERSOONBUS'
    assert remove_jjjj_vv('JJJJBUS') == 'BUS'
    assert remove_jjjj_vv('VVBUS') == 'BUS'
    assert remove_jjjj_vv('JJJJTABVVTAB') == 'TABTAB'
    assert remove_jjjj_vv('CWIJJJJMMDDTABVV') == 'CWITAB'
    assert remove_jjjj_vv('GEMSTPLAATSJJJJMMBUSVV') == 'GEMSTPLAATSBUS'
    assert remove_jjjj_vv('b_handel_JJJJMM') == "B_HANDEL"


def test_cbs_metadata_refiner_dsc_dictionary(dsc_dict):

    input_data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "alternativeTitle",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": "PS ArbodienstenVV"
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
                            "typeName": "alternativeTitle",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": "PS ARBODIENSTEN"
                        }
                    ]
                }
            }
        }
    }

    test_output = refine_cbs_metadata(input_data, dsc_dict)

    assert test_output == expected_output


def test_cbs_metadata_refiner_clean_alternative_title(dsc_dict):
    input_data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "alternativeTitle",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": "PS Speur- en ontwikkelingswerk"
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
                            "typeName": "alternativeTitle",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": "PS_SPEURONTWIKKELING"
                        }
                    ]
                }
            }
        }
    }

    test_output = refine_cbs_metadata(input_data, dsc_dict)

    assert test_output == expected_output


def test_cbs_metadata_refiner_missing_key(dsc_dict):
    input_data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "foo",
                            "value": "bar"
                        }
                    ]
                }
            }
        }
    }

    with pytest.raises(HTTPException) as exc_info:
        refine_cbs_metadata(input_data, dsc_dict)
    assert exc_info.value.status_code == 422


def test_cbs_metadata_refiner_refine_keywords(dsc_dict):
    input_data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "keyword",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": ["keyword1/keyword2", "keyword3"]
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
                            "typeName": "keyword",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": ["keyword1", "keyword2", "keyword3"]
                        }
                    ]
                }
            }
        }
    }

    test_output = refine_cbs_metadata(input_data, dsc_dict)

    assert test_output == expected_output


# Run the test case
test_cbs_metadata_refiner_refine_keywords(dsc_dict)


def test_refine_keywords():
    fields = [
        {'typeName': 'keyword', 'value': ['keyword1/keyword2', 'keyword3']},
        {'typeName': 'other', 'value': 'some value'}
    ]

    # Test case 1: Keywords with slashes
    expected_output = ['keyword1', 'keyword2', 'keyword3']
    output = refine_keywords(fields)
    assert output == expected_output

    # Test case 2: No keyword field
    fields_no_keywords = [
        {'typeName': 'other', 'value': 'some value'}
    ]
    expected_output_no_keywords = []
    output_no_keywords = refine_keywords(fields_no_keywords)
    assert output_no_keywords == expected_output_no_keywords

    # Test case 3: Empty keyword value
    fields_empty_keywords = [
        {'typeName': 'keyword', 'value': []},
        {'typeName': 'other', 'value': 'some value'}
    ]
    expected_output_empty_keywords = []
    output_empty_keywords = refine_keywords(fields_empty_keywords)
    assert output_empty_keywords == expected_output_empty_keywords
