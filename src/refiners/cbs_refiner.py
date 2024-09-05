import re
import jmespath

from fastapi import HTTPException

from queries import CBS_ID_QUERY
from utils import get_field, add_doi_to_dab_link


def refine_cbs_metadata(metadata: dict, dsc_dictionary) -> dict:
    """ Refines CBS metadata, specificly alt title, keyword and statline field.

    The alternative title is either matched on a table or cleaned up.
    The keyword is split on "/" character and added as separate keywords.
    The statline field formats all statline links to be clickable URLs.

    :param metadata: CBS metadata to be refined.
    :param dsc_dictionary: DSC dictionary containing refined alt titles.
    :return: Refined metadata.
    :raises HTTPException: Raises if required keys are missing from metadata.
    """
    try:
        metadataBlocks = metadata['datasetVersion']['metadataBlocks']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))

    # refinements for fields in the citation metadata block.
    if 'citation' in metadataBlocks:
        citation_fields = metadataBlocks['citation']['fields']

        alt_title_dict = get_field('alternativeTitle', citation_fields)
        if 'value' in alt_title_dict:
            alt_titles = []
            for alternative_title in alt_title_dict['value']:
                alt_titles.append(refine_alternative_title(
                    alternative_title, dsc_dictionary))
            alt_title_dict['value'] = alt_titles
        keyword_dict = get_field('keyword', citation_fields)
        if 'value' in keyword_dict:
            keyword_dict['value'] = refine_keywords(
                keyword_dict['value'])

    # refinements for fields in the CBSMetadata block.
    if 'CBSMetadata' in metadataBlocks:
        CBS_fields = metadataBlocks['CBSMetadata']['fields']

        statline_dict = get_field('statlineTabel', CBS_fields)
        if 'value' in statline_dict:
            statline_dict['value'] = refine_statline_table(
                statline_dict['value'])

    cbs_id = jmespath.search(CBS_ID_QUERY, metadata)
    if cbs_id:
        doi = "doi:10.57934/" + cbs_id
        add_doi_to_dab_link(metadata, doi)

    return metadata


def refine_keywords(keyword_values):
    """ Refine a list of keyword values by splitting specific keywords.

    :param keyword_values: The list of keyword values to refine.
    :return: A list of refined keywords.
    """

    refined_keywords = []
    for keyword_value in keyword_values:
        if 'keywordValue' in keyword_value:
            refined_keywords.extend(
                Add_split_keywords(keyword_value['keywordValue']['value'])
            )
    return refined_keywords


def Add_split_keywords(keyword):
    """
    Split a keyword value by '/' and format it into a dictionary.

    :param keyword: The keyword value to split.
    :return: A list of formatted keywords as dictionaries.
    """
    refined_keywords = []
    split_keywords = keyword.split('/')
    for split_keyword in split_keywords:
        refined_keywords.append({
            'keywordValue': {
                'typeName': 'keywordValue',
                'multiple': False,
                'typeClass': 'primitive',
                'value': split_keyword
            }
        })
    return refined_keywords


def refine_alternative_title(alt_title, dsc_dictionary):
    """
    Refine an alternative title by looking it up in a dictionary or
    cleaning it if not found.

    :param alt_title: The alternative title to refine.
    :param dsc_dictionary: Dictionary containing refined alternative titles.
    :return: The refined alternative title.
    """
    try:
        return dsc_dictionary[alt_title]
    except KeyError:
        return clean_alternative_title(alt_title)


def clean_alternative_title(alternative_title: str):
    """ Clean the alternative title by performing various transformations.

    This function takes an alternative title as input and performs
    several cleaning operations to transform it into a standardized format.
    The alternative title is expected to be a string.

    The cleaning operations performed by this function include these steps:

    1. Convert the alternative title to uppercase.
    2. Remove 'VV' suffix from the end of the string if matches the pattern.
    3. Remove 'JJJJ' suffix from the end of the string if matches the pattern.
    4. Remove 'JJJJMMDD' or 'JJJJMM' from the title if present.
    5. Remove 'JJJJ' and 'VV' suffixes surrounding "bus/BUS" or "tab/TAB".
    6. Remove trailing underscores from the alternative title.

    After, the function returns the cleaned alternative title as a string.

    :param alternative_title: The alternative title to be cleaned.
    :return: The cleaned alternative title.
    """
    alternative_title = alternative_title.upper()

    # remove JJJJ and VV suffixes from end of string if they match the pattern.
    if alternative_title.endswith('VV'):
        alternative_title = alternative_title[:-2]
    if alternative_title.endswith('JJJJ'):
        alternative_title = alternative_title[:-4]

    # Remove JJJJMMDD or JJMM from the title.
    if "JJJJMMDD" in alternative_title:
        dd_index = alternative_title.find("JJJJMMDD")
        alternative_title = alternative_title[:dd_index] + alternative_title[
                                                           dd_index + 8:]
    if "JJJJMM" in alternative_title:
        mm_index = alternative_title.find("JJJJMM")
        alternative_title = alternative_title[:mm_index] + alternative_title[
                                                           mm_index + 6:]

    # remove JJJJ and VV suffixes surrounding "bus/BUS" or "tab/TAB".
    alternative_title = alternative_title.replace('JJJJBUS', 'BUS').replace(
        'VVBUS', 'BUS').replace('JJJJTAB', 'TAB').replace('VVTAB', 'TAB')

    alternative_title = alternative_title.rstrip('_')

    return alternative_title


def refine_statline_table(statlineLinks: list) -> list:
    """ Reformats statline links to a clickable URL if they contain a code.

    Some links to the statline tables only include the id of the table.
    This function splits the links not yet in URL format from the correctly
    formatted links. It then formats them to also be clickable URLs.

    :param statlineLinks: A list of URLs and table id's. (Linking to statline).
    :return: List with URLs linking to statline tables.
    """
    valid_urls = [url for url in statlineLinks if is_url(url)]
    statline_codes = [url for url in statlineLinks if not is_url(url)]
    formatted_statline_urls = [format_statline_url(code) for code in
                               statline_codes]

    return valid_urls + formatted_statline_urls


def format_statline_url(statline_code):
    """ Alters a statline code that identifies a table to be a clickable url.

    :param statline_code: The code linking to the a table.
    :return: The URL that links to a statline table.
    """
    return f'https://opendata.cbs.nl/#/CBS/nl/dataset/{statline_code}'


def is_url(s):
    """ Checks if a string is a URL """
    url_pattern = r'^https?://\S+$'
    return bool(re.match(url_pattern, s))
