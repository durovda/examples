import pytest

from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream, InputMessages, OutputMessages


def test_input_messages():
    input_messages = InputMessages()
    input_messages.add('Question_01: ', 'answer_01')
    input_messages.add('Question_02: ', 'answer_02')

    assert input_messages.get() == ('Question_01: ', 'answer_01')
    assert input_messages.get() == ('Question_02: ', 'answer_02')
    assert len(input_messages._messages) == 2


def test_mock_input_stream():
    input_stream = MockInputStream()
    input_stream.add_expected_answer('Введите команду: ', 'узнать статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '7')

    assert input_stream.input('Введите команду: ') == 'узнать статус пациента'
    assert input_stream.input('Введите ID пациента: ') == '7'


def test_invalid_question():
    input_stream = MockInputStream()
    input_stream.add_expected_answer('Question: ', 'answer')

    with pytest.raises(AssertionError) as err:
        answer = input_stream.input('Invalid question: ')


def test_output_messages():
    output_messages = OutputMessages()
    output_messages.add('Первое сообщение')
    output_messages.add('Второе сообщение')

    assert output_messages.get() == 'Первое сообщение'
    assert output_messages.get() == 'Второе сообщение'
    assert len(output_messages._messages) == 2


def test_mock_output_stream():
    output_stream = MockOutputStream()
    output_stream.add_expected_message('Статус пациента: "Болен"')
    output_stream.add_expected_message('Новый статус пациента: "Слегка болен"')

    output_stream.print('Статус пациента: "Болен"')
    output_stream.print('Новый статус пациента: "Слегка болен"')


def test_invalid_output_message():
    output_stream = MockOutputStream()
    output_stream.add_expected_message('Статус пациента: "Болен"')

    with pytest.raises(AssertionError) as err:
        output_stream.print('Статус пациента: "Тяжело болен"')
