from fastapi import FastAPI, HTTPException

from schema.input import RefinerInput

app = FastAPI()


@app.post('/cbs-metadata-refinement')
async def dataverse_metadata_enhancer(refiner_input: RefinerInput) -> dict:
    metadata = refiner_input.metadata
    try:
        fields = metadata['datasetVersion']['metadataBlocks']['citation'][
            'fields']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))
    alt_title_dict = next((field for field in fields if
                           field.get('typeName') == 'alternativeTitle'), {})

    try:
        alt_title = alt_title_dict['value']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))

    alt_title_dict['value'] = remove_jjjj_vv(alt_title)
    return metadata


def remove_jjjj_vv(alternative_title: str):
    # remove JJJJ and VV suffixes from end of string if they match the pattern
    if alternative_title.endswith('JJJJ'):
        if all(c.isupper() for c in alternative_title[-4:]):
            alternative_title = alternative_title[:-4]
    if alternative_title.endswith('VV'):
        if all(c.isupper() for c in alternative_title[-2:]):
            alternative_title = alternative_title[:-2]

    # remove JJJJ and VV suffixes surrounding "bus/BUS" or "tab/TAB"
    alternative_title = alternative_title.replace('JJJJbus', 'bus').replace(
        'VVbus', 'bus').replace('JJJJBUS', 'BUS').replace('VVBUS', 'BUS')
    alternative_title = alternative_title.replace('JJJJtab', 'tab').replace(
        'VVtab', 'tab').replace('JJJJTAB', 'TAB').replace('VVTAB', 'TAB')
    return alternative_title
