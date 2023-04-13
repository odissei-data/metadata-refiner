# metadata-refiner
## Description
This service refines metadata by cleaning up unwanted fields, altering wrongly formatted fields and adding the correct license.
## Frameworks
This project uses:
- Python 3.10
- FastAPI
- Poetry

## Setup
The default port in the example .env is 7878, change it to fit your needs.
1. `cp dot_env_example .env`
2. `make build`


## End-points
### Version
Returns the current version of the API

### Refiner
Refines metadata for different data providers.
#### Parameters
- metadata - [JSON metadata for Dataverse](https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json) - The input metadata describing a dataset in JSON meant for Dataverse.

#### Return value
When successful, the API call will return the metadata with the necessary refinements.
The call will return an exception on a failed attempt further elaborating what went wrong.
