from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream


def test_mock_input_stream():
    input_stream = MockInputStream(['узнать статус пациента', '7'])

    message = input_stream.get_message('Для этого теста не важно, что здесь написано')
    assert message == 'узнать статус пациента'

    message = input_stream.get_message('Для этого теста не важно, что здесь написано')
    assert message == '7'


def test_mock_output_stream():
    output_stream = MockOutputStream()

    output_stream.send_message('Статус пациента: "Болен"')
    output_stream.send_message('Новый статус пациента: "Слегка болен"')

    assert output_stream.messages == ['Статус пациента: "Болен"', 'Новый статус пациента: "Слегка болен"']

