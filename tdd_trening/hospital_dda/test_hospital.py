import pytest

from tdd_trening.hospital_dda.exceptions import MinStatusCannotDownError
from tdd_trening.hospital_dda.hospital import Hospital


def test_get_patient_status():
    hospital = Hospital([2, 1, 3])
    assert hospital.get_patient_status_by_id(2) == 'Болен'


def test_patient_status_up():
    hospital = Hospital([1, 1, 1])
    hospital.patient_status_up(2)
    assert hospital._patients_db == [1, 2, 1]


def test_patient_status_down():
    hospital = Hospital([1, 1, 1])
    hospital.patient_status_down(2)
    assert hospital._patients_db == [1, 0, 1]


def test_min_status_cannot_down_error():
    hospital = Hospital([1, 0, 1])
    with pytest.raises(MinStatusCannotDownError) as err:
        hospital.patient_status_down(2)
    assert hospital._patients_db == [1, 0, 1]


def test_discharge_patient():
    hospital = Hospital([1, 3, 1])
    hospital.discharge_patient(2)
    assert hospital._patients_db == [1, 1]


def test_get_statistics():
    hospital = Hospital([2, 1, 1, 1, 2])
    assert hospital.get_statistics() == {"Болен": 3, "Слегка болен": 2}
