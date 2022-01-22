from tdd_trening.hospital_dda.application import Application, Command
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal


def test_get_cmd_stop():
    app = Application(input_stream=MockInputStream(['стоп']))
    assert app._get_command_from_input_stream() == Command.STOP


def test_get_cmd_get_status():
    app = Application(input_stream=MockInputStream(['узнать статус пациента']))
    assert app._get_command_from_input_stream() == Command.GET_STATUS


def test_get_cmd_status_up():
    app = Application(input_stream=MockInputStream(['повысить статус пациента']))
    assert app._get_command_from_input_stream() == Command.STATUS_UP


def test_get_cmd_status_down():
    app = Application(input_stream=MockInputStream(['понизить статус пациента']))
    assert app._get_command_from_input_stream() == Command.STATUS_DOWN


def test_get_cmd_calculate_statistics():
    app = Application(input_stream=MockInputStream(['рассчитать статистику']))
    assert app._get_command_from_input_stream() == Command.CALCULATE_STATISTICS


def test_get_patient_id_from_input_stream():
    app = Application(input_stream=MockInputStream(['2']))
    assert app._get_patient_id_from_input_stream() == 2


def test_cmd_stop():
    hospital = Hospital([1, 1])
    expected_output_messages = ['Сеанс завершён.']
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      output_stream=output_stream)

    app._cmd_stop()

    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_cmd_get_status():
    hospital = Hospital([1, 1, 2])
    expected_output_messages = ['Статус пациента: "Слегка болен"']
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      output_stream=output_stream)

    app._cmd_get_status(patient_id=3)

    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_cmd_status_up():
    hospital = Hospital([1, 1, 2])
    expected_output_messages = ['Новый статус пациента: "Готов к выписке"']
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      output_stream=output_stream)

    app._cmd_status_up(patient_id=3)

    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_cmd_calculate_statistics():
    hospital = Hospital([1, 1])
    expected_output_messages = ['Статистика по статусам:' +
                                '\n - в статусе "Болен": 2 чел.']
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      output_stream=output_stream)

    app._cmd_calculate_statistics()

    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_cmd_status_down():
    hospital = Hospital([1, 3, 1])
    expected_output_messages = ['Новый статус пациента: "Слегка болен"']
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      output_stream=output_stream)

    app._cmd_status_down(patient_id=2)

    assert_lists_equal(output_stream.messages, expected_output_messages)
