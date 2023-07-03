import os

import pytest
from refiners.cbs_refiner import clean_alternative_title, refine_cbs_metadata, \
    refine_keywords
from utils import csv_to_dict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "../.."))


@pytest.fixture
def dsc_dict():
    return csv_to_dict(os.path.join(PROJECT_ROOT, "src/data", "DSC_table.csv"))


def test_remove_jjjj_vv():
    assert clean_alternative_title(
        'WoonbasePopulatieWoonruimtenJJJJVV') == 'WOONBASEPOPULATIEWOONRUIMTEN'
    assert clean_alternative_title('ABCJJJJVV') == 'ABC'
    assert clean_alternative_title('ABCVV') == 'ABC'
    assert clean_alternative_title('ABCJJJJTAB') == 'ABCTAB'
    assert clean_alternative_title('ABCVVTAB') == 'ABCTAB'
    assert clean_alternative_title('ABC') == 'ABC'
    assert clean_alternative_title(
        'PWETSRGPERSOONJJJJBUSVV') == 'PWETSRGPERSOONBUS'
    assert clean_alternative_title('JJJJBUS') == 'BUS'
    assert clean_alternative_title('VVBUS') == 'BUS'
    assert clean_alternative_title('JJJJTABVVTAB') == 'TABTAB'
    assert clean_alternative_title('CWIJJJJMMDDTABVV') == 'CWITAB'
    assert clean_alternative_title(
        'GEMSTPLAATSJJJJMMBUSVV') == 'GEMSTPLAATSBUS'
    assert clean_alternative_title('b_handel_JJJJMM') == "B_HANDEL"


def test_cbs_metadata_refiner_dsc_dictionary(dsc_dict):
    print(dsc_dict)
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
                            "value": [
                                {
                                    "keywordValue": {
                                        "typeName": "keywordValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "keyword1"
                                    }
                                },
                                {
                                    "keywordValue": {
                                        "typeName": "keywordValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "keyword2/keyword3"
                                    }
                                }
                            ]
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
                            "value": [
                                {
                                    "keywordValue": {
                                        "typeName": "keywordValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "keyword1"
                                    }
                                },
                                {
                                    "keywordValue": {
                                        "typeName": "keywordValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "keyword2"
                                    }
                                },
                                {
                                    "keywordValue": {
                                        "typeName": "keywordValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "keyword3"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    test_output = refine_cbs_metadata(input_data, dsc_dict)

    assert test_output == expected_output


    assert test_output == expected_output


def test_refine_keywords():
    fields = [
        {'typeName': 'keyword', 'value': [
            {'keywordValue': {'value': 'keyword1/keyword2'}},
            {'someOtherKey': {'value': 'keyword3'}}
        ]},
        {'typeName': 'other', 'value': 'some value'}
    ]

    # Test case 1: Keywords with slashes
    expected_output = [
        {'keywordValue': {'typeName': 'keywordValue', 'multiple': False, 'typeClass': 'primitive', 'value': 'keyword1'}},
        {'keywordValue': {'typeName': 'keywordValue', 'multiple': False, 'typeClass': 'primitive', 'value': 'keyword2'}}
    ]
    output = refine_keywords(fields[0]['value'])
    assert output == expected_output

    # Test case 2: No keywordValue key
    fields_no_keyword_value = [
        {'typeName': 'keyword', 'value': [
            {'someOtherKey': {'value': 'keyword1/keyword2'}},
            {'anotherKey': {'value': 'keyword3'}}
        ]},
        {'typeName': 'other', 'value': 'some value'}
    ]
    expected_output_no_keyword_value = []
    output_no_keyword_value = refine_keywords(fields_no_keyword_value[0]['value'])
    assert output_no_keyword_value == expected_output_no_keyword_value

    # Test case 3: Empty keyword value
    fields_empty_keywords = [
        {'typeName': 'keyword', 'value': []},
        {'typeName': 'other', 'value': 'some value'}
    ]
    expected_output_empty_keywords = []
    output_empty_keywords = refine_keywords(fields_empty_keywords[0]['value'])
    assert output_empty_keywords == expected_output_empty_keywords


