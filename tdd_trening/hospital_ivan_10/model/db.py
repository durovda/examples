class NonExistentPatientIdError(Exception):
    pass


class MaxStatusExceedError(Exception):
    pass


class MinStatusExceedError(Exception):
    pass


class HospitalListDB:
    def __init__(self, db, statuses=None):
        self.db = db
        if statuses is None:
            statuses = {
                0: 'Тяжело болен',
                1: 'Болен',
                2: 'Слегка болен',
                3: 'Готов к выписке',
            }
        self.statuses = statuses
        self.min_status = min(self.statuses.keys())
        self.max_status = max(self.statuses.keys())

    def get_total_patients_count(self):
        """ Получить общее число пациентов """
        return len(self.db)

    def get_patient_status_by_index(self, patient_index: int):
        """ Получить статус пациента по индексу """
        if patient_index < len(self.db):
            return self.db[patient_index]
        else:
            raise NonExistentPatientIdError(
                f'Пациент с индексом {patient_index + 1} не найден')

    def update_patient_status(self, patient_index: int, new_status: int):
        """ Записать новый статус пациента """
        if new_status < self.min_status:
            raise MinStatusExceedError(
                'Ошибка. Запрашиваемый статус ниже минимального!')
        elif new_status > self.max_status:
            raise MaxStatusExceedError(
                'Ошибка. Запрашиваемый статус выше минимального!')
        else:
            self.db[patient_index] = new_status

    def delete_patient(self, patient_index: int):
        """ Удалить пациента """
        if patient_index < len(self.db):
            self.db.pop(patient_index)
        else:
            raise NonExistentPatientIdError(
                f'Пациент с индексом {patient_index + 1} не найден')

    def calc_patients_stat_by_groups(self):
        """ Рассчитываем статистику по группам """
        stat_with_zeros = {
            k: self._get_patients_count_by_status(k)
            for k in self.statuses.keys()
        }
        return {k: v for k, v in stat_with_zeros.items() if v != 0}

    def raise_patient_status(self, patient_index, confirmation_request_method):
        user_status = self.get_patient_status_by_index(patient_index)
        new_user_status = user_status + 1
        if new_user_status < len(self.statuses):
            self.update_patient_status(patient_index, new_user_status)
            return f'Новый статус пациента: "{self.statuses[new_user_status]}"'
        else:
            if not confirmation_request_method():
                return f'Пациент остался в статусе "{self.statuses[new_user_status - 1]}"'
            else:
                self.delete_patient(patient_index)
                return f'Пациент с ID={patient_index + 1} выписан.'

    def reduce_patient_status(self, patient_index):
        user_status = self.get_patient_status_by_index(patient_index)
        new_user_status = user_status - 1
        if new_user_status < self.min_status:
            return (
                'У этого пациента самый низкий статус '
                f'"{self.statuses[self.min_status]}".\n'
                'Статус пациента не изменился, т.к. в нашей больнице '
                'пациенты не умирают!\n'
            )
        else:
            self.update_patient_status(patient_index, new_user_status)
            return f'Новый статус пациента: "{self.statuses[new_user_status]}"'

    def _get_patients_count_by_status(self, status: int):
        """ Получить число пациентов с определенным статусом """
        return len(list(filter(
            lambda patient_stat: patient_stat == status, self.db)))
