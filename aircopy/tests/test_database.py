import aircopy.database as database


def test_denormalize_project(real_db):
    if real_db is None:
        return
    record = real_db.Projects.get('rec6UVonazWUS1h94')
    assert database.denormalize_project(record, real_db.People, real_db.Institutions, inplace=False)
    assert database.denormalize_project(record, real_db.People, real_db.Institutions, inplace=False, only_data=True)


def test_get_projecta(real_db):
    assert next(real_db.get_projecta({}))
