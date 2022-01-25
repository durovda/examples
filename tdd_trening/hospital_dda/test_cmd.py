from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal


def test_cmd_stop():
    app = Application()
    result_message = app._cmd_stop()
    assert result_message == 'Сеанс завершён.'


def test_cmd_get_status():
    app = Application(hospital=Hospital([1, 1, 2]))
    app._get_patient_id_from_input_stream = lambda: 3
    result_message = app._cmd_get_status()
    assert result_message == 'Статус пациента: "Слегка болен"'


def test_cmd_status_up():
    app = Application(hospital=Hospital([1, 1, 1, 2]))
    app._get_patient_id_from_input_stream = lambda: 4
    result_message = app._cmd_status_up()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1, 3])
    assert result_message == 'Новый статус пациента: "Готов к выписке"'


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


def test_cmd_calculate_statistics():
    app = Application(hospital=Hospital([1, 3, 1, 0, 1, 3]))
    expected_result_messages = 'Статистика по статусам:\n' \
                               ' - в статусе "Тяжело болен": 1 чел.\n' \
                               ' - в статусе "Болен": 3 чел.\n' \
                               ' - в статусе "Готов к выписке": 2 чел.'
    result_message = app._cmd_calculate_statistics()
    assert result_message == expected_result_messages


def test_cmd_status_down():
    app = Application(hospital=Hospital([1, 1, 1, 3]))
    app._get_patient_id_from_input_stream = lambda: 4
    result_message = app._cmd_status_down()
    assert_lists_equal(app._hospital._patients_db, [1, 1, 1, 2])
    assert result_message == 'Новый статус пациента: "Слегка болен"'
