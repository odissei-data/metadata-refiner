from utils import add_contact_email


def refine_sicada_metadata(metadata: dict) -> dict:
    metadata = add_contact_email(metadata, "info@sicada.nl")

    metadata_blocks = metadata["datasetVersion"]['metadataBlocks']
    dataset_version = {'metadataBlocks': metadata_blocks}
    metadata['datasetVersion'] = dataset_version

    return metadata
