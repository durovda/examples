class HospitalListDB:
    def __init__(self, db):
        self.db = db

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
            return None

    def update_patient_status(self, patient_index: int, new_status: int):
        """ Записать новый статус пациента """
        self.db[patient_index] = new_status

    def delete_patient(self, patient_index: int):
        """ Удалить пациента """
        self.db.pop(patient_index)
