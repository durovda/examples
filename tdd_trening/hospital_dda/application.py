class Command:
    STOP = 1
    STATUS_UP = 2
    STATUS_DOWN = 3
    GET_STATUS = 4
    UNKNOWN = 5


class Application:
    def __init__(self, hospital=None, input_stream=None, output_stream=None):
        self._hospital = hospital
        self._input_stream = input_stream
        self._output_stream = output_stream

    def main(self):
        stop = False
        while not stop:
            command = self._get_command_from_input_stream()
            if command == Command.GET_STATUS:
                patient_id = self._get_patient_id_from_input_stream()
                self._cmd_get_status(patient_id)
            elif command == Command.STATUS_UP:
                patient_id = self._get_patient_id_from_input_stream()
                self._cmd_status_up(patient_id)
            elif command == Command.STATUS_DOWN:
                patient_id = self._get_patient_id_from_input_stream()
                self._cmd_status_down(patient_id)
            elif command == Command.STOP:
                self._cmd_stop()
                stop = True
            elif command == Command.UNKNOWN:
                self._output_stream.send_message('Неизвестная команда! Попробуйте ещё раз')

    def _get_command_from_input_stream(self):
        command_as_text = self._input_stream.get_message('Введите команду: ')
        if command_as_text == 'стоп':
            return Command.STOP
        elif command_as_text == 'узнать статус пациента':
            return Command.GET_STATUS
        elif command_as_text == 'повысить статус пациента':
            return Command.STATUS_UP
        elif command_as_text == 'понизить статус пациента':
            return Command.STATUS_DOWN
        else:
            return Command.UNKNOWN

    def _get_patient_id_from_input_stream(self):
        return int(self._input_stream.get_message('Введите ID пациента: '))

    def _cmd_stop(self):
        text = 'Сеанс завершён.\nСтатистика на конец сеанса:'
        statistics = self._hospital.get_statistics()
        for status in statistics:
            text += f'\n - в статусе "{status}": {statistics[status]} чел.'
        self._output_stream.send_message(text)

    def _cmd_get_status(self, patient_id):
        patient_status = self._hospital.get_patient_status_by_id(patient_id)
        self._output_stream.send_message(f'Статус пациента: "{patient_status}"')

    def _cmd_status_up(self, patient_id):
        self._hospital.patient_status_up(patient_id)
        new_status = self._hospital.get_patient_status_by_id(patient_id)
        self._output_stream.send_message(f'Новый статус пациента: "{new_status}"')

    def _cmd_status_down(self, patient_id):
        self._hospital.patient_status_down(patient_id)
        new_status = self._hospital.get_patient_status_by_id(patient_id)
        self._output_stream.send_message(f'Новый статус пациента: "{new_status}"')
