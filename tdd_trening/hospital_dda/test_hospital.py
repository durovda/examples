import pytest

from tdd_trening.hospital_dda.exceptions import MinStatusCannotDownError
from tdd_trening.hospital_dda.hospital import Hospital
from tdd_trening.hospital_dda_01.exceptions import PatientNotExistsError


def test_get_patient_status():
    hospital = Hospital([2, 1, 3])
    assert hospital.get_patient_status_by_id(2) == 'Болен'


def test_get_patient_status_when_patient_not_exists():
    hospital = Hospital([1])
    with pytest.raises(PatientNotExistsError) as err:
        hospital.get_patient_status_by_id(2)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_patient_status_up():
    hospital = Hospital([1, 1, 1])
    hospital.patient_status_up(2)
    assert hospital._patients_db == [1, 2, 1]


def test_patient_status_up_when_patient_not_exists():
    hospital = Hospital([1])
    with pytest.raises(PatientNotExistsError) as err:
        hospital.patient_status_up(2)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_patient_status_down():
    hospital = Hospital([1, 1, 1])
    hospital.patient_status_down(2)
    assert hospital._patients_db == [1, 0, 1]


def test_patient_status_down_when_patient_not_exists():
    hospital = Hospital([1])
    with pytest.raises(PatientNotExistsError) as err:
        hospital.patient_status_down(2)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_min_status_cannot_down_error():
    hospital = Hospital([1, 0, 1])
    with pytest.raises(MinStatusCannotDownError) as err:
        hospital.patient_status_down(2)
    assert hospital._patients_db == [1, 0, 1]


def test_discharge_patient():
    hospital = Hospital([1, 3, 1])
    hospital.discharge_patient(2)
    assert hospital._patients_db == [1, 1]


def test_discharge_patient_when_patient_not_exists():
    hospital = Hospital([3])
    with pytest.raises(PatientNotExistsError) as err:
        hospital.discharge_patient(2)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_get_statistics():
    hospital = Hospital([2, 1, 1, 1, 2])
    assert hospital.get_statistics() == {"Болен": 3, "Слегка болен": 2}


def test_patient_exists():
    hospital = Hospital([1])
    assert not hospital.patient_exists(2)
