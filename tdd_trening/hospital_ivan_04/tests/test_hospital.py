import pytest
from app.hostpital import Application
from app.db import HospitalListDB


@pytest.fixture(scope="function")
def prepared_app_with_db():
    statuses = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке',
    }
    database = HospitalListDB([
        0,
        1, 1, 1, 1,
        2, 2, 2,
        3, 3,
    ])
    return Application(database, statuses)


def test_ask_for_index(prepared_app_with_db):
    prepared_app_with_db._input_method = lambda x: '77'
    index = prepared_app_with_db._ask_for_index()
    assert 77 == index - 1


def test_ask_yes(prepared_app_with_db):
    prepared_app_with_db._input_method = lambda x: 'да'
    boolean = prepared_app_with_db._ask_yes_or_no()
    assert True == boolean


def test_ask_no(prepared_app_with_db):
    prepared_app_with_db._input_method = lambda x: 'нет'
    boolean = prepared_app_with_db._ask_yes_or_no()
    assert False == boolean


def test_ask_about_discharge_from_hostpital(prepared_app_with_db):

    prepared_app_with_db._input_method = lambda x: 'нет'

    boolean = prepared_app_with_db._ask_about_discharge_from_hostpital()
    assert False == boolean


def test_calc_statistics(prepared_app_with_db):
    statistics = prepared_app_with_db._calc_patients_stat_by_groups()
    assert statistics == {0: 1, 1: 4, 2: 3, 3: 2}
