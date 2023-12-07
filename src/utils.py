import csv


def add_contact_email(metadata, contact_email):
    """ Adds a contact email to dataverse JSON.

    If metadata exported from a Dataverse is missing the contact email,
    add_contact_email can be used to add a contact email.

    :param contact_email: Standard contact email to use.
    :param metadata: Dataverse JSON that is missing the contact email.
    :return: dataverse JSON with the contact email added.
    """
    fields = metadata['datasetVersion']['metadataBlocks']['citation'][
        'fields']
    dataset_contact = next((field for field in fields if
                            field.get('typeName') == 'datasetContact'), None)
    if dataset_contact:
        for dataset_contact in dataset_contact["value"]:
            dataset_contact["datasetContactEmail"] = {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": contact_email
            }
    else:
        fields.append({
            "typeName": "datasetContact",
            "multiple": True,
            "typeClass": "compound",
            "value": [
                {
                    "datasetContactEmail": {
                        "typeName": "datasetContactEmail",
                        "multiple": False,
                        "typeClass": "primitive",
                        "value": contact_email
                    }
                }
            ]
        })
    return metadata


def csv_to_dict(filename: str) -> dict[str, str]:
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # skip header row if present
        return {row[1]: row[0] for row in reader if len(row) >= 2}


def get_field(typename, fields):
    """ Get the field dictionary for a given field type from a list of fields.

    :param typename: The type name of the field.
    :param fields: The list of fields to search in.
    :return: The field dictionary matching the given type name, or {}.
    """
    field_dict = next((field for field in fields if
                       field.get('typeName') == typename), {})
    return field_dict