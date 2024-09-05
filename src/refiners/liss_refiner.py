import re

from fastapi import HTTPException
from utils import add_doi_to_dab_link, extract_doi_from_url


def refine_liss_metadata(metadata: dict) -> dict:
    try:
        doi = extract_doi_from_url(metadata["persistentUrl"])
        add_doi_to_dab_link(metadata, doi)
    except KeyError:
        raise HTTPException(status_code=400,
                            detail="DOI is missing from the metadata.")

    update_topic_classification(metadata)

    return metadata


def update_topic_classification(metadata: dict) -> None:
    """ Navigate to the path where the topicClassValue fields are located and
     replaces them.

    :param metadata:
    """

    try:
        citation_fields = metadata["datasetVersion"]["metadataBlocks"][
            "citation"]["fields"]
    except KeyError:
        raise HTTPException(status_code=400,
                            detail="Metadata should be dataverse JSON.")

    for field in citation_fields:
        if field.get('typeName') == 'topicClassification':
            topic_classifications = field['value']
            for topic in topic_classifications:
                topic['topicClassValue']['value'] = update_topic(
                    topic['topicClassValue']['value'])


def update_topic(topic: str) -> str:
    """ Cleans topics by removing (LISS) or (LISS/ELSST) from the string.

    :param topic: String representing a topic. Ends in (LISS) or (LISS/ELLST).
    :return: Cleaned topic.
    """
    return re.sub(r'\s*\(.*?\)', '', topic)


def update_distributor_name(distributor_name: str) -> str:
    """ Changes CentERdata to Centerdata for the dist name.

    :param distributor_name: Either Centerdata or CentERdata.
    :return: Fixed distributor name.
    """
    if distributor_name == 'CentERdata':
        return "Centerdata"
    return distributor_name
