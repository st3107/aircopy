"""The cli interface."""
import os

import fire

import aircopy.io as io
from aircopy.database import DataBase


def aircopy(add_info: dict = None, **options):
    """Transfer the data from Airtbale to Billinge group projecta database. It will read the variables 'AIRTABLE_BASE_ID'
    and 'AIRTABLE_API_TOKEN' inside your environment and connect to your airtable database, download the content and
    parse it into Billinge group database documents and write it out to yaml files.

    Parameters
    ----------
    add_info : dict
        Additional information for the projecta. The keys must be in the Billinge group projecta database schemas.

    options : dict
        The view and filter options. Include
            max_records (``int``, optional): The maximum total number of
                records that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            page_size (``int``, optional ): The number of records returned
                in each request. Must be less than or equal to 100.
                Default is 100. See :any:`PageSizeParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.
    """
    if add_info is None:
        add_info = dict()
    base_id = os.environ['AIRTABLE_BASE_ID']
    api_token = os.environ['AIRTABLE_API_TOKEN']
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
