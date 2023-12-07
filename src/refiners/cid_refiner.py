from datetime import datetime
from fastapi import HTTPException
from utils import get_field


def refine_cid_metadata(metadata):
    try:
        metadataBlocks = metadata['datasetVersion']['metadataBlocks']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))

    # refinements for fields in the citation metadata block.
    if 'citation' in metadataBlocks:
        citation_fields = metadataBlocks['citation']['fields']

        # dist date looks like "2023-10-29T07:58:43.398551" and should be just "2023-10-29"
        dist_date_dict = get_field('distributionDate', citation_fields)
        if 'value' in dist_date_dict:
            dist_date_dict['value'] = refine_distribution_date(
                dist_date_dict['value'])

    return metadata


def refine_distribution_date(dist_date):
    date_obj = datetime.strptime(dist_date, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date