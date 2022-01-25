from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal


def test_full_positive_case():
    hospital = Hospital([1, 1, 0, 3, 1])
    input_messages = []
    expected_output_messages = []
    input_messages.append('узнать статус пациента')
    input_messages.append('1')
    expected_output_messages.append('Статус пациента: "Болен"')
    input_messages.append('повысить статус пациента')
    input_messages.append('1')
    expected_output_messages.append('Новый статус пациента: "Слегка болен"')
    input_messages.append('повысить статус пациента')
    input_messages.append('4')
    input_messages.append('да')
    expected_output_messages.append('Пациент выписан из больницы')
    input_messages.append('понизить статус пациента')
    input_messages.append('2')
    expected_output_messages.append('Новый статус пациента: "Тяжело болен"')
    # todo: Добавить функционал для ниже закомментированной части теста
    # input_messages.append('понизить статус пациента')
    # input_messages.append('3')
    # expected_output_messages.append('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')
    input_messages.append('рассчитать статистику')
    expected_output_messages.append('Статистика по статусам:' +
                                    '\n - в статусе "Тяжело болен": 2 чел.' +
                                    '\n - в статусе "Болен": 1 чел.' +
                                    '\n - в статусе "Слегка болен": 1 чел.')
    input_messages.append('стоп')
    expected_output_messages.append('Сеанс завершён.')
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      input_stream=MockInputStream(input_messages),
                      output_stream=output_stream)

    app.main()

    assert app._hospital._patients_db == [2, 0, 0, 1]
    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_patient_id_is_not_integer():
    hospital = Hospital([1, 1])
    input_messages = []
    expected_output_messages = []
    input_messages.append('узнать статус пациента')
    input_messages.append('два')
    expected_output_messages.append('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')
    input_messages.append('стоп')
    expected_output_messages.append('Сеанс завершён.')
    output_stream = MockOutputStream()
    app = Application(hospital=hospital,
                      input_stream=MockInputStream(input_messages),
                      output_stream=output_stream)

    app.main()

    assert_lists_equal(output_stream.messages, expected_output_messages)


def test_unknown_command():
    input_messages = []
    expected_output_messages = []
    input_messages.append('сделай что-нибудь...')
    expected_output_messages.append('Неизвестная команда! Попробуйте ещё раз')
    input_messages.append('стоп')
    expected_output_messages.append('Сеанс завершён.')
    output_stream = MockOutputStream()
    app = Application(input_stream=MockInputStream(input_messages),
                      output_stream=output_stream)

    app.main()

    assert_lists_equal(output_stream.messages, expected_output_messages)