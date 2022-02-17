from unittest.mock import MagicMock

from tdd_trening.hospital_dda.commands import Commands
from tdd_trening.hospital_dda.exceptions import PatientIdNotIntegerError, PatientNotExistsError, \
    MinStatusCannotDownError


def make_commands():
    return Commands(hospital=MagicMock(), dialog_with_user=MagicMock())


def test_stop():
    cmd = make_commands()
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.stop()

    cmd._dialog_with_user.send_message.assert_called_with('Сеанс завершён.')


def test_get_status():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Слегка болен')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.get_patient_status_by_id.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Статус пациента: "Слегка болен"')


def test_get_status_when_patient_id_not_integer():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_get_status_when_patient_not_exists():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.get_patient_status_by_id = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.get_status()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.get_patient_status_by_id.assert_called_with(999)
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.cannot_status_up_for_this_patient = MagicMock(return_value=False)
    cmd._hospital.patient_status_up = MagicMock()
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Готов к выписке')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.cannot_status_up_for_this_patient.assert_called_with(77)
    cmd._hospital.patient_status_up.assert_called_with(77)
    cmd._hospital.get_patient_status_by_id.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Готов к выписке"')


def test_status_up_when_patient_id_not_integer():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_up_when_patient_not_exists():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.cannot_status_up_for_this_patient = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.cannot_status_up_for_this_patient.assert_called_with(999)
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up_when_patient_discharge():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.cannot_status_up_for_this_patient = MagicMock(return_value=True)
    cmd._dialog_with_user.request_patient_discharge_confirmation = MagicMock(return_value=True)
    cmd._hospital.discharge_patient = MagicMock()
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.cannot_status_up_for_this_patient.assert_called_with(77)
    cmd._dialog_with_user.request_patient_discharge_confirmation.assert_called_with()
    cmd._hospital.discharge_patient.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Пациент выписан из больницы')


def test_status_up_when_status_not_changed():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.cannot_status_up_for_this_patient = MagicMock(return_value=True)
    cmd._dialog_with_user.request_patient_discharge_confirmation = MagicMock(return_value=False)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_up()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.cannot_status_up_for_this_patient.assert_called_with(77)
    cmd._dialog_with_user.request_patient_discharge_confirmation.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')


def test_status_down():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.patient_status_down = MagicMock()
    cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Слегка болен')
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.patient_status_down.assert_called_with(77)
    cmd._hospital.get_patient_status_by_id.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')


def test_status_down_when_patient_id_not_integer():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
                                                          'ID пациента должно быть числом (целым, положительным)')


def test_status_down_when_patient_not_exists():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=999)
    cmd._hospital.patient_status_down = MagicMock(side_effect=PatientNotExistsError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.patient_status_down.assert_called_with(999)
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_down_when_min_status_cannot_down():
    cmd = make_commands()
    cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
    cmd._hospital.patient_status_down = MagicMock(side_effect=MinStatusCannotDownError)
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.status_down()

    cmd._dialog_with_user.request_patient_id.assert_called_with()
    cmd._hospital.patient_status_down.assert_called_with(77)
    cmd._dialog_with_user.send_message.assert_called_with('Ошибка. Нельзя понизить самый низкий статус '
                                                          '(наши пациенты не умирают)')


def test_calculate_statistics():
    cmd = make_commands()
    cmd._hospital.get_statistics = MagicMock(return_value={"Тяжело болен": 1, "Болен": 3, "Готов к выписке": 2})
    cmd._dialog_with_user.send_message = MagicMock()

    cmd.calculate_statistics()

    cmd._hospital.get_statistics.assert_called_with()
    cmd._dialog_with_user.send_message.assert_called_with('Статистика по статусам:\n'
                                                          ' - в статусе "Тяжело болен": 1 чел.\n'
                                                          ' - в статусе "Болен": 3 чел.\n'
                                                          ' - в статусе "Готов к выписке": 2 чел.')
