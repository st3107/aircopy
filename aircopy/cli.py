"""The cli interface."""
import os
from typing import Union, List

import fire

import aircopy.io as io
from aircopy.database import DataBase


def aircopy(add_info: dict = None, max_records: int = None, view: int = None, page_size: int = None,
            fields: Union[str, List[str]] = None, sort: List[str] = None, formula: str = None):
    """Transfer the data from Airtbale to Billinge group projecta database.

    It will read the variables 'AIRTABLE_BASE_ID' and 'AIRTABLE_API_TOKEN' inside your environment and connect to your
    airtable database, download the content and parse it into Billinge group database documents and write it out to
    yaml files.

    To use the it, you need to find the base id of your Airtable by visiting the airtable api website
    (https://airtable.com/api) and generate the api token following the instructions on the website
    (https://support.airtable.com/hc/en-us/articles/219046777-How-do-I-get-my-API-key-).
    Then, export the base id and api token to the environment variables.

    `export AIRTABLE_BASE_ID=***`

    `export AIRTABLE_API_TOKEN=***`

    Then run the aircopy.

    `aircopy`

    Parameters
    ----------
    add_info : dict
        Additional information for the projecta. The keys must be in the Billinge group projecta database schemas.

    max_records : int
        The maximum total number of records that will be returned.

    view : str
        The name or ID of a view.

    page_size : int
        The number of records returned in each request. Must be less than or equal to 100. Default is 100.

    fields : str or list
        Name of field or fields to be retrieved. Default is all fields.

    sort : list
        List of fields to sort by. Default order is ascending.

    formula : str
        Airtable formula.
    """
    if add_info is None:
        add_info = dict()
    options = dict()
    if max_records is not None:
        options.update({'add_info': max_records})
    if view is not None:
        options.update({'view': view})
    if page_size is not None:
        options.update({'page_size': page_size})
    if fields is not None:
        options.update({'fields': fields})
    if sort is not None:
        options.update({'sort': sort})
    if formula is not None:
        options.update({'formula': formula})
    base_id = os.getenv('AIRTABLE_BASE_ID')
    if base_id is None:
        raise EnvironmentError(
            "AIRTABLE_BASE_ID not found in environment. "
            "Please search your airtable base id online and export it as the environment variable AIRTABLE_BASE_ID"
        )
    api_token = os.getenv('AIRTABLE_API_TOKEN')
    if api_token is None:
        raise EnvironmentError(
            "AIRTABLE_API_TOKEN not found in environment. "
            "Please search your airtable base id online and export it as the environment variable AIRTABLE_API_TOKEN"
        )
    db = DataBase(base_id, api_token=api_token)
    projects, people, institutions = db.get_projecta(add_info, **options)
    io.write_docs_to_yaml('airtable_projects.yaml', projects)
    io.write_docs_to_yaml('airtable_people.yaml', people)
    io.write_docs_to_yaml('airtable_institutions.yaml', institutions)
    return


def main():
    """Fire aircopy."""
    fire.Fire(aircopy)


if __name__ == "__main__":
    main()
