from tdd_trening.hospital_dda.command_type import CommandType
from tdd_trening.hospital_dda.exceptions import PatientIdNotIntegerError


class DialogWithUser:
    def __init__(self, console=None):
        self._console = console

    def send_message(self, text_message):
        self._console.print(text_message)

    def request_command(self):
        command_as_text = self._console.input('Введите команду: ')
        return self._parse_text_to_command(command_as_text)

    @staticmethod
    def _parse_text_to_command(command_as_text):
        command_as_text = command_as_text.lower()
        if command_as_text in ['стоп', 'stop']:
            return CommandType.STOP
        elif command_as_text == 'узнать статус пациента':
            return CommandType.GET_STATUS
        elif command_as_text == 'повысить статус пациента':
            return CommandType.STATUS_UP
        elif command_as_text == 'понизить статус пациента':
            return CommandType.STATUS_DOWN
        elif command_as_text == 'рассчитать статистику':
            return CommandType.CALCULATE_STATISTICS
        else:
            return CommandType.UNKNOWN

    def request_patient_id(self):
        try:
            id_as_text = self._console.input('Введите ID пациента: ')
            return int(id_as_text)
        except ValueError:
            raise PatientIdNotIntegerError

    def request_patient_discharge_confirmation(self):
        confirmation_text = self._console.input('Желаете этого клиента выписать? (да/нет) ')
        return confirmation_text in ['да', 'yes']
