import pytest
from collections import OrderedDict

DB = {
    'Blogroll': ['recKm29VrzmM6eyjs'],
    'Collaborators': [{'First Name': 'Randy',
                       'ID': 'rnangah',
                       'Institutions': [
                           {'Address': 'Yaounde, Cameroon',
                            'Collaborators 2': ['rec6VLeAUdItvIqbY'],
                            'Name': 'University of Yaounde'}
                       ],
                       'Last Name': 'Nangah',
                       'Manuscripts': ['recoZh0EL9qM0ufyD'],
                       'Projects': ['rec6UVonazWUS1h94']}],
    'Grant': ['dmrefcheme16'],
    'Link to Analysis': 'http://gitlab.thebillingegroup.com/analysis/19st_sponge',
    'Link to Paper': 'http://gitlab.thebillingegroup.com/papers/19st_sponge',
    'Manuscripts': ['recoZh0EL9qM0ufyD'],
    'Name': '19st_sponge',
    'Notes': 'la la la ...',
    'Project Lead': 'Songsheng Tao',
    'Samples': ['rec0Rnl9YH7h8aw33',
                'recCOTctyb1eJXqG3',
                'recAC9R3jPzuEn1gJ',
                'recd8drZvs0yfRUCt'],
    'Start Date': '2019-03-04',
    'Status': '6 Report Sent'
}

PROJECT = OrderedDict(
    [
        ('begin_date', '2019-03-04'),
        ('collaborators', ['rnangah']),
        ('description', 'la la la ...'),
        ('grants', ['dmrefcheme16']),
        ('group_members', ['sstao']),
        ('lead', 'sstao'),
        ('log_url', ''),
        ('ana_repo_url',
         'http://gitlab.thebillingegroup.com/analysis/19st_sponge'),
        ('man_repo_url',
         'http://gitlab.thebillingegroup.com/papers/19st_sponge'),
        ('milestones',
         [
             OrderedDict([('audience',
                           ['pi', 'lead', 'group members', 'collaborators']),
                          ('due_date', '2019-03-11'),
                          ('name', 'Kick off meeting'),
                          ('objective', 'roll out of project to team'),
                          ('status', 'proposed')]),
             OrderedDict([('audience', ['pi', 'lead', 'group members']),
                          ('due_date', '2019-03-18'),
                          ('name', 'Project lead presentation'),
                          ('objective',
                           'lead presents background reading and initial '
                           'project plan'),
                          ('status', 'proposed')]),
             OrderedDict([('audience', ['pi', 'lead', 'group members']),
                          ('due_date', '2019-04-01'),
                          ('name', 'planning meeting'),
                          ('objective', 'develop a detailed plan with dates'),
                          ('status', 'proposed')]),
             OrderedDict([('audience',
                           ['pi', 'lead', 'group members', 'collaborators']),
                          ('due_date', '2020-03-03'),
                          ('name', 'submission'),
                          ('objective',
                           'submit the paper, release the code, whatever'),
                          ('status', 'proposed')])
         ]
         ),
        ('name', ''),
        ('pi_id', 'sbillinge'),
        ('status', '6 Report Sent')
    ]
)


@pytest.fixture
def fake_db():
    return DB


@pytest.fixture
def example_project():
    return PROJECT
