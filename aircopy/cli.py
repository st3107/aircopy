"""The cli interface."""
import aircopy.parser as parser
import aircopy.database as database
from airtable import Airtable


def get_projecta_docs(projects: Airtable, people: Airtable, institutions: Airtable, add_info: dict, **options):
    for page in projects.get_iter(**options):
        for record in page:
            database.denormalize_project(record, people, institutions, inplace=True)
            yield parser.parse_project(record, add_info)

