from fastapi import FastAPI

from cbs_refiner import refine_cbs_metadata
from dataverse_nl_refiner import refine_dataverse_nl_metadata
from schema.input import RefinerInput
from sicada_refiner import refine_sicada_metadata

app = FastAPI()


@app.post('/metadata-refinement/dataverse-nl')
async def dataversenl_refinement(refiner_input: RefinerInput) -> dict:
    return refine_dataverse_nl_metadata(refiner_input.metadata)



@app.post('/metadata-refinement/cbs')
async def cbs_metadata_refinement(refiner_input: RefinerInput) -> dict:
    return refine_cbs_metadata(refiner_input.metadata)


@app.post('/metadata-refinement/sicada')
async def sicada_metadata_refinement(refiner_input: RefinerInput) -> dict:
    return refine_sicada_metadata(refiner_input.metadata)