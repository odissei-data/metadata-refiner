import os

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from cbs_refiner import remove_jjjj_vv, refine_cbs_metadata
from main import app
from utils import csv_to_dict

client = TestClient(app)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def dsc_dict():
    return csv_to_dict(os.path.join(PROJECT_ROOT, "data", "DSC_table.csv"))


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


def test_cbs_metadata_refiner_remove_jjj_vv(dsc_dict):
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

