import pytest
from model.application import Application
from model.db import HospitalListDB
from copy import deepcopy

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
def prepared_app():
    return deepcopy(application)


def test_ask_for_index(prepared_app):
    prepared_app._input_method = lambda x: '77'
    index = prepared_app._ask_for_index()
    assert 77 == index + 1


def test_getting_non_int_for_index(prepared_app):
    prepared_app._input_method = lambda x: 'ыбавато'
    assert 'Ошибка. Требуется ввести целочисленное значение!' == \
           prepared_app.raise_patient_status()


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


def test_ask_yes(prepared_app):
    prepared_app._input_method = lambda x: 'да'
    boolean = prepared_app._ask_yes_or_no()
    assert True == boolean


def test_ask_no(prepared_app):
    prepared_app._input_method = lambda x: 'нет'
    boolean = prepared_app._ask_yes_or_no()
    assert False == boolean


def test_ask_about_discharge_from_hostpital(prepared_app):
    prepared_app._input_method = lambda x: 'нет'
    boolean = prepared_app._ask_about_discharge_from_hostpital()
    assert False == boolean


def test_just_raise_patient_status(prepared_app):
    prepared_app.db_interface.db = [1, 1, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    prepared_app._ask_about_discharge_from_hostpital = lambda: False

    new_status = prepared_app.raise_patient_status()
    assert 'Новый статус пациента: "Слегка болен"' == new_status
    assert prepared_app.db_interface.db == [1, 2, 1]


def test_try_to_raise_nonexistent_patient(prepared_app):
    prepared_app._ask_for_index = lambda: 100-1
    assert 'Пациент с индексом 100 не найден' == \
           prepared_app.raise_patient_status()


def test_do_not_discharge_patient_with_max_status(prepared_app):
    prepared_app.db_interface.db = [1, 3, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    prepared_app._ask_about_discharge_from_hostpital = lambda: False
    new_status = prepared_app.raise_patient_status()
    assert new_status == 'Пациент остался в статусе "Готов к выписке"'
    assert prepared_app.db_interface.db == [1, 3, 1]


def test_discharge_patient_with_max_status(prepared_app):
    prepared_app.db_interface.db = [1, 3, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    prepared_app._ask_about_discharge_from_hostpital = lambda: True
    new_status = prepared_app.raise_patient_status()
    assert new_status == 'Пациент с ID=2 выписан.'
    assert prepared_app.db_interface.db == [1, 1]


def test_just_reduce_patient_status(prepared_app):
    prepared_app.db_interface.db = [1, 3, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    new_status = prepared_app.reduce_patient_status()
    assert new_status == 'Новый статус пациента: "Слегка болен"'
    assert prepared_app.db_interface.db == [1, 2, 1]


def test_try_to_reduce_min_status(prepared_app):
    expected_status = \
        'У этого пациента самый низкий статус "Тяжело болен".\n' \
        'Статус пациента не изменился, т.к. в нашей больнице пациенты не умирают!\n'

    prepared_app.db_interface.db = [1, 0, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    new_status = prepared_app.reduce_patient_status()
    assert new_status == expected_status
    assert prepared_app.db_interface.db == [1, 0, 1]


def test_calc_statistics(prepared_app):
    statistics = prepared_app._calc_patients_stat_by_groups()
    assert statistics == {0: 1, 1: 4, 2: 3, 3: 2}


def test_stop_dialog(prepared_app):
    stop_message = prepared_app.stop_dialog()
    assert stop_message == 'Сеанс завершён.'
    assert prepared_app.time_to_exit == True


def test_get_status(prepared_app):
    prepared_app.db_interface.db = [1, 3, 1]
    prepared_app._ask_for_index = lambda: 2 - 1
    status = prepared_app.ask_and_print_patient_status()
    assert 'Готов к выписке' == status


def test_get_non_existent_patient_status(prepared_app):
    prepared_app.db_interface.db = [1, 3, 1]
    prepared_app._ask_for_index = lambda: 100-1
    assert 'Пациент с индексом 100 не найден' == \
           prepared_app.ask_and_print_patient_status()


def test_print_statistics_by_patients_groups(prepared_app):
    prepared_app.db_interface.db = [
        0,
        1, 1,
        2, 2, 2,
        3, 3, 3, 3
    ]
    expected_statistics_text = \
        'В больнице на данный момент находится 10 пациентов, из них:\n' \
        ' - в статусе "Тяжело болен": 1 чел.\n' \
        ' - в статусе "Болен": 2 чел.\n' \
        ' - в статусе "Слегка болен": 3 чел.\n' \
        ' - в статусе "Готов к выписке": 4 чел.'
    actual_statistics_text = prepared_app.print_statistics_by_patients_groups()
    assert actual_statistics_text == expected_statistics_text


def test_print_statistics_with_one_group(prepared_app):
    prepared_app.db_interface.db = [
        1, 1,
    ]
    expected_statistics_text = \
        'В больнице на данный момент находится 2 пациентов, из них:\n' \
        ' - в статусе "Болен": 2 чел.'
    actual_statistics_text = prepared_app.print_statistics_by_patients_groups()
    assert actual_statistics_text == expected_statistics_text
