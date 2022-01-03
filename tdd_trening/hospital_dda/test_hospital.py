from tdd_trening.hospital_dda.hospital import Hospital


def test_get_patient_status():
    hospital = Hospital([2, 1, 3])
    assert hospital.get_patient_status_by_id(2) == 'Болен'


def test_patient_status_up():
    hospital = Hospital([1, 1, 1])
    hospital.patient_status_up(2)
    assert hospital._patients_db == [1, 2, 1]


def test_get_statistics():
    hospital = Hospital([2, 1, 1, 1, 2])
    assert hospital.get_statistics() == {"Болен": 3, "Слегка болен": 2}
