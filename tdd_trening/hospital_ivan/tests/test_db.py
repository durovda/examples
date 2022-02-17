import pytest
from model.db import HospitalListDB, NonExistentPatientIdError, \
    MinStatusExceedError, MaxStatusExceedError


@pytest.fixture(scope="function")
def db_for_tests():
    return HospitalListDB([0,
                           1, 1, 1, 1,
                           2, 2, 2,
                           3, 3,
                           ])


def test_get_total_patients_count(db_for_tests):
    assert db_for_tests.get_total_patients_count() == 10


def test_get_patients_count_by_status(db_for_tests):
    assert db_for_tests._get_patients_count_by_status(2) == 3


def test_try_update_patient_status_below_minimum(db_for_tests):
    new_status = -1
    patient_index = 1
    with pytest.raises(MinStatusExceedError):
        db_for_tests._update_patient_status(patient_index, new_status)


def test_try_update_patient_status_above_maximum(db_for_tests):
    new_status = 4
    patient_index = 1
    with pytest.raises(MaxStatusExceedError):
        db_for_tests._update_patient_status(patient_index, new_status)


def test_update_patient_status(db_for_tests):
    new_status = 3
    patient_index = 1
    db_for_tests._update_patient_status(patient_index, new_status)
    assert db_for_tests.db[patient_index] == new_status


def test_get_patient_by_index(db_for_tests):
    assert db_for_tests.get_patient_status_by_index(1) == 1


def test_delete_patient(db_for_tests):
    len_before = len(db_for_tests.db)
    patient_index = 9
    db_for_tests.delete_patient(patient_index)
    len_after = len(db_for_tests.db)
    with pytest.raises(NonExistentPatientIdError):
        db_for_tests.get_patient_status_by_index(patient_index)
    assert len_before - 1 == len_after


def test_raise_patient_status(db_for_tests):
    db_for_tests.raise_patient_status(1)
    assert db_for_tests.db[1] == 2


def test_reduce_patient_status(db_for_tests):
    db_for_tests.reduce_patient_status(1)
    assert db_for_tests.db[1] == 0
    with pytest.raises(MinStatusExceedError):
        db_for_tests.reduce_patient_status(1)
    assert db_for_tests.db[1] == 0


def test_calc_statistics(db_for_tests):
    statistics = db_for_tests.calc_patients_stat_by_groups()
    assert statistics == {0: 1, 1: 4, 2: 3, 3: 2}
