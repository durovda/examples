class TestCase:
    def __init__(self, key_raw=None, name_raw=None, folder_raw=None, objective_raw=None, precondition_raw=None):
        self.key_raw = key_raw
        self.name_raw = name_raw
        self.folder_raw = folder_raw
        self.objective_raw = objective_raw
        self.precondition_raw = precondition_raw
        self.steps = []

    def as_lines(self, indent=0):
        lines = []
        lines.append('\t' * (indent) + ' --> '.join(self.folder))
        lines.append('\t' * (indent + 1) + self.name)
        if (self.objective is not None) and (len(self.objective) > 0):
            lines.append('\t' * (indent + 2) + 'objective:')
            for line in self.objective:
                lines.append('\t' * (indent + 3) + line)
        if (self.precondition is not None) and (len(self.precondition) > 0):
            lines.append('\t' * (indent + 2) + 'precondition:')
            for line in self.precondition:
                lines.append('\t' * (indent + 3) + line)
        if len(self.steps) > 0:
            for step in self.steps:
                lines += step.as_lines(indent=(indent + 2))
        return lines

    def add_step(self, step):
        self.steps.append(step)

    @property
    def name(self):
        return self.name_raw

    @property
    def key(self):
        return self.key_raw

    @property
    def folder(self):
        return self.folder_raw.split('/')

    @property
    def objective(self):
        if self.objective_raw is None:
            return None
        text = self.objective_raw.replace('<br />', '<br/>')
        lines_raw = text.split('<br/>')
        lines = []
        for line in lines_raw:
            line = line.strip()
            if line != '':
                lines.append(line)
        return lines

    @property
    def precondition(self):
        if self.precondition_raw is None:
            return None
        text = self.precondition_raw.replace('<br />', '<br/>')
        lines_raw = text.split('<br/>')
        lines = []
        for line in lines_raw:
            line = line.strip()
            if line != '':
                lines.append(line)
        return lines


class Step:
    def __init__(self, index=None, description_raw=None, expected_result_raw=None):
        self.index = index
        self.description_raw = description_raw
        self.expected_result_raw = expected_result_raw

    def as_lines(self, indent=0):
        lines = []
        lines.append('\t' * (indent) + 'step ' + str(self.index) + ':')
        if (self.description is not None) and (len(self.description) > 0):
            for line in self.description:
                lines.append('\t' * (indent + 1) + line)
        if (self.expected_result is not None) and (len(self.expected_result) > 0):
            lines.append('\t' * (indent + 1) + 'expected_result:')
            for line in self.expected_result:
                lines.append('\t' * (indent + 2) + line)
        return lines

    @property
    def description(self):
        if self.description_raw is None:
            return None
        text = self.description_raw.replace('<br />', '<br/>')
        lines_raw = text.split('<br/>')
        lines = []
        for line in lines_raw:
            line = line.strip()
            if line != '':
                lines.append(line)
        return lines

    @property
    def expected_result(self):
        if self.expected_result_raw is None:
            return None
        text = self.expected_result_raw.replace('<br />', '<br/>')
        lines_raw = text.split('<br/>')
        lines = []
        for line in lines_raw:
            line = line.strip()
            if line != '':
                lines.append(line)
        return lines
