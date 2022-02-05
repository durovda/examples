from tdd_trening.hospital_dda.exceptions import PatientIdNotIntegerError, PatientNotExistsError, \
    MinStatusCannotDownError


class Commands:
    def __init__(self, hospital=None, dialog_with_user=None):
        self._hospital = hospital
        self._dialog_with_user = dialog_with_user

    @staticmethod
    def stop():
        return 'Сеанс завершён.'

    def get_status(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            patient_status = self._hospital.get_patient_status_by_id(patient_id)
            return f'Статус пациента: "{patient_status}"'
        except (PatientIdNotIntegerError, PatientNotExistsError) as err:
            return str(err)

    def status_up(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            if self._hospital.cannot_status_up_for_this_patient(patient_id):
                discharge_confirmation = self._dialog_with_user.request_patient_discharge_confirmation()
                if discharge_confirmation:
                    self._hospital.discharge_patient(patient_id)
                    return 'Пациент выписан из больницы'
                else:
                    return 'Пациент остался в статусе "Готов к выписке"'
            else:
                self._hospital.patient_status_up(patient_id)
                new_status = self._hospital.get_patient_status_by_id(patient_id)
                return f'Новый статус пациента: "{new_status}"'
        except (PatientIdNotIntegerError, PatientNotExistsError) as err:
            return str(err)

    def status_down(self):
        try:
            patient_id = self._dialog_with_user.request_patient_id()
            self._hospital.patient_status_down(patient_id)
            new_status = self._hospital.get_patient_status_by_id(patient_id)
            result_message = f'Новый статус пациента: "{new_status}"'
            return result_message
        except (PatientIdNotIntegerError, PatientNotExistsError, MinStatusCannotDownError) as err:
            return str(err)

    def calculate_statistics(self):
        result_message = 'Статистика по статусам:'
        statistics = self._hospital.get_statistics()
        for status in statistics:
            result_message += f'\n - в статусе "{status}": {statistics[status]} чел.'
        return result_message
