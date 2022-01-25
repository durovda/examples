from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.mocks import MockInputStream, MockOutputStream


def test_full_positive_case():
    hospital = Hospital([1, 1, 0, 3, 1])
    input_stream = MockInputStream()
    output_stream = MockOutputStream()
    input_stream.add_expected_answer('Введите команду: ', 'узнать статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '1')
    output_stream.add_expected_message('Статус пациента: "Болен"')
    input_stream.add_expected_answer('Введите команду: ', 'повысить статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '1')
    output_stream.add_expected_message('Новый статус пациента: "Слегка болен"')
    input_stream.add_expected_answer('Введите команду: ', 'повысить статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '4')
    input_stream.add_expected_answer('Желаете этого клиента выписать? (да/нет) ', 'да')
    output_stream.add_expected_message('Пациент выписан из больницы')
    input_stream.add_expected_answer('Введите команду: ', 'понизить статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '2')
    output_stream.add_expected_message('Новый статус пациента: "Тяжело болен"')
    input_stream.add_expected_answer('Введите команду: ', 'понизить статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', '3')
    output_stream.add_expected_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')
    input_stream.add_expected_answer('Введите команду: ', 'рассчитать статистику')
    output_stream.add_expected_message('Статистика по статусам:' +
                                       '\n - в статусе "Тяжело болен": 2 чел.' +
                                       '\n - в статусе "Болен": 1 чел.' +
                                       '\n - в статусе "Слегка болен": 1 чел.')
    input_stream.add_expected_answer('Введите команду: ', 'стоп')
    output_stream.add_expected_message('Сеанс завершён.')
    app = Application(hospital=hospital,
                      input_stream=input_stream,
                      output_stream=output_stream)

    app.main()

    assert app._hospital._patients_db == [2, 0, 0, 1]


def test_patient_id_is_not_integer():
    hospital = Hospital([1, 1])
    input_stream = MockInputStream()
    output_stream = MockOutputStream()
    input_stream.add_expected_answer('Введите команду: ', 'узнать статус пациента')
    input_stream.add_expected_answer('Введите ID пациента: ', 'два')
    output_stream.add_expected_message('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')
    input_stream.add_expected_answer('Введите команду: ', 'стоп')
    output_stream.add_expected_message('Сеанс завершён.')
    app = Application(hospital=hospital,
                      input_stream=input_stream,
                      output_stream=output_stream)

    app.main()


def test_unknown_command():
    input_stream = MockInputStream()
    output_stream = MockOutputStream()
    input_stream.add_expected_answer('Введите команду: ', 'сделай что-нибудь...')
    output_stream.add_expected_message('Неизвестная команда! Попробуйте ещё раз')
    input_stream.add_expected_answer('Введите команду: ', 'стоп')
    output_stream.add_expected_message('Сеанс завершён.')
    app = Application(input_stream=input_stream,
                      output_stream=output_stream)

    app.main()
