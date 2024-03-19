from refiners.dataverse_nl_refiner import format_license


def refine_datastation_metadata(metadata: dict) -> dict:

    if 'license' in metadata['datasetVersion'] and metadata['datasetVersion'][
        'license'] != 'NONE' and metadata['datasetVersion']['license']:
        metadata['datasetVersion']['license'] = format_license(
            metadata['datasetVersion']['license']
        )
    elif 'license' in metadata['datasetVersion']:
        del metadata['datasetVersion']['license']

    return metadata
