from tdd_trening.patients.patients import PatientsRepository


def test_create_patients_repository():
    patients_db = [1, 2, 3]
    patients = PatientsRepository(patients_db)
    assert patients._patients_db == [1, 2, 3]


def test_patient_status_up():
    patients = PatientsRepository([1, 1, 1])
    patients.patient_status_up(2)
    assert patients._patients_db == [1, 2, 1]


def test_patient_status_down():
    patients = PatientsRepository([1, 1, 1])
    patients.patient_status_down(2)
    assert patients._patients_db == [1, 0, 1]
