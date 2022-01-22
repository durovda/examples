import pytest
from hostpital import Application, HospitalListDB


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
    database = HospitalListDB([0,
                               1, 1, 1, 1,
                               2, 2, 2,
                               3, 3,
                               ])
    return Application(database, statuses)


def test_get_patient_status(prepared_app_with_db):
    user_inputs = [
        'узнать статус пациента', 2,
        'стоп'
    ]
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert ['Болен', 'Сеанс завершён.'] == prints_chain


def test_raise_patient_status(prepared_app_with_db):
    user_inputs = [
        'узнать статус пациента', 8,
        'повысить статус пациента', 8,
        'узнать статус пациента', 8,
        'повысить статус пациента', 8,
        'да',
        'стоп'
    ]
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert ['Слегка болен',
            'Новый статус пациента: "Готов к выписке"',
            'Готов к выписке',
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
    assert ['Болен',
            'Новый статус пациента: "Тяжело болен"',
            'Сеанс завершён.'] == prints_chain
