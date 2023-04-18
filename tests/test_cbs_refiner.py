from fastapi.testclient import TestClient

from cbs_refiner import remove_jjjj_vv
from main import app


client = TestClient(app)


def test_remove_jjjj_vv():
    assert remove_jjjj_vv('PS Arbodiensten') == 'PS Arbodiensten'
    assert remove_jjjj_vv('PS ArbodienstenBUS') == 'PS ArbodienstenBUS'
    assert remove_jjjj_vv('PS ArbodienstenVV') == 'PS Arbodiensten'
    assert remove_jjjj_vv('PS ArbodienstenJJJJ') == 'PS Arbodiensten'
    assert remove_jjjj_vv('PS ArbodienstenJJJJbus') == 'PS Arbodienstenbus'
    assert remove_jjjj_vv('PS ArbodienstenJJJJbusVV') == 'PS Arbodienstenbus'
    assert remove_jjjj_vv('PS ArbodienstenJJJJBUSVV') == 'PS ArbodienstenBUS'
    assert remove_jjjj_vv('PS ArbodienstenJJJJtabVV') == 'PS Arbodienstentab'
    assert remove_jjjj_vv('PS JJJJArbodienstentab') == 'PS JJJJArbodienstentab'


def test_dataverse_metadata_enhancer():
    input_data = {
        "metadata": {
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
                            "value": "PS Arbodiensten"
                        }
                    ]
                }
            }
        }
    }
    response = client.post('/metadata-refinement/cbs', json=input_data)
    assert response.status_code == 200
    assert response.json() == expected_output


def test_dataverse_metadata_enhancer_missing_key():
    input_data = {
        "metadata": {
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
    }
    response = client.post('/metadata-refinement/cbs', json=input_data)
    assert response.status_code == 422
