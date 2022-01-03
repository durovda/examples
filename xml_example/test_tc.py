from xml_example.tc import TestCase, Step


def test_tc_name():
    tc = TestCase(name_raw='Name **1**')
    assert tc.name == 'Name **1**'


def test_tc_folder():
    tc = TestCase(folder_raw='Запись звука/Ротация/Под-под-раздел')
    assert tc.folder == ['Запись звука', 'Ротация', 'Под-под-раздел']


def test_tc_precondition():
    tc = TestCase(precondition_raw='precondition_1 <br/> precondition_2 <br /> precondition_3')
    expected_lines = [
        'precondition_1',
        'precondition_2',
        'precondition_3'
    ]
    assert tc.precondition == expected_lines


def test_tc_precondition_2():
    tc = TestCase(precondition_raw='precondition_1 <br/> <br/> precondition_2')
    expected_lines = [
        'precondition_1',
        'precondition_2'
    ]
    assert tc.precondition == expected_lines


def test_tc_objective():
    tc = TestCase(objective_raw='objective_1 <br/> objective_2 <br /> objective_3')
    expected_lines = [
        'objective_1',
        'objective_2',
        'objective_3'
    ]
    assert tc.objective == expected_lines


def test_tc_objective_2():
    tc = TestCase(objective_raw='objective_1 <br/> <br/> objective_2')
    expected_lines = [
        'objective_1',
        'objective_2'
    ]
    assert tc.objective == expected_lines


def test_get_tc_as_lines():
    tc = TestCase(name_raw='Name **1**',
                  folder_raw='Запись звука/Ротация',
                  objective_raw='objective_1 <br/> objective_2',
                  precondition_raw='precondition_1 <br/> precondition_2')
    step_1 = Step(index='1',
                  description_raw='description_1 <br/> description_2',
                  expected_result_raw='expected_result_1 <br/> expected_result_2')
    step_2 = Step(index='2',
                  description_raw='description_3 <br/> description_4',
                  expected_result_raw='expected_result_3 <br/> expected_result_4')
    tc.add_step(step_1)
    tc.add_step(step_2)
    expected_lines = [
        '\tЗапись звука --> Ротация',
        '\t\tName **1**',
        '\t\t\tobjective:',
        '\t\t\t\tobjective_1',
        '\t\t\t\tobjective_2',
        '\t\t\tprecondition:',
        '\t\t\t\tprecondition_1',
        '\t\t\t\tprecondition_2',
        '\t\t\tstep 1:',
        '\t\t\t\tdescription_1',
        '\t\t\t\tdescription_2',
        '\t\t\t\texpected_result:',
        '\t\t\t\t\texpected_result_1',
        '\t\t\t\t\texpected_result_2',
        '\t\t\tstep 2:',
        '\t\t\t\tdescription_3',
        '\t\t\t\tdescription_4',
        '\t\t\t\texpected_result:',
        '\t\t\t\t\texpected_result_3',
        '\t\t\t\t\texpected_result_4'
    ]
    assert tc.as_lines(indent=1) == expected_lines


def test_get_tc_as_lines_2():
    tc = TestCase(name_raw='Name **1**',
                  folder_raw='Запись звука/Ротация')
    expected_lines = [
        '\tЗапись звука --> Ротация',
        '\t\tName **1**'
    ]
    assert tc.as_lines(indent=1) == expected_lines
