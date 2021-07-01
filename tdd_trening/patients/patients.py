class PatientsRepository():
    def __init__(self, patients_db):
        self._patients_db = patients_db

    def patient_status_up(self, patient_id):
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code + 1

    def patient_status_down(self, patient_id):
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code - 1

    def get_status_by_patient_id(self, patient_id):
        patient_index = patient_id - 1
        status_db = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен",
                     3: "Близок к выздоровлению", 4: "Выписать через пару дней", 5: "Выписан"}
        status_code = self._patients_db[patient_index]
        return status_db[status_code]
