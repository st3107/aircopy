"""The tools for data operation and the wrapper for the airtable database."""
from airtable import Airtable
from aircopy.datatype import Record
import aircopy.tools as tools
import copy
from typing import Union, List


def query(db: Airtable, uid: str, only_data: bool):
    """Query the data by the unique id from airtable.

    Parameters
    ----------
    db : Airtable
        The airtable client.

    uid : str
        The airtbale style uid.

    only_data : bool
        If True, only the value for the 'fields' in record will be returned. Otherwise, return whole record.

    Returns
    -------
    record : Record or Fields
        The dictionary of the data.
    """
    record = db.get(uid)
    if only_data:
        return record.get('fields')
    return record


def denormalize_project(project: Record, people: Airtable, institutions: Airtable, only_data: bool = False, inplace: bool = False) -> Union[None, dict]:
    """Denormalize the project record from airtbale.

    Parameters
    ----------
    project : Record
        The record the project.

    people : Airtable
        The airtable client of 'People'.

    institutions : Airtable
        The airtable client of 'Institutions'.

    only_data : bool
        If True, only the value for the 'fields' in record will be returned. Otherwise, return whole record.

    inplace : bool
        If True, demoralization is done inplace. Otherwise, return the denormalized copy of the project record.

    Returns
    -------
    project : None or dict
        If inplace == False, return the denormalized record. Otherwise, denormalize inplace and return None.
    """
    if not inplace:
        project = copy.deepcopy(project)
    project = tools.get_data(project)
    if 'Collaborators' in project:
        project['Collaborators'] = [
            query(people, uid, only_data=only_data)
            for uid in project['Collaborators']
        ]
        for collaborator in project['Collaborators']:
            if 'Institutions' in collaborator:
                collaborator['Institutions'] = [
                    query(institutions, uid, only_data=only_data)
                    for uid in collaborator['Institutions']
                ]
    if not inplace:
        return project
    return


class DataBase:
    """A collection of airtables at the same base."""
    def __init__(self, base_id: str, tables: List[str], api_token: str = None):
        """
        Initiate the class. Attributes will be added as the name of the table and its corresponding Airtable object.

        Parameters
        ----------
        base_id : str
            The base id for the airtables.

        tables : list
            The name of the tables.
        """
        for table in tables:
            self.__setattr__(table, Airtable(base_id, table, api_key=api_token))
