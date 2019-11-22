from orgunit import Orgunit, Position, NodeType


def test_how_to_use_orgunit():
    # Создаем объект подразделения и используем его данные для:
    # - создания подразделения в inRights
    # - назначения на подразделение базовых ролей (если необходимо)
    org = Orgunit("Подразделение 1_2",
                  full_name="Подразделение ОДИН_ДВА",
                  manager="Офицер ИБ",
                  parent_chain_as_lines=["Компания", "Подразделение 1"],
                  basic_roles=["Роль_01", "Роль_02"])

    assert "Подразделение 1_2" == org.name
    assert "Подразделение ОДИН_ДВА" == org.full_name
    assert "Офицер ИБ" == org.manager
    assert ["Компания", "Подразделение 1"] == org.get_parent_chain_as_lines()
    assert org.have_basic_roles()
    assert ["Роль_01", "Роль_02"] == org.get_basic_roles()


def test_how_to_use_position():
    # Создаем объект должности и используем её данные для:
    # - создания должности в inRights
    # - назначения на должность базовых ролей (если необходимо)
    pos = Position("Должность 01",
                   parent_chain_as_lines=["Компания", "Подразделение 1"],
                   basic_roles=["Роль_01", "Роль_02"])

    assert "Должность 01" == pos.name
    assert ["Компания", "Подразделение 1"] == pos.get_parent_chain_as_lines()
    assert pos.have_basic_roles()
    assert ["Роль_01", "Роль_02"] == pos.get_basic_roles()


def test_create_orgunit_by_name():
    org = Orgunit("Подразделение 1")

    assert org.type == NodeType.Orgunit

    assert "Подразделение 1" == org.name
    assert "description: Подразделение 1" == org.full_name
    assert org.manager is None

    assert not org.have_parent()
    assert org.get_parent() is None
    assert [] == org.get_parent_chain()
    assert [] == org.get_parent_chain_as_lines()

    assert not org.have_children()
    assert [] == org.get_children()

    assert not org.have_basic_roles()
    assert [] == org.get_basic_roles()


def test_create_position_by_name():
    pos = Position("Должность 01")

    assert pos.type == NodeType.Position

    assert "Должность 01" == pos.name

    assert not pos.have_parent()
    assert pos.get_parent() is None
    assert [] == pos.get_parent_chain()
    assert [] == pos.get_parent_chain_as_lines()

    assert not pos.have_children()
    assert [] == pos.get_children()

    assert not pos.have_basic_roles()
    assert [] == pos.get_basic_roles()


def test_create_orgunit_with_all_params():
    org = Orgunit("Подразделение 1_2",
                  full_name="Подразделение ОДИН_ДВА",
                  manager="Офицер ИБ",
                  parent_chain_as_lines=["Компания", "Подразделение 1"],
                  basic_roles=["Роль_01", "Роль_02"])

    assert org.type == NodeType.Orgunit

    assert "Подразделение 1_2" == org.name
    assert "Подразделение ОДИН_ДВА" == org.full_name
    assert "Офицер ИБ" == org.manager

    assert org.have_parent()
    assert "Подразделение 1" == org.get_parent().name
    parent = org.get_parent()
    parent_parent = org.get_parent().get_parent()
    assert [parent_parent, parent] == org.get_parent_chain()
    assert ["Компания", "Подразделение 1"] == org.get_parent_chain_as_lines()

    assert not org.have_children()

    assert org.have_basic_roles()
    assert ["Роль_01", "Роль_02"] == org.get_basic_roles()


def test_create_position_with_all_params():
    pos = Position("Роль 01",
                   parent_chain_as_lines=["Компания", "Подразделение 1"],
                   basic_roles=["Роль_01", "Роль_02"])

    assert pos.type == NodeType.Position

    assert "Роль 01" == pos.name

    assert pos.have_parent()
    assert "Подразделение 1" == pos.get_parent().name
    parent = pos.get_parent()
    parent_parent = pos.get_parent().get_parent()
    assert [parent_parent, parent] == pos.get_parent_chain()
    assert ["Компания", "Подразделение 1"] == pos.get_parent_chain_as_lines()

    assert not pos.have_children()

    assert pos.have_basic_roles()
    assert ["Роль_01", "Роль_02"] == pos.get_basic_roles()


def test_add_child_org():
    org = Orgunit("Подразделение 1")
    child_org = Orgunit("Подразделение 1_2")
    org.add_child(child_org)

    assert org.have_children()
    assert [child_org] == org.get_children()

    assert child_org.have_parent()
    assert org == child_org.get_parent()
    assert [org] == child_org.get_parent_chain()
    assert ["Подразделение 1"] == child_org.get_parent_chain_as_lines()


def test_add_child():
    org = Orgunit("Подразделение 1")
    child_org = Orgunit("Подразделение 1_2")
    pos_1 = Position("Должность 1")
    pos_2 = Position("Должность 2")
    pos_03 = Position("Должность 03")
    org.add_child(child_org)
    org.add_child(pos_1)
    org.add_child(pos_2)
    child_org.add_child(pos_03)

    assert org.have_children()
    child_org_children = org.get_children()
    assert 3 == len(child_org_children)
    assert child_org in child_org_children
    assert pos_1 in child_org_children
    assert pos_2 in child_org_children

    assert child_org.have_children()
    child_org_children = child_org.get_children()
    assert 1 == len(child_org_children)
    assert pos_03 in child_org_children

    assert child_org.have_parent()
    assert org == child_org.get_parent()
    assert [org] == child_org.get_parent_chain()
    assert ["Подразделение 1"] == child_org.get_parent_chain_as_lines()


def test_parent_chain_for_org():
    org_1 = Orgunit("Подразделение 1")
    org_1_2 = Orgunit("Подразделение 1_2")
    org_1_2_3 = Orgunit("Подразделение 1_2_3")
    org_1.add_child(org_1_2)
    org_1_2.add_child(org_1_2_3)

    assert [org_1, org_1_2] == org_1_2_3.get_parent_chain()
    assert ["Подразделение 1", "Подразделение 1_2"] == org_1_2_3.get_parent_chain_as_lines()


def test_parent_chain_for_pos():
    org_1 = Orgunit("Подразделение 1")
    org_1_2 = Orgunit("Подразделение 1_2")
    pos_1_2_3 = Position("Должность 1_2_3")
    org_1.add_child(org_1_2)
    org_1_2.add_child(pos_1_2_3)

    assert [org_1, org_1_2] == pos_1_2_3.get_parent_chain()
    assert ["Подразделение 1", "Подразделение 1_2"] == pos_1_2_3.get_parent_chain_as_lines()


def test_create_orgunit_with_parent_chain_as_lines():
    org_1_2_3_4 = Orgunit('org_1_2_3_4',
                          parent_chain_as_lines=['org_1', 'org_1_2', 'org_1_2_3'])

    assert ['org_1', 'org_1_2', 'org_1_2_3'] == org_1_2_3_4.get_parent_chain_as_lines()

    org_1_2_3 = org_1_2_3_4.get_parent()
    org_1_2 = org_1_2_3.get_parent()
    org_1 = org_1_2.get_parent()

    assert [org_1, org_1_2, org_1_2_3] == org_1_2_3_4.get_parent_chain()


def test_create_position_with_parent_chain_as_lines():
    pos_1_2_3_4 = Position('pos_1_2_3_4',
                           parent_chain_as_lines=['org_1', 'org_1_2', 'org_1_2_3'])

    assert ['org_1', 'org_1_2', 'org_1_2_3'] == pos_1_2_3_4.get_parent_chain_as_lines()

    org_1_2_3 = pos_1_2_3_4.get_parent()
    org_1_2 = org_1_2_3.get_parent()
    org_1 = org_1_2.get_parent()

    assert [org_1, org_1_2, org_1_2_3] == pos_1_2_3_4.get_parent_chain()


class PrintingNodeToLines:

    def __init__(self, lines):
        self._result_lines = lines

    def print_node_to_lines(self, node):
        lines = node.get_parent_chain_as_lines()
        parents = " --> ".join(lines)
        self._result_lines.append("(" + parents + ") " + str(node.type.value) + ": " + node.name)


def test_run_func_deep():
    org_1 = Orgunit('org_1')
    org_1_1 = Orgunit('org_1_1')
    org_1_2 = Orgunit('org_1_2')
    org_1_1_1 = Orgunit('org_1_1_1')
    org_1_1_2 = Orgunit('org_1_1_2')

    pos_1_aa = Position('pos_1_aa')
    pos_1_1_1_bb = Position('pos_1_1_1_bb')
    pos_1_1_1_cc = Position('pos_1_1_1_cc')

    org_1.add_child(org_1_1)
    org_1.add_child(org_1_2)
    org_1_1.add_child(org_1_1_1)
    org_1_1.add_child(org_1_1_2)

    org_1.add_child(pos_1_aa)
    org_1_1_1.add_child(pos_1_1_1_bb)
    org_1_1_1.add_child(pos_1_1_1_cc)

    result_lines = []
    func = PrintingNodeToLines(result_lines)
    org_1.run_function_deep(func.print_node_to_lines)

    expected_lines = [
        '() Подразделение: org_1',
        '(org_1) Подразделение: org_1_1',
        '(org_1 --> org_1_1) Подразделение: org_1_1_1',
        '(org_1 --> org_1_1 --> org_1_1_1) Должность: pos_1_1_1_bb',
        '(org_1 --> org_1_1 --> org_1_1_1) Должность: pos_1_1_1_cc',
        '(org_1 --> org_1_1) Подразделение: org_1_1_2',
        '(org_1) Подразделение: org_1_2',
        '(org_1) Должность: pos_1_aa'
    ]

    assert expected_lines == result_lines


def test_print():
    assert "['basic_role']" == str(['basic_role'])
