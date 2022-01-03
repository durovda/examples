from xml_example.tc import Step


def test_step_description():
    step = Step(description_raw='description_1 <br/> description_2 <br /> description_3')
    expected_lines = [
        'description_1',
        'description_2',
        'description_3'
    ]
    assert step.description == expected_lines


def test_step_expected_result():
    step = Step(expected_result_raw='expected_result_1 <br/> expected_result_2 <br /> expected_result_3')
    expected_lines = [
        'expected_result_1',
        'expected_result_2',
        'expected_result_3'
    ]
    assert step.expected_result == expected_lines


def test_get_step_as_lines():
    step = Step(index='1',
                description_raw='description_1 <br/> description_2',
                expected_result_raw='expected_result_1 <br/> expected_result_2')
    expected_lines = [
        '\tstep 1:',
        '\t\tdescription_1',
        '\t\tdescription_2',
        '\t\texpected_result:',
        '\t\t\texpected_result_1',
        '\t\t\texpected_result_2'
    ]
    assert step.as_lines(indent=1) == expected_lines


def test_get_step_as_lines_2():
    tc = Step(index='1',
              description_raw='description_1 <br/> description_2')
    expected_lines = [
        '\tstep 1:',
        '\t\tdescription_1',
        '\t\tdescription_2'
    ]
    assert tc.as_lines(indent=1) == expected_lines
