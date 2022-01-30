import pytest
from app.db import HospitalListDB


@pytest.fixture(scope="function")
def db_for_db_tests():
    return HospitalListDB([0,
                           1, 1, 1, 1,
                           2, 2, 2,
                           3, 3,
                           ])


def test_get_total_patients_count(db_for_db_tests):
    assert 10 == db_for_db_tests.get_total_patients_count()


def test_get_patients_count_by_status(db_for_db_tests):
    assert 3 == db_for_db_tests.get_patients_count_by_status(2)


def test_update_patient_status(db_for_db_tests):
    new_status = 7
    patient_index = 1
    db_for_db_tests.update_patient_status(patient_index, new_status)
    assert db_for_db_tests.db[patient_index] == new_status


def test_get_patient_by_index(db_for_db_tests):
    assert 1 == db_for_db_tests.get_patient_status_by_index(1)


def test_delete_patient(db_for_db_tests):
    len_before = len(db_for_db_tests.db)
    patient_index = 9
    db_for_db_tests.delete_patient(patient_index)
    len_after = len(db_for_db_tests.db)
    assert not db_for_db_tests.get_patient_status_by_index(patient_index)
    assert len_before - 1 == len_after
