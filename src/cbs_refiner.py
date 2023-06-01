from fastapi import HTTPException


def refine_cbs_metadata(metadata: dict, dsc_dictionary) -> dict:
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

    try:
        alt_title_dict['value'] = dsc_dictionary[alt_title]
    except KeyError:
        alt_title_dict['value'] = remove_jjjj_vv(alt_title)
    return metadata


def remove_jjjj_vv(alternative_title: str):
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
    alternative_title = alternative_title.replace('JJJJBUS', 'BUS').replace(
        'VVBUS', 'BUS').replace('JJJJTAB', 'TAB').replace('VVTAB', 'TAB')

    alternative_title = alternative_title.rstrip('_')

    return alternative_title
