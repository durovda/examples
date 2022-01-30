import pytest
from app.hostpital import Application
from app.db import HospitalListDB


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
application = Application(database, statuses)


@pytest.fixture(scope="function")
def prepared_app_with_db():
    return application


def test_ask_for_index(prepared_app_with_db):
    prepared_app_with_db._input_method = lambda x: '77'
    index = prepared_app_with_db._ask_for_index()
    assert 77 == index + 1


empty_application = Application()


@pytest.mark.parametrize("command,expected_method", [
    ('рассчитать статистику', empty_application.print_statistics_by_patients_groups),
    ('узнать статус пациента', empty_application.ask_and_print_patient_status),
    ('повысить статус пациента', empty_application.raise_patient_status),
    ('понизить статус пациента', empty_application.reduce_patient_status),
    ('стоп', empty_application.stop_dialog),
    ('StOp', empty_application.stop_dialog),
])
def test_match_command(command,
                       expected_method):
    reterned_method = empty_application.match_command(command)
    assert reterned_method == expected_method


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
