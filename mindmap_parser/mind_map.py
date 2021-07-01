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
            child.add_self_to_lines(lines, level=next_level)

    def create_children_based_on_lines(self, raw_lines, level=1):
        current_lines = []
        current_child = None
        for line in raw_lines:
            line_level = calculate_level(line)
            if line_level == level:
                if current_child is None:
                    current_child = self.add_child(Node(line.strip()))
                else:
                    current_child.create_children_based_on_lines(current_lines, level=level + 1)
                    current_lines = []
                    current_child = self.add_child(Node(line.strip()))
            else:
                current_lines.append(line)

    def __repr__(self):
        return f'({self.raw_text})'


class MindMap:
    pass
