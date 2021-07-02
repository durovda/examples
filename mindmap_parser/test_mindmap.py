from mindmap_parser.mindmap import Node, MindMap
from spesial_asserts import assert_lines_equal


def test_create_mindmap():
    node_1 = Node(raw_text='Node 1')
    node_2 = Node(raw_text='Node 2')
    mindmap = MindMap([node_1, node_2])
    assert mindmap.root_nodes == [node_1, node_2]


def test_create_default_mindmap():
    mindmap = MindMap()
    assert mindmap.root_nodes == []


def test_mindmap_as_lines():
    node_1 = Node(raw_text='Node 1')
    node_1_1 = Node(raw_text='Node 1.1')
    node_1_1_1 = Node(raw_text='Node 1.1.1')
    node_1_1_2 = Node(raw_text='Node 1.1.2')
    node_1_2 = Node(raw_text='Node 1.2')
    node_2 = Node(raw_text='Node 2')
    node_2_1 = Node(raw_text='Node 2.1')
    node_2_1_1 = Node(raw_text='Node 2.1.1')

    node_1.add_child(node_1_1)
    node_1_1.add_child(node_1_1_1)
    node_1_1.add_child(node_1_1_2)
    node_1.add_child(node_1_2)
    node_2.add_child(node_2_1)
    node_2_1.add_child(node_2_1_1)

    mindmap = MindMap([node_1, node_2])

    expected_lines = ['Node 1',
                      '    Node 1.1',
                      '        Node 1.1.1',
                      '        Node 1.1.2',
                      '    Node 1.2',
                      'Node 2',
                      '    Node 2.1',
                      '        Node 2.1.1']
    assert mindmap.as_lines() == expected_lines


def test_mindmap_as_lines_with_tabs():
    node_1 = Node(raw_text='Node 1')
    node_1_1 = Node(raw_text='Node 1.1')
    node_1_1_1 = Node(raw_text='Node 1.1.1')

    node_1.add_child(node_1_1)
    node_1_1.add_child(node_1_1_1)

    mindmap = MindMap([node_1])

    expected_lines = ['Node 1',
                      '\tNode 1.1',
                      '\t\tNode 1.1.1']
    assert mindmap.as_lines(indent='\t') == expected_lines


def test_add_root_nodes_based_on_lines():
    lines = ['Node 1',
             '\tNode 1.1',
             '\t\tNode 1.1.1',
             '\t\tNode 1.1.2',
             '\tNode 1.2',
             'Node 2',
             '\tNode 2.1']

    expected_lines = ['Node 1',
                      '    Node 1.1',
                      '        Node 1.1.1',
                      '        Node 1.1.2',
                      '    Node 1.2',
                      'Node 2',
                      '    Node 2.1']

    mindmap = MindMap()
    mindmap.add_root_nodes_based_on_lines(lines)

    actual_lines = mindmap.as_lines()
    assert_lines_equal(actual_lines, expected_lines)


def test_create_mindmap_based_on_lines():
    lines = ['Node 1',
             '\tNode 1.1',
             '\t\tNode 1.1.1',
             '\t\tNode 1.1.2',
             '\tNode 1.2',
             'Node 2',
             '\tNode 2.1']

    expected_lines = ['Node 1',
                      '    Node 1.1',
                      '        Node 1.1.1',
                      '        Node 1.1.2',
                      '    Node 1.2',
                      'Node 2',
                      '    Node 2.1']

    mindmap = MindMap(lines_with_tabs=lines)

    actual_lines = mindmap.as_lines()
    assert_lines_equal(actual_lines, expected_lines)
