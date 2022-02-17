import pytest
from model.application import Application, YesOrNoError
from copy import deepcopy

application = Application()


@pytest.fixture(scope="function")
def app():
    return deepcopy(application)


def test_ask_for_index(app):
    app._input_method = lambda x: '77'
    index = app._request_for_index()
    assert index + 1 == 77


def test_getting_non_int_for_index(app):
    app._input_method = lambda x: 'ыбавато'
    assert app._cmd_raise_patient_status() == \
           'Ошибка. Требуется ввести целочисленное значение!'


@pytest.mark.parametrize("command,expected_method", [
    ('рассчитать статистику', application._cmd_print_statistics_by_patients_groups),
    ('узнать статус пациента', application._cmd_get_patient_status),
    ('повысить статус пациента', application._cmd_raise_patient_status),
    ('понизить статус пациента', application._cmd_reduce_patient_status),
    ('стоп', application._cmd_stop_dialog),
    ('StOp', application._cmd_stop_dialog),
])
def test_match_command(command,
                       expected_method):
    returned_method = application._match_command(command)
    assert returned_method == expected_method


def test_answer_yes(app):
    app._input_method = lambda x: 'да'
    confirmed = app \
        ._request_confirmation_about_discharge_from_hostpital()
    assert confirmed


def test_answer_nonsense(app):
    app._input_method = lambda x: 'asdfasdf'
    with pytest.raises(YesOrNoError):
        app._request_confirmation_about_discharge_from_hostpital()


def test_answer_no(app):
    app._input_method = lambda x: 'нет'
    confirmed = app._request_confirmation_about_discharge_from_hostpital()
    assert not confirmed


def test_ask_about_discharge_from_hostpital(app):
    app._input_method = lambda x: 'нет'
    boolean = app._request_confirmation_about_discharge_from_hostpital()
    assert boolean is False


def test_just_raise_patient_status(app):
    app.db_interface.db = [1, 1, 1]
    app._request_for_index = lambda: 2 - 1
    app._request_confirmation_about_discharge_from_hostpital = lambda: False

    new_status = app._cmd_raise_patient_status()
    assert new_status == 'Новый статус пациента: "Слегка болен"'
    assert app.db_interface.db == [1, 2, 1]


def test_try_to_raise_nonexistent_patient(app):
    app._request_for_index = lambda: 100 - 1
    assert app._cmd_raise_patient_status() == \
           'Пациент с индексом 100 не найден'


def test_do_not_discharge_patient_with_max_status(app):
    app.db_interface.db = [1, 3, 1]
    app._request_for_index = lambda: 2 - 1
    app._request_confirmation_about_discharge_from_hostpital = lambda: False
    new_status = app._cmd_raise_patient_status()
    assert new_status == 'Пациент остался в статусе "Готов к выписке"'
    assert app.db_interface.db == [1, 3, 1]


def test_discharge_patient_with_max_status(app):
    app.db_interface.db = [1, 3, 1]
    app._request_for_index = lambda: 2 - 1
    app._request_confirmation_about_discharge_from_hostpital = lambda: True
    new_status = app._cmd_raise_patient_status()
    assert new_status == 'Пациент с ID=2 выписан.'
    assert app.db_interface.db == [1, 1]


def test_just_reduce_patient_status(app):
    app.db_interface.db = [1, 3, 1]
    app._request_for_index = lambda: 2 - 1
    new_status = app._cmd_reduce_patient_status()
    assert new_status == 'Новый статус пациента: "Слегка болен"'
    assert app.db_interface.db == [1, 2, 1]


def test_try_to_reduce_min_status(app):
    expected_status = \
        'У этого пациента самый низкий статус "Тяжело болен".\n' \
        'Статус пациента не изменился, т.к. в нашей больнице пациенты не умирают!\n'

    app.db_interface.db = [1, 0, 1]
    app._request_for_index = lambda: 2 - 1
    new_status = app._cmd_reduce_patient_status()
    assert new_status == expected_status
    assert app.db_interface.db == [1, 0, 1]


def test_stop_dialog(app):
    stop_message = app._cmd_stop_dialog()
    assert stop_message == 'Сеанс завершён.'
    assert app.time_to_exit is True


def test_get_status(app):
    app.db_interface.db = [1, 3, 1]
    app._request_for_index = lambda: 2 - 1
    status = app._cmd_get_patient_status()
    assert status == 'Готов к выписке'


def test_get_non_existent_patient_status(app):
    app.db_interface.db = [1, 3, 1]
    app._request_for_index = lambda: 100 - 1
    assert app._cmd_get_patient_status() == \
           'Пациент с индексом 100 не найден'


def test_print_statistics_by_patients_groups(app):
    app.db_interface.db = [
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
    actual_statistics_text = app._cmd_print_statistics_by_patients_groups()
    assert actual_statistics_text == expected_statistics_text


def test_print_statistics_with_one_group(app):
    app.db_interface.db = [
        1, 1,
    ]
    expected_statistics_text = \
        'В больнице на данный момент находится 2 пациентов, из них:\n' \
        ' - в статусе "Болен": 2 чел.'
    actual_statistics_text = app._cmd_print_statistics_by_patients_groups()
    assert actual_statistics_text == expected_statistics_text
