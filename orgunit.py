from enum import Enum


class NodeType(Enum):
    Orgunit = "Подразделение"
    Position = "Должность"


class Node:

    def __init__(self, node_type, name, parent_chain_as_lines=None, basic_roles=None):
        self.type = node_type
        self.name = name
        self._parent = None
        self._children = []
        if parent_chain_as_lines is not None:
            if len(parent_chain_as_lines) > 0:
                self._add_parent_chain_by_lines(parent_chain_as_lines)
        if basic_roles is None:
            self._basic_roles = []
        else:
            self._basic_roles = basic_roles

    def have_parent(self):
        return self._parent is not None

    def get_parent(self):
        return self._parent

    def _add_parent_chain_by_lines(self, parent_chain_as_lines):
        org_chain = []
        for line in parent_chain_as_lines:
            org_chain.append(Orgunit(line))
        len_org_chain = len(org_chain)
        org_chain.append(self)
        for i in range(len_org_chain):
            org_chain[i].add_child(org_chain[i+1])

    def have_children(self):
        return len(self._children) > 0

    def get_children(self):
        return self._children

    def add_child(self, orgunit):
        orgunit._parent = self
        self._children.append(orgunit)

    def have_basic_roles(self):
        return len(self._basic_roles) > 0

    def get_basic_roles(self):
        return self._basic_roles

    def add_basic_role(self, basic_role):
        self._basic_roles.append(basic_role)

    def get_parent_chain_as_lines(self):
        parent_chain = self.get_parent_chain()
        lines = []
        if parent_chain is not None:
            for unit in parent_chain:
                lines.append(unit.name)
        return lines

    def get_parent_chain(self):
        parent_chain = []
        if self.have_parent():
            if self._parent.have_parent():
                parent_chain = self._parent.get_parent_chain()
            parent_chain.append(self._parent)
        return parent_chain

    def run_function_deep(self, func_name):
        func_name(self)
        if self.have_children():
            for child in self._children:
                child.run_function_deep(func_name)


class Position(Node):

    def __init__(self, name, parent_chain_as_lines=None, basic_roles=None):
        Node.__init__(self, NodeType.Position, name, parent_chain_as_lines, basic_roles)


class Orgunit(Node):

    def __init__(self, name, full_name=None, manager=None, parent_chain_as_lines=None, basic_roles=None):
        Node.__init__(self, NodeType.Orgunit, name, parent_chain_as_lines, basic_roles)
        if full_name is None:
            self.full_name = 'description: ' + self.name
        else:
            self.full_name = full_name
        self.manager = manager
