"""Tools used in the module."""
from collections import OrderedDict
from typing import List, Iterable
from datetime import datetime, timedelta
from nameparser import HumanName
from aircopy.datatype import Record


MILESTONES_TEMPLATE = [
    OrderedDict(
        {'audience': ['pi', 'lead', 'group members', 'collaborators'],
         'due_date': timedelta(days=7),
         'name': 'Kick off meeting',
         'objective': 'roll out of project to team',
         'status': 'proposed'}
    ),
    OrderedDict(
        {'audience': ['pi', 'lead', 'group members'],
         'due_date': timedelta(days=14),
         'name': 'Project lead presentation',
         'objective': 'lead presents background reading and initial project plan',
         'status': 'proposed'}
    ),
    OrderedDict(
        {'audience': ['pi', 'lead', 'group members'],
         'due_date': timedelta(days=28),
         'name': 'planning meeting',
         'objective': 'develop a detailed plan with dates',
         'status': 'proposed'}
    ),
    OrderedDict(
        {'audience': ['pi', 'lead', 'group members', 'collaborators'],
         'due_date': timedelta(days=365),
         'name': 'submission',
         'objective': 'submit the paper, release the code, whatever',
         'status': 'proposed'}
    )
]

SPECIAL_ID = {
    'Songsheng Tao': 'sstao'
}


def gen_person_id(name: str) -> str:
    """Generate the id of the person."""
    if name in SPECIAL_ID:
        return SPECIAL_ID.get(name)
    hn = HumanName(name)
    return '{}{}'.format(hn.first[0], hn.last).lower()


def auto_gen_milestons(start_date: str, template: List[dict] = None) -> List[OrderedDict]:
    """Automatically generate the milestones list according to the template."""
    if template is None:
        template = MILESTONES_TEMPLATE.copy()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    for milestone in template:
        time_gap = milestone['due_date']
        due_date = start_date + time_gap
        milestone['due_date'] = due_date.strftime('%Y-%m-%d')
    return template


def tag_date(record: dict, turn_off: tuple = ()):
    """Tag the record dictionary with today date time."""
    today = datetime.today()
    now = today.now()
    date = {
        'day': today.day,
        'month': today.month,
        'year': today.year,
        'updated': now
    }
    for key in turn_off:
        date.pop(key)
    record.update(date)
    return


def get_keys(pairs: Iterable[tuple]) -> list:
    """Get the key of a iterable of key value pairs."""
    return [pair[0] for pair in pairs]


def gen_inst_id(name: str, mode: str):
    """Generate the key according to the name."""
    def gen_key_u(_name: str):
        return str(_name.lower().replace(' of ', "").replace(" ", "").replace("university", "u"))

    def gen_key_d(_name: str):
        _name = _name.lower()
        if "department" in _name:
            return _name.replace("department of", "").replace("department", "").replace(" ", "")
        else:
            return ''.join(_name.split())

    def gen_key_s(_name: str):
        _name = _name.lower()
        if "school" in _name:
            return _name.replace("school of", "").replace("school", "").replace(" ", "")
        else:
            return ''.join(_name.split())

    dct = {
        'u': gen_key_u,
        'd': gen_key_d,
        's': gen_key_s
    }
    if mode not in dct:
        raise ValueError(f"Unknown mode: {mode}")
    method = dct.get(mode)
    return method(name)


def get_data(record: Record):
    """Get the data in a record from the airtable api."""
    if 'fields' not in record:
        raise ValueError(
            "'fields' not found in the following record {}".format(record)
        )
    return record.get('fields')
