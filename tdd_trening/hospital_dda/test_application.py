import pytest

from tdd_trening.hospital_dda.application import Application, Command
from tdd_trening.hospital_dda.exceptions import IdNotIntegerError
from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal

fixture_for_parser = [('стоп', Command.STOP),
                      ('Стоп', Command.STOP),
                      ('stop', Command.STOP),
                      ('STOP', Command.STOP),
                      ('остановите программу!', Command.UNKNOWN),
                      ('узнать статус пациента', Command.GET_STATUS),
                      ('повысить статус пациента', Command.STATUS_UP),
                      ('понизить статус пациента', Command.STATUS_DOWN),
                      ('рассчитать статистику', Command.CALCULATE_STATISTICS)
                      ]


@pytest.mark.parametrize('tpl', fixture_for_parser)
def test_parse_text_to_command(tpl):
    app = Application()
    assert app._parse_text_to_command(tpl[0]) == tpl[1]


def test_get_command_from_input_stream():
    app = Application(input_stream=MockInputStream(['стоп']))
    assert app._get_command_from_input_stream() == Command.STOP


def test_get_patient_id_from_input_stream():
    app = Application(input_stream=MockInputStream(['2']))
    assert app._get_patient_id_from_input_stream() == 2


def test_get_patient_discharge_confirmation_from_input_stream():
    input_messages = ['да']
    app = Application(input_stream=MockInputStream(input_messages))
    assert app._get_patient_discharge_confirmation_from_input_stream()


def test_get_patient_discharge_not_confirmation_from_input_stream():
    input_messages = ['нет']
    app = Application(input_stream=MockInputStream(input_messages))
    assert not app._get_patient_discharge_confirmation_from_input_stream()


def test_patient_id_is_not_integer():
    input_messages = ['два']
    app = Application(input_stream=MockInputStream(input_messages))
    with pytest.raises(IdNotIntegerError) as err:
        app._get_patient_id_from_input_stream()
    assert str(err.value) == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_send_message_to_output_stream():
    expected_output_messages = ['Сообщение, посылаемое в output_stream']
    output_stream = MockOutputStream()
    app = Application(output_stream=output_stream)
    app._send_message_to_output_stream('Сообщение, посылаемое в output_stream')
    assert_lists_equal(output_stream.messages, expected_output_messages)
