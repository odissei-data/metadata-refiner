from fastapi import HTTPException


def refine_cbs_metadata(metadata: dict, dsc_dictionary) -> dict:
    """ Refines CBS metadata by refining the alt title and keyword field.

    The alternative title is either matched on a table or cleaned up.
    The keyword is split on "/" character and added as separate keywords.

    :param metadata: CBS metadata to be refined.
    :param dsc_dictionary: DSC dictionary containing refined alt titles.
    :return: Refined metadata.
    :raises HTTPException: Raises if required keys are missing from metadata.
    """
    try:
        fields = metadata['datasetVersion']['metadataBlocks']['citation'][
            'fields']
    except KeyError as error:
        raise HTTPException(status_code=422, detail=str(error))

    alt_title_dict = get_field('alternativeTitle', fields)
    if 'value' in alt_title_dict:
        alt_title_dict['value'] = refine_alternative_title(
            alt_title_dict['value'], dsc_dictionary)

    keyword_dict = get_field('keyword', fields)
    if 'value' in keyword_dict:
        keyword_dict['value'] = refine_keywords(
            keyword_dict['value'])

    return metadata


def get_field(typename, fields):
    """ Get the field dictionary for a given field type from a list of fields.

    :param typename: The type name of the field.
    :param fields: The list of fields to search in.
    :return: The field dictionary matching the given type name, or {}.
    """
    field_dict = next((field for field in fields if
                       field.get('typeName') == typename), {})
    return field_dict


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
    Refine an alternative title by looking it up in a dictionary or cleaning it if not found.

    :param alt_title: The alternative title to refine.
    :param dsc_dictionary: The dictionary containing refined alternative titles.
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
