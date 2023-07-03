import os

from fastapi import FastAPI

from refiners.cbs_refiner import refine_cbs_metadata
from refiners.datastation_refiner import refine_datastation_metadata
from refiners.dataverse_nl_refiner import refine_dataverse_nl_metadata
from schema.input import RefinerInput
from sicada_refiner import refine_sicada_metadata
from utils import csv_to_dict
from version import get_version

app = FastAPI()

DSC_TABLE_CSV = os.environ.get('DSC_TABLE_CSV', 'data/DSC_table.csv')


def load_data():
    filename = os.path.join(os.getcwd(), DSC_TABLE_CSV)
    dsc_dictionary = csv_to_dict(filename)
    return dsc_dictionary


@app.get("/version")
async def info():
    result = get_version()
    return {"version": result}


@app.post('/metadata-refinement/dataverse-nl')
async def dataversenl_refinement(refiner_input: RefinerInput) -> dict:
    return refine_dataverse_nl_metadata(refiner_input.metadata)


@app.post('/metadata-refinement/cbs')
async def cbs_metadata_refinement(refiner_input: RefinerInput) -> dict:
    dsc_dictionary = load_data()
    return refine_cbs_metadata(refiner_input.metadata,
                               dsc_dictionary)


@app.post('/metadata-refinement/sicada')
async def sicada_metadata_refinement(refiner_input: RefinerInput) -> dict:
    return refine_sicada_metadata(refiner_input.metadata)


@app.post('/metadata-refinement/datastation')
async def datastation_metadata_refinement(refiner_input: RefinerInput) -> dict:
    return refine_datastation_metadata(refiner_input.metadata)
