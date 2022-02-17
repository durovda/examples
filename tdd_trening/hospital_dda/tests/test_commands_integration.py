from unittest.mock import MagicMock

from tdd_trening.hospital_dda.commands import Commands
from tdd_trening.hospital_dda.exceptions import PatientIdNotIntegerError, MinStatusCannotDownError, \
    PatientNotExistsError
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda.spesial_asserts import assert_lists_equal


def raise_id_not_integer_error():
    raise PatientIdNotIntegerError


def raise_patient_not_exists_error():
    raise PatientNotExistsError


def raise_min_status_cannot_down_error():
    raise MinStatusCannotDownError


class MockDialogWithUser:
    pass


def test_stop():
    cmd = Commands(dialog_with_user=MagicMock())
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.stop()

    cmd._dialog_with_user.send_message.assert_called_with('Сеанс завершён.')


def test_get_status():
    cmd = Commands(Hospital([1, 1, 2]), dialog_with_user=MagicMock())
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=3)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.send_message.assert_called_with('Статус пациента: "Слегка болен"')


def test_get_status_when_patient_id_not_integer():
    cmd = Commands(None, MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: raise_id_not_integer_error()
    result_message = cmd.get_status()
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_get_status_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 2
    result_message = cmd.get_status()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_status_up():
    cmd = Commands(Hospital([1, 1, 1, 2]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 4
    result_message = cmd.status_up()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 3])
    assert result_message == 'Новый статус пациента: "Готов к выписке"'


def test_status_up_when_patient_id_not_integer():
    cmd = Commands(Hospital([1, 1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: raise_id_not_integer_error()
    result_message = cmd.status_up()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1])
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_status_up_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 2
    result_message = cmd.status_up()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_status_up_when_patient_discharge():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 4
    cmd._dialog_with_user.request_patient_discharge_confirmation = lambda: True
    result_message = cmd.status_up()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1])
    assert result_message == 'Пациент выписан из больницы'


def test_status_up_when_status_not_changed():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 4
    cmd._dialog_with_user.request_patient_discharge_confirmation = lambda: False
    result_message = cmd.status_up()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 3])
    assert result_message == 'Пациент остался в статусе "Готов к выписке"'


def test_status_down():
    cmd = Commands(Hospital([1, 1, 1, 3]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 4
    result_message = cmd.status_down()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1, 1, 2])
    assert result_message == 'Новый статус пациента: "Слегка болен"'


def test_status_down_when_patient_not_exists():
    cmd = Commands(Hospital([1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 2
    result_message = cmd.status_down()
    assert result_message == 'Ошибка. В больнице нет пациента с таким ID'


def test_status_down_when_patient_id_not_integer():
    cmd = Commands(Hospital([1, 1]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: raise_id_not_integer_error()
    result_message = cmd.status_down()
    assert_lists_equal(cmd._hospital._patients_db, [1, 1])
    assert result_message == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_status_down_when_min_status_cannot_down():
    cmd = Commands(Hospital([1, 0]), MockDialogWithUser())
    cmd._dialog_with_user.request_patient_id = lambda: 2
    cmd._hospital.patient_status_down = lambda x: raise_min_status_cannot_down_error()
    result_message = cmd.status_down()
    assert_lists_equal(cmd._hospital._patients_db, [1, 0])
    assert result_message == 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'


def test_calculate_statistics():
    cmd = Commands(Hospital([1, 3, 1, 0, 1, 3]))
    expected_result_messages = 'Статистика по статусам:\n' \
                               ' - в статусе "Тяжело болен": 1 чел.\n' \
                               ' - в статусе "Болен": 3 чел.\n' \
                               ' - в статусе "Готов к выписке": 2 чел.'
    result_message = cmd.calculate_statistics()
    assert result_message == expected_result_messages


def test_discharge_patient():
    pass
