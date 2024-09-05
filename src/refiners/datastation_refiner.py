from fastapi import HTTPException

from utils import add_doi_to_dab_link, format_license


def refine_datastation_metadata(metadata: dict) -> dict:
    if 'license' in metadata['datasetVersion'] and metadata['datasetVersion'][
         'license'] != 'NONE' and metadata['datasetVersion']['license']:
        metadata['datasetVersion']['license'] = format_license(
            metadata['datasetVersion']['license']
        )
    elif 'license' in metadata['datasetVersion']:
        del metadata['datasetVersion']['license']

    try:
        doi = metadata["datasetVersion"]["datasetPersistentId"]
        add_doi_to_dab_link(metadata, doi)
    except KeyError:
        raise HTTPException(status_code=400,
                            detail="DOI is missing from the metadata")

    return metadata



