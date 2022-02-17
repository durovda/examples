import pytest

from tdd_trening.hospital_dda.mock_console import MockConsole


def test_input():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '7')

    assert console.input('Введите команду: ') == 'узнать статус пациента'
    assert console.input('Введите ID пациента: ') == '7'


def test_input_when_invalid_request():
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'для этого теста подходит любой ответ')

    with pytest.raises(AssertionError):
        console.input('Пожалуйста, введите команду: ')


def test_print():
    console = MockConsole()
    console.add_expected_output_message('Статус пациента: "Болен"')
    console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

    console.print('Статус пациента: "Болен"')
    console.print('Новый статус пациента: "Слегка болен"')


def test_print_when_invalid_output_message():
    console = MockConsole()
    console.add_expected_output_message('Статус пациента: "Болен"')

    with pytest.raises(AssertionError):
        console.print('Статус пациента: "Тяжело болен"')


def test_print_when_invalid_order_of_output_message():
    console = MockConsole()
    console.add_expected_output_message('Первое сообщение')
    console.add_expected_output_message('Второе сообщение')

    with pytest.raises(AssertionError):
        console.print('Второе сообщение')
