import xml.etree.ElementTree as ET

from xml_example.tc import TestCase, Step


def test_one():
    tree = ET.parse('test_cases_jira.xml')
    root = tree.getroot()
    print()
    folders = root.find(r'.//folders')
    print(folders.tag)
    for folder in folders.iter('folder'):
        print(folder.get('fullPath'))
    test_cases = root.findall(r'.//testCase')
    test_case_1 = test_cases[0]
    print(type(test_case_1))
    print(test_case_1.find('folder').text)


def test_parse_one_test_case():
    tree = ET.parse('test_cases_jira.xml')
    root = tree.getroot()
    print()

    test_cases = root.findall(r'.//testCase')
    case = test_cases[0]
    print('folder:', case.find('folder').text)
    print('\tname:', case.find('name').text)
    print('\tobjective:', case.find('objective').text)

    steps = case.findall(r'.//step')
    print('\tsteps:')
    for step in steps:
        step_name = step.find('description').text
        step_name.replace('', '\n')
        print('\t\tstep:', step_name)
        print('\t\t\t', step.find('expectedResult').text)
        print()


def test_parse_and_print_cases_without_steps():
    tree = ET.parse('test_cases_jira.xml')
    root = tree.getroot()

    test_cases = root.findall(r'.//testCase')
    tc_list = []
    for case in test_cases:
        item = case.find('objective')
        if item is None:
            objective_raw = None
        else:
            objective_raw = item.text
        item = case.find('precondition')
        if item is None:
            precondition_raw = None
        else:
            precondition_raw = item.text
        tc = TestCase(name_raw=case.find('name').text,
                      folder_raw=case.find('folder').text,
                      objective_raw=objective_raw,
                      precondition_raw=precondition_raw)
        steps = case.findall(r'.//step')
        for step in steps:
            index = step.get('index')
            item = step.find('description')
            if item is None:
                description = None
            else:
                description = item.text
            item = step.find('expectedResult')
            if item is None:
                expected_result = None
            else:
                expected_result = item.text
            tc.add_step(
                Step(index=index, description_raw=description, expected_result_raw=expected_result)
            )
        tc_list.append(tc)

    print()
    print()

    for tc in tc_list:
        lines = tc.as_lines()
        print('\n'.join(lines))
        print()
