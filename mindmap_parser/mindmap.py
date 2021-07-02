def calculate_level(raw_line):
    count = 0
    for symbol in raw_line:
        if symbol == '\t':
            count += 1
        else:
            return count
    return count


class Node:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        return child_node

    def add_self_to_lines(self, lines, indent='    ', level=0):
        lines.append(indent * level + self.raw_text)
        next_level = level + 1
        for child in self.children:
            child.add_self_to_lines(lines, indent=indent, level=next_level)

    def add_children_based_on_lines(self, lines, level=1):
        current_lines = []
        current_child = None
        for line in lines:
            line_level = calculate_level(line)
            if line_level == level:
                if current_child is None:
                    current_child = self.add_child(Node(line.strip()))
                else:
                    current_child.add_children_based_on_lines(current_lines, level=level + 1)
                    current_lines = []
                    current_child = self.add_child(Node(line.strip()))
            else:
                current_lines.append(line)
        if len(current_lines) > 0:
            current_child.add_children_based_on_lines(current_lines, level=level + 1)

    def __repr__(self):
        return f'({self.raw_text})'


class MindMap:
    def __init__(self, root_node_list=None, lines_with_tabs=None):
        self.root_nodes = root_node_list or []
        if lines_with_tabs is not None:
            self.add_root_nodes_based_on_lines(lines_with_tabs)

    def add_root_node(self, root_node):
        self.root_nodes.append(root_node)
        return root_node

    def as_lines(self, indent='    '):
        lines = []
        for node in self.root_nodes:
            node.add_self_to_lines(lines, indent=indent)
        return lines

    def add_root_nodes_based_on_lines(self, lines_with_tabs):
        level = 0
        current_lines = []
        current_root_node = None
        for line in lines_with_tabs:
            line_level = calculate_level(line)
            if line_level == level:
                if current_root_node is None:
                    current_root_node = self.add_root_node(Node(line.strip()))
                else:
                    current_root_node.add_children_based_on_lines(current_lines, level=1)
                    current_lines = []
                    current_root_node = self.add_root_node(Node(line.strip()))
            else:
                current_lines.append(line)
        if len(current_lines) > 0:
            current_root_node.add_children_based_on_lines(current_lines, level=1)
