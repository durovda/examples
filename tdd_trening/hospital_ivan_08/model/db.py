class NonExistentPatientIdException(Exception):
    def __init__(self, message):
        self.message = message


class MaxStatusExceed(Exception):
    def __init__(self, message):
        self.message = message


class MinStatusExceed(Exception):
    def __init__(self, message):
        self.message = message


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

    def get_patients_count_by_status(self, status: int):
        """ Получить число пациентов с определенным статусом """
        return len(list(filter(
            lambda patient_stat: patient_stat == status, self.db)))

    def get_total_patients_count(self):
        """ Получить общее число пациентов """
        return len(self.db)

    def get_patient_status_by_index(self, patient_index: int):
        """ Получить статус пациента по индекс """
        if patient_index < len(self.db):
            return self.db[patient_index]
        else:
            raise NonExistentPatientIdException(
                f'Пациент с индексом {patient_index + 1} не найден')

    def update_patient_status(self, patient_index: int, new_status: int):
        """ Записать новый статус пациента """
        self.db[patient_index] = new_status

    def delete_patient(self, patient_index: int):
        """ Удалить пациента """
        self.db.pop(patient_index)
