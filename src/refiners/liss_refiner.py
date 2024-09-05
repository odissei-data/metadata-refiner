import re

from fastapi import HTTPException

from utils import add_doi_to_dab_link, update_field


def refine_liss_metadata(metadata: dict) -> dict:
    try:
        doi = metadata["persistentUrl"]
        add_doi_to_dab_link(metadata, doi)
    except KeyError:
        raise HTTPException(status_code=400,
                            detail="DOI is missing from the metadata")

    update_field(metadata, "citation", "topicClassValue", update_topic)

    update_field(metadata, "citation", "distributorName",
                 update_distributor_name)

    return metadata


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
