

class Hospital:
    def __init__(self, patients_db):
        self._patients_db = patients_db
        self._statuses_db = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен",
                             3: "Близок к выздоровлению", 4: "Готов к выписке"}

    def get_patient_status_by_id(self, patient_id):
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        return self._statuses_db[status_code]

    def patient_status_up(self, patient_id):
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code + 1

    def patient_status_down(self, patient_id):
        patient_index = patient_id - 1
        status_code = self._patients_db[patient_index]
        self._patients_db[patient_index] = status_code - 1

    def get_statistics(self):
        statistics = {}
        for status_code in self._statuses_db:
            count = 0
            for patient_status_code in self._patients_db:
                if patient_status_code == status_code:
                    count += 1
            if count > 0:
                statistics[self._statuses_db[status_code]] = count
        return statistics
