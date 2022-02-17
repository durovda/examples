class PatientIdNotIntegerError(Exception):
    def __init__(self):
        super().__init__('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')


class MinStatusCannotDownError(Exception):
    def __init__(self):
        super().__init__('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')


class MaxStatusCannotUpError(Exception):
    def __init__(self):
        super().__init__('Ошибка. Нельзя повысить самый высокий статус. Но этого пациента можно выписать')


class PatientNotExistsError(Exception):
    def __init__(self):
        super().__init__('Ошибка. В больнице нет пациента с таким ID')

