import pytest
from model.application import Application
from tests.e2e_mocks import get_prompts_inputs_and_expected_outputs, mock_app_input_and_print_methods


@pytest.fixture(scope="function")
def app():
    return Application()


def test_get_patient_status(app):
    app.db_interface.db = [0, 1, 0]
    expeted_prompts, user_inputs, expected_outputs = \
        get_prompts_inputs_and_expected_outputs([
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', 2]],
                'output': ['Болен']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', 140]],
                'output': ['Пациент с индексом 140 не найден']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'стоп']],
                'output': ['Сеанс завершён.']
            },
        ])

    actual_prompts, actual_outputs = \
        mock_app_input_and_print_methods(app, user_inputs)
    app.start_dialog_with_user()

    assert actual_outputs == expected_outputs
    assert actual_prompts == expeted_prompts


def test_raise_patient_status(app):
    app.db_interface.db = [1, 2, 1]
    expected_patient_db = [1, 1]
    patient_id = 2
    max_status_alert = \
        'У этого пациента самый высокий статус "Готов к выписке".\n' \
        'Желаете ли выписать этого пациента?'

    expeted_prompts, user_inputs, expected_outputs = \
        get_prompts_inputs_and_expected_outputs([
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', patient_id]],
                'output': ['Слегка болен']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'повысить статус пациента'],
                    ['Введите ID пациента: ', patient_id]],
                'output': ['Новый статус пациента: "Готов к выписке"']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', patient_id]],
                'output': ['Готов к выписке']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'повысить статус пациента'],
                    ['Введите ID пациента: ', patient_id],
                    ['(да/нет) ', 'нет']
                ],
                'output': [max_status_alert, 'Пациент остался в статусе "Готов к выписке"']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'повысить статус пациента'],
                    ['Введите ID пациента: ', patient_id],
                    ['(да/нет) ', 'да']
                ],
                'output': [max_status_alert, f'Пациент с ID={patient_id} выписан.']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'стоп']],
                'output': ['Сеанс завершён.']
            },
        ])

    actual_prompts, actual_outputs = mock_app_input_and_print_methods(app, user_inputs)

    app.start_dialog_with_user()

    assert actual_outputs == expected_outputs
    assert actual_prompts == expeted_prompts

    assert app.db_interface.db == expected_patient_db


def test_reduce_patient_status(app):
    min_status_text = 'У этого пациента самый низкий статус ' \
                      '"Тяжело болен".\n' \
                      'Статус пациента не изменился, т.к. в нашей больнице ' \
                      'пациенты не умирают!\n'
    app.db_interface.db = [1, 1, 1]

    expeted_prompts, user_inputs, expected_outputs = \
        get_prompts_inputs_and_expected_outputs([
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', 2]
                ],
                'output': ['Болен']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'понизить статус пациента'],
                    ['Введите ID пациента: ', 2]
                ],
                'output': ['Новый статус пациента: "Тяжело болен"']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'узнать статус пациента'],
                    ['Введите ID пациента: ', 2]
                ],
                'output': ['Тяжело болен']
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'понизить статус пациента'],
                    ['Введите ID пациента: ', 2]
                ],
                'output': [min_status_text]
            },
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'стоп']
                ],
                'output': ['Сеанс завершён.']
            }

        ])
    actual_prompts, actual_outputs = mock_app_input_and_print_methods(app, user_inputs)

    app.start_dialog_with_user()

    assert actual_outputs == expected_outputs
    assert actual_prompts == expeted_prompts
    assert app.db_interface.db == [1, 0, 1]


def test_print_statistics_by_patients_groups(app):
    app.db_interface.db = [
        0,
        1, 1, 1, 1,
        2, 2, 2,
        3, 3,
    ]
    statistics_text = '''В больнице на данный момент находится 10 пациентов, из них:
 - в статусе "Тяжело болен": 1 чел.
 - в статусе "Болен": 4 чел.
 - в статусе "Слегка болен": 3 чел.
 - в статусе "Готов к выписке": 2 чел.'''

    expeted_prompts, user_inputs, expected_outputs = \
        get_prompts_inputs_and_expected_outputs([
            {
                'prompt_and_input': [
                    ['Введите команду: ', 'рассчитать статистику']],
                'output': [statistics_text]
            },
            {
                'prompt_and_input': [['Введите команду: ', 'стоп']],
                'output': ['Сеанс завершён.']
            }
        ])
    actual_prompts, actual_outputs = mock_app_input_and_print_methods(app, user_inputs)

    app.start_dialog_with_user()

    assert actual_outputs == expected_outputs
    assert actual_prompts == expeted_prompts


def test_unknown_command(app):
    expeted_prompts, user_inputs, expected_outputs = \
        get_prompts_inputs_and_expected_outputs([
            {
                'prompt_and_input': [['Введите команду: ', 'йцукен']],
                'output': ['Неизвестная команда! Попробуйте ещё раз']
            },
            {
                'prompt_and_input': [['Введите команду: ', 'стоп']],
                'output': ['Сеанс завершён.']
            }
        ])
    actual_prompts, actual_outputs = mock_app_input_and_print_methods(app, user_inputs)

    app.start_dialog_with_user()

    assert actual_outputs == expected_outputs
    assert actual_prompts == expeted_prompts
