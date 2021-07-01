from mindmap_parser.mind_map import Node, calculate_level
from spesial_asserts import assert_lines_equal


def test_create_node():
    node = Node(raw_text='Node 1')
    assert node.raw_text == 'Node 1'
    assert node.children == []


def test_add_child():
    node_1 = Node(raw_text='Node *1*')
    node_1_1 = Node(raw_text='Node *1.1*')
    new_child = node_1.add_child(node_1_1)
    assert node_1.children == [node_1_1]
    assert new_child == node_1_1


def test_add_self_to_lines():
    node_1 = Node(raw_text='Node 1')
    node_1_1 = Node(raw_text='Node 1.1')
    node_1_1_1 = Node(raw_text='Node 1.1.1')
    node_1_1_2 = Node(raw_text='Node 1.1.2')
    node_1_2 = Node(raw_text='Node 1.2')

    node_1.add_child(node_1_1)
    node_1_1.add_child(node_1_1_1)
    node_1_1.add_child(node_1_1_2)
    node_1.add_child(node_1_2)

    expected_lines = ['Node 1',
                      '    Node 1.1',
                      '        Node 1.1.1',
                      '        Node 1.1.2',
                      '    Node 1.2']
    actual_lines = []
    node_1.add_self_to_lines(actual_lines)
    assert_lines_equal(actual_lines, expected_lines)


def test_calculate_level_0():
    assert calculate_level('Raw line') == 0


def test_calculate_level_2():
    assert calculate_level('\t\tRaw line') == 2


def test_create_children_based_on_lines():
    node_1 = Node(raw_text='Node 1')
    raw_lines = ['\tNode 1.1',
                 '\t\tNode 1.1.1',
                 '\t\t\tNode 1.1.1.1',
                 '\t\t\tNode 1.1.1.2',
                 '\t\t\tNode 1.1.1.3',
                 '\t\tNode 1.1.2',
                 '\tNode 1.2']
    node_1.create_children_based_on_lines(raw_lines)
    expected_lines = ['Node 1',
                      '    Node 1.1',
                      '        Node 1.1.1',
                      '            Node 1.1.1.1',
                      '            Node 1.1.1.2',
                      '            Node 1.1.1.3',
                      '        Node 1.1.2',
                      '    Node 1.2']
    actual_lines = []
    node_1.add_self_to_lines(actual_lines)
    assert_lines_equal(actual_lines, expected_lines)
