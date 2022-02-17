import pytest
from app.hostpital import Application
from app.db import HospitalListDB


def extended_fake_inputs(inputs_chain):
    """
    Элемены из inputs_chain по очереди отправляются при каждом
    вызове _input_method класса Application
    """
    inputs_chain = inputs_chain

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


def get_inputs_and_expected_outputs(input_output_list):
    user_inputs = []
    expected_outputs = []
    for ipt in input_output_list:
        user_inputs += ipt['input']
    for ipt in input_output_list:
        expected_outputs += ipt['output']
    return user_inputs, expected_outputs


def test_get_patient_status(prepared_app_with_db):
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
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(apps_outputs)

    prepared_app_with_db.start_dialog_with_user()

    assert expected_outputs == apps_outputs


def test_raise_patient_status(prepared_app_with_db):
    patient_db = [1, 2, 1]
    # prepared_app_with_db.db = patient_db
    patient_id = 6
    user_inputs = [
        'узнать статус пациента', patient_id,
        'повысить статус пациента', patient_id,
        'узнать статус пациента', patient_id,
        'повысить статус пациента', patient_id,
        'нет',
        'повысить статус пациента', patient_id,
        'да',
        'стоп'
    ]
    max_status_alert = 'У этого пациента самый высокий статус "Готов к выписке".\n' \
                       'Желаете ли выписать этого пациента?'
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    expected_patient_db = [1, 1]
    assert ['Слегка болен',
            'Новый статус пациента: "Готов к выписке"',
            'Готов к выписке',
            max_status_alert,
            max_status_alert,
            'Сеанс завершён.'] == prints_chain


def test_reduce_patient_status(prepared_app_with_db):
    user_inputs = [
        'узнать статус пациента', 2,
        'понизить статус пациента', 2,
        'узнать статус пациента', 2,
        'понизить статус пациента', 2,
        'стоп'
    ]
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert [
           'Болен',
           'Новый статус пациента: "Тяжело болен"',
           'Тяжело болен',
           'У этого пациента самый низкий статус '
           f'"{prepared_app_with_db.statuses[prepared_app_with_db.min_status]}".\n'
           'Статус пациента не изменился, т.к. в нашей больнице '
           'пациенты не умирают!\n',
           'Сеанс завершён.'] == prints_chain


def test_print_statistics_by_patients_groups(prepared_app_with_db):
    user_inputs = [
        'рассчитать статистику',
        'стоп'
    ]
    prints_chain = []
    statistics_text = '''В больнице на данный момент находится 10, из них:
 - в статусе "Тяжело болен": 1 чел.
 - в статусе "Болен": 4 чел.
 - в статусе "Слегка болен": 3 чел.
 - в статусе "Готов к выписке": 2 чел.'''

    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert [statistics_text, 'Сеанс завершён.'] == prints_chain


def test_unknown_command(prepared_app_with_db):
    user_inputs = [
        'йцукен',
        'стоп'
    ]
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert ['Неизвестная команда! Попробуйте ещё раз',
            'Сеанс завершён.'] == prints_chain