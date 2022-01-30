from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.exceptions import IdNotIntegerError, MinStatusCannotDownError
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal
from tdd_trening.hospital_dda_01.exceptions import PatientNotExistsError


def raise_id_not_integer_error():
    raise IdNotIntegerError('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')


def raise_patient_not_exists_error():
    raise PatientNotExistsError('Ошибка. В больнице нет пациента с таким ID')


def raise_min_status_cannot_down_error():
    raise MinStatusCannotDownError('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')


def test_cmd_stop():
    app = Application()
    result_message = app._cmd_stop()
    assert result_message == 'Сеанс завершён.'


def test_cmd_get_status():
    app = Application(hospital=Hospital([1, 1, 2]))
    app._get_patient_id_from_input_stream = lambda: 3
    result_message = app._cmd_get_status()
    assert result_message == 'Статус пациента: "Слегка болен"'


def test_cmd_get_status_when_patient_id_not_integer():
    app = Application()
    app._get_patient_id_from_input_stream = lambda: raise_id_not_integer_error()
    result_message = app._cmd_get_status()
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_cmd_get_status_when_patient_not_exists():
    app = Application(hospital=Hospital([1]))
    app._get_patient_id_from_input_stream = lambda: 2
    result_message = app._cmd_get_status()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_cmd_status_up():
    app = Application(hospital=Hospital([1, 1, 1, 2]))
    app._get_patient_id_from_input_stream = lambda: 4
    result_message = app._cmd_status_up()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1, 3])
    assert result_message == 'Новый статус пациента: "Готов к выписке"'


def test_cmd_status_up_when_patient_id_not_integer_error():
    app = Application(hospital=Hospital([1, 1]))
    app._get_patient_id_from_input_stream = lambda: raise_id_not_integer_error()
    result_message = app._cmd_status_up()
    assert_lists_equal(app._hospital._patients_db, [1, 1])
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_cmd_status_up_when_patient_not_exists():
    app = Application(hospital=Hospital([1]))
    app._get_patient_id_from_input_stream = lambda: 2
    result_message = app._cmd_status_up()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_cmd_status_up_when_patient_discharge():
    app = Application(hospital=Hospital([1, 1, 1, 3]))
    app._get_patient_id_from_input_stream = lambda: 4
    app._get_patient_discharge_confirmation_from_input_stream = lambda: True
    result_message = app._cmd_status_up()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1])
    assert result_message == 'Пациент выписан из больницы'


def test_cmd_status_up_when_status_not_changed():
    app = Application(hospital=Hospital([1, 1, 1, 3]))
    app._get_patient_id_from_input_stream = lambda: 4
    app._get_patient_discharge_confirmation_from_input_stream = lambda: False
    result_message = app._cmd_status_up()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1, 3])
    assert result_message == 'Пациент остался в статусе "Готов к выписке"'


def test_cmd_status_down():
    app = Application(hospital=Hospital([1, 1, 1, 3]))
    app._get_patient_id_from_input_stream = lambda: 4
    result_message = app._cmd_status_down()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1, 2])
    assert result_message == 'Новый статус пациента: "Слегка болен"'


def test_cmd_status_down_when_patient_not_exists():
    app = Application(hospital=Hospital([1]))
    app._get_patient_id_from_input_stream = lambda: 2
    result_message = app._cmd_status_down()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_cmd_status_down_when_patient_id_not_integer_error():
    app = Application(hospital=Hospital([1, 1]))
    app._get_patient_id_from_input_stream = lambda: raise_id_not_integer_error()
    result_message = app._cmd_status_down()
    assert_lists_equal(app._hospital._patients_db, [1, 1])
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_cmd_status_down_when_min_status_cannot_down_error():
    app = Application(hospital=Hospital([1, 0]))
    app._get_patient_id_from_input_stream = lambda: 2
    app._hospital.patient_status_down = lambda x: raise_min_status_cannot_down_error()
    result_message = app._cmd_status_down()
    assert_lists_equal(app._hospital._patients_db, [1, 0])
    assert result_message == 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'


def test_cmd_calculate_statistics():
    app = Application(hospital=Hospital([1, 3, 1, 0, 1, 3]))
    expected_result_messages = 'Статистика по статусам:\n' \
                               ' - в статусе "Тяжело болен": 1 чел.\n' \
                               ' - в статусе "Болен": 3 чел.\n' \
                               ' - в статусе "Готов к выписке": 2 чел.'
    result_message = app._cmd_calculate_statistics()
    assert result_message == expected_result_messages
