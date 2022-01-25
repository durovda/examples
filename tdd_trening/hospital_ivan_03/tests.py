import pytest
from hostpital import Application
from db import HospitalListDB


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
        'узнать статус пациента', 140,
        'стоп'
    ]
    prints_chain = []
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    prepared_app_with_db._print_method = save_print_chain(prints_chain)

    prepared_app_with_db.start_dialog_with_user()
    assert ['Болен', 'Пациент с указанным индексом отсутствует',
            'Сеанс завершён.'] == prints_chain


def test_raise_patient_status(prepared_app_with_db):
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


def test_ask_for_index(prepared_app_with_db):
    user_inputs = [
        '77',
    ]
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    index = prepared_app_with_db._ask_for_index()
    assert 77 == index - 1


def test_ask_yes(prepared_app_with_db):
    user_inputs = [
        'да',
    ]
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    boolean = prepared_app_with_db._ask_yes_or_no()
    assert True == boolean


def test_ask_no(prepared_app_with_db):
    user_inputs = [
        'нет',
    ]
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    boolean = prepared_app_with_db._ask_yes_or_no()
    assert False == boolean


def test_ask_about_discharge_from_hostpital(prepared_app_with_db):
    user_inputs = [
        'нет',
    ]
    prepared_app_with_db._input_method = extended_fake_inputs(user_inputs[::-1])
    boolean = prepared_app_with_db._ask_about_discharge_from_hostpital()
    assert False == boolean


def test_calc_statistics(prepared_app_with_db):
    statistics = prepared_app_with_db._calc_patients_stat_by_groups()
    assert statistics == {0: 1, 1: 4, 2: 3, 3: 2}


@pytest.fixture(scope="function")
def db_for_db_tests():
    return HospitalListDB([0,
                           1, 1, 1, 1,
                           2, 2, 2,
                           3, 3,
                           ])


def test_db_get_total_patients_count(db_for_db_tests):
    assert 10 == db_for_db_tests.get_total_patients_count()


def test_db_get_patients_count_by_status(db_for_db_tests):
    assert 3 == db_for_db_tests.get_patients_count_by_status(2)


def test_db_update_patient_status(db_for_db_tests):
    new_status = 7
    patient_index = 1
    db_for_db_tests.update_patient_status(patient_index, new_status)
    assert db_for_db_tests.db[patient_index] == new_status


def test_db_get_patient_by_index(db_for_db_tests):
    assert 1 == db_for_db_tests.get_patient_status_by_index(1)


def test_db_delete_patient(db_for_db_tests):
    len_before = len(db_for_db_tests.db)
    patient_index = 9
    db_for_db_tests.delete_patient(patient_index)
    len_after = len(db_for_db_tests.db)
    assert not db_for_db_tests.get_patient_status_by_index(patient_index)
    assert len_before - 1 == len_after
