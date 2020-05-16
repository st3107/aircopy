"""Parsers that parse the information queried from airtable to a pyhton dictionary following Billinge group database standard."""
from collections import OrderedDict
from airtable import Airtable
from typing import List, Any, Tuple
import aircopy.tools as tools
from aircopy.datatype import Record, Pair

import uuid

DEFAULT = {
    'pi_id': 'sbillinge',
    'name': '',
    'log_url': ''
}


def _retrieve(add_info: dict, key: str) -> Any:
    """Retrieve information from the dictionary. If not found, use the value in DEFAULT.

    Parameters
    ----------
    add_info : dict
        The addition information provided by the user.

    key : str
        The key to search inside the addition information.

    Returns
    -------
    value : Any
        The value from the add_info or DEFAULT or it is None.
    """
    return add_info.get(key, DEFAULT.get(key))


def parse_project(record: Record, add_info: dict) -> Tuple[Pair, List[Pair], List[Pair]]:
    """Parse the project record in airtable to Billinge group format. Return a key-value pair of the project and a list of key-value pairs of the people doc and institution doc in the project. The record should be denormalized at first.

    Parameters
    ----------
    record : Record
        The record from the airtable.

    add_info : dict
        A dictionary of the additional information.

    Returns
    -------

    """
    record = tools.get_data(record)
    pairs = list(map(parse_person, record.get('Collaborators', [])))
    people = [pair[0] for pair in pairs]
    institutions = [pair[1] for pair in pairs]
    key = record.get('Name')
    value = OrderedDict(
        {
            'begin_date': record.get('Start Date'),
            'collaborators': tools.get_keys(people),
            'description': record.get('Notes'),
            'grants': record.get('Grant'),
            'group_members': [tools.gen_person_id(record.get('Project Lead'))],
            'lead': tools.gen_person_id(record.get('Project Lead')),
            'log_url': _retrieve(add_info, 'log_url'),
            'ana_repo_url': record.get('Link to Analysis'),
            'man_repo_url': record.get('Link to Paper'),
            'milestones': tools.auto_gen_milestons(record.get('Start Date')),
            'name': _retrieve(add_info, 'name'),
            'pi_id': _retrieve(add_info, 'pi_id'),
            'status': record.get('Status')
        }
    )
    return (key, value), people, institutions


def parse_person(record: Record) -> Tuple[Pair, Pair]:
    record = tools.get_data(record)
    institutions = list(map(parse_institution, record.get('Institutions', [])))
    institution = institutions[0] if institutions else None
    key = record.get('ID')
    value = OrderedDict(
        {
            'name': '{} {}'.format(
                record.get('First Name'),
                record.get('Last Name')
            ),
            'aka': '{}, {}'.format(
                record.get('Last Name'),
                record.get('First Name')
            ),
            'institution': institution[0] if institution else None,
            'notes': [],
            'uuid': uuid.uuid4()
        }
    )
    tools.tag_date(value)
    return (key, value), institution


def parse_institution(record: Record) -> Tuple[str, dict]:
    record = tools.get_data(record)
    key = tools.gen_inst_id(record.get('Name', ''), 'u')
    value = OrderedDict(
        {
            'aka': [],
            'city': record.get('Address'),
            'state': record.get('State'),
            'county': record.get('County'),
            'name': record.get('Name')
        }
    )
    tools.tag_date(value)
    return key, value


if __name__ == "__main__":
    import pprint
    at = Airtable('appQbMUE26cMSSKdr', 'People', api_key='keyLPD6r72jho8O02')
    at1 = Airtable('appQbMUE26cMSSKdr', 'Projects', api_key='keyLPD6r72jho8O02')
    at2 = Airtable('appQbMUE26cMSSKdr', 'Institutions', api_key='keyLPD6r72jho8O02')
    pprint.pprint(at2.get('recFoBBdAy3cLxwYC'))
    pprint.pprint(at.get('rec6VLeAUdItvIqbY'))
    pprint.pprint(at1.get('rec6UVonazWUS1h94'))
