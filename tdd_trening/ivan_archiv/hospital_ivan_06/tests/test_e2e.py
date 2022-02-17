import pytest
from model.application import Application
from model.db import HospitalListDB


def extended_fake_inputs(inputs_chain):
    """
    Элемены из inputs_chain по очереди отправляются при каждом
    вызове _input_method класса Application
    """
    inputs_chain = inputs_chain[::-1]

    def inner(text):
        return inputs_chain.pop()
    return inner


def save_print_chain(prints_chain):
    """
    В save_print_chain сохраняются элементы
    отправленные в _print_method класса Application
    """
    prints_chain = prints_chain

    def inner(text):
        prints_chain.append(text)
    return inner


@pytest.fixture(scope="function")
def prepared_app():
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


def get_inputs_and_expected_outputs(input_output_list):
    user_inputs = []
    expected_outputs = []
    for ipt in input_output_list:
        user_inputs += ipt['input']
    for ipt in input_output_list:
        expected_outputs += ipt['output']
    return user_inputs, expected_outputs


def test_get_patient_status(prepared_app):
    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input':  ['узнать статус пациента', 2],
            'output': ['Болен']
        },
        {
            'input':  ['узнать статус пациента', 140],
            'output': ['Пациент с указанным индексом отсутствует']
        },
        {
            'input':  ['стоп'],
            'output': ['Сеанс завершён.']
        },
    ])
    apps_outputs = []
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(apps_outputs)

    prepared_app.start_dialog_with_user()

    assert expected_outputs == apps_outputs


def test_raise_patient_status(prepared_app):
    prepared_app.db_interface.db = [1, 2, 1]
    patient_id = 2
    max_status_alert = 'У этого пациента самый высокий статус "Готов к выписке".\n' \
                       'Желаете ли выписать этого пациента?'

    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input':  ['узнать статус пациента', patient_id],
            'output': ['Слегка болен']
        },
        {
            'input':  ['повысить статус пациента', patient_id],
            'output': ['Новый статус пациента: "Готов к выписке"']
        },
        {
            'input':  ['узнать статус пациента', patient_id],
            'output': ['Готов к выписке']
        },
        {
            'input':  ['повысить статус пациента', patient_id, 'нет'],
            'output': [max_status_alert, 'Пациент остался в статусе "Готов к выписке"']
        },
        {
            'input':  ['повысить статус пациента', patient_id, 'да'],
            'output': [max_status_alert, f'Пациент с ID={patient_id} выписан.']
        },
        {
            'input':  ['стоп'],
            'output': ['Сеанс завершён.']
        },
    ])

    prints_chain = []
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(prints_chain)

    prepared_app.start_dialog_with_user()

    expected_patient_db = [1, 1]
    assert expected_outputs == prints_chain
    assert prepared_app.db_interface.db == expected_patient_db


def test_reduce_patient_status(prepared_app):
    min_status_text = 'У этого пациента самый низкий статус ' \
                      f'"{prepared_app.statuses[prepared_app.min_status]}".\n' \
                      'Статус пациента не изменился, т.к. в нашей больнице ' \
                      'пациенты не умирают!\n'
    prepared_app.db_interface.db = [1, 1, 1]

    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input': ['узнать статус пациента', 2],
            'output': ['Болен']
        },
        {
            'input': ['понизить статус пациента', 2],
            'output': ['Новый статус пациента: "Тяжело болен"']
        },
        {
            'input': ['узнать статус пациента', 2],
            'output': ['Тяжело болен']
        },
        {
            'input': ['понизить статус пациента', 2],
            'output': [min_status_text]
        },
        {
            'input': ['стоп'],
            'output': ['Сеанс завершён.']
        }

    ])
    prints_chain = []
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(prints_chain)

    prepared_app.start_dialog_with_user()

    assert expected_outputs == prints_chain
    assert prepared_app.db_interface.db == [1, 0, 1]


def test_print_statistics_by_patients_groups(prepared_app):
    prepared_app.db_interface.db = [
        0,
        1, 1, 1, 1,
        2, 2, 2,
        3, 3,
    ]
    prints_chain = []
    statistics_text = '''В больнице на данный момент находится 10, из них:
 - в статусе "Тяжело болен": 1 чел.
 - в статусе "Болен": 4 чел.
 - в статусе "Слегка болен": 3 чел.
 - в статусе "Готов к выписке": 2 чел.'''

    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input':  ['рассчитать статистику'],
            'output': [statistics_text]
        },
        {
            'input':  ['стоп'],
            'output': ['Сеанс завершён.']
        }
    ])
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(prints_chain)
    prepared_app.start_dialog_with_user()

    assert expected_outputs == prints_chain


def test_unknown_command(prepared_app):
    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input':  ['йцукен'],
            'output': ['Неизвестная команда! Попробуйте ещё раз']
        },
        {
            'input':  ['стоп'],
            'output': ['Сеанс завершён.']
        }
    ])
    prints_chain = []
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(prints_chain)

    prepared_app.start_dialog_with_user()
    assert expected_outputs == prints_chain


def test_command_match(prepared_app):
    user_inputs, expected_outputs = get_inputs_and_expected_outputs([
        {
            'input':  ['йцукен'],
            'output': ['Неизвестная команда! Попробуйте ещё раз']
        },
        {
            'input':  ['стоп'],
            'output': ['Сеанс завершён.']
        }
    ])
    prints_chain = []
    prepared_app._input_method = extended_fake_inputs(user_inputs)
    prepared_app._print_method = save_print_chain(prints_chain)

    prepared_app.start_dialog_with_user()
    assert expected_outputs == prints_chain
