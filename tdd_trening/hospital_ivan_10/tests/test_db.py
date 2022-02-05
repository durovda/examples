import pytest
from model.db import HospitalListDB, NonExistentPatientIdError, MinStatusExceedError, MaxStatusExceedError


@pytest.fixture(scope="function")
def db_for_tests():
    return HospitalListDB([0,
                           1, 1, 1, 1,
                           2, 2, 2,
                           3, 3,
                           ])


def test_get_total_patients_count(db_for_tests):
    assert 10 == db_for_tests.get_total_patients_count()


def test_get_patients_count_by_status(db_for_tests):
    assert 3 == db_for_tests._get_patients_count_by_status(2)


def test_try_update_patient_status_below_minimum(db_for_tests):
    new_status = -1
    patient_index = 1
    with pytest.raises(MinStatusExceedError):
        db_for_tests.update_patient_status(patient_index, new_status)


def test_try_update_patient_status_above_maximum(db_for_tests):
    new_status = 4
    patient_index = 1
    with pytest.raises(MaxStatusExceedError):
        db_for_tests.update_patient_status(patient_index, new_status)


def test_update_patient_status(db_for_tests):
    new_status = 3
    patient_index = 1
    db_for_tests.update_patient_status(patient_index, new_status)
    assert db_for_tests.db[patient_index] == new_status


def test_get_patient_by_index(db_for_tests):
    assert 1 == db_for_tests.get_patient_status_by_index(1)


def test_delete_patient(db_for_tests):
    len_before = len(db_for_tests.db)
    patient_index = 9
    db_for_tests.delete_patient(patient_index)
    len_after = len(db_for_tests.db)
    with pytest.raises(NonExistentPatientIdError):
        db_for_tests.get_patient_status_by_index(patient_index)
    assert len_before - 1 == len_after


def test_delete_non_existing_patient(db_for_tests):
    len_before = len(db_for_tests.db)
    patient_index = 100
    with pytest.raises(NonExistentPatientIdError):
        db_for_tests.get_patient_status_by_index(patient_index)
    len_after = len(db_for_tests.db)
    assert len_before == len_after


def test_calc_statistics(db_for_tests):
    statistics = db_for_tests.calc_patients_stat_by_groups()
    assert statistics == {0: 1, 1: 4, 2: 3, 3: 2}
