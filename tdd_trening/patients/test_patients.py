from tdd_trening.patients.patients import PatientsRepository


def test_create_patients_repository():
    patients_db = [1, 2, 3]
    patients = PatientsRepository(patients_db)
    assert patients._patients_db == [1, 2, 3]
