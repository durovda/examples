from tdd_trening.hospital_dda.exceptions import IdNotIntegerError


class Command:
    STOP = 'стоп'
    STATUS_UP = 'повысить статус пациента'
    STATUS_DOWN = 'понизить статус пациента'
    GET_STATUS = 'узнать статус пациента'
    CALCULATE_STATISTICS = 'рассчитать статистику'
    UNKNOWN = 'неизвестная команда'


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
                result_message = self._cmd_get_status()
                self._send_message_to_output_stream(result_message)
            elif command == Command.STATUS_UP:
                result_message = self._cmd_status_up()
                self._send_message_to_output_stream(result_message)
            elif command == Command.STATUS_DOWN:
                result_message = self._cmd_status_down()
                self._send_message_to_output_stream(result_message)
            elif command == Command.CALCULATE_STATISTICS:
                result_message = self._cmd_calculate_statistics()
                self._send_message_to_output_stream(result_message)
            elif command == Command.STOP:
                result_message = self._cmd_stop()
                self._send_message_to_output_stream(result_message)
                stop = True
            elif command == Command.UNKNOWN:
                self._send_message_to_output_stream('Неизвестная команда! Попробуйте ещё раз')

    def _send_message_to_output_stream(self, text_message):
        self._output_stream.print(text_message)

    def _get_command_from_input_stream(self):
        command_as_text = self._input_stream.input('Введите команду: ')
        return self._parse_text_to_command(command_as_text)

    def _get_patient_id_from_input_stream(self):
        try:
            return int(self._input_stream.input('Введите ID пациента: '))
        except ValueError:
            raise IdNotIntegerError('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')

    @staticmethod
    def _cmd_stop():
        return 'Сеанс завершён.'

    def _cmd_get_status(self):
        try:
            patient_id = self._get_patient_id_from_input_stream()
            patient_status = self._hospital.get_patient_status_by_id(patient_id)
            result_message = f'Статус пациента: "{patient_status}"'
            return result_message
        except TypeError as err:
            return str(err)

    def _cmd_status_up(self):
        patient_id = self._get_patient_id_from_input_stream()
        status = self._hospital.get_patient_status_by_id(patient_id)
        if status == 'Готов к выписке':
            discharge_confirmation = self._get_patient_discharge_confirmation_from_input_stream()
            if discharge_confirmation:
                self._hospital.discharge_patient(patient_id)
                result_message = 'Пациент выписан из больницы'
                return result_message
            else:
                result_message = 'Пациент остался в статусе "Готов к выписке"'
                return result_message
        else:
            self._hospital.patient_status_up(patient_id)
            new_status = self._hospital.get_patient_status_by_id(patient_id)
            result_message = f'Новый статус пациента: "{new_status}"'
            return result_message

    def _cmd_status_down(self):
        patient_id = self._get_patient_id_from_input_stream()
        self._hospital.patient_status_down(patient_id)
        new_status = self._hospital.get_patient_status_by_id(patient_id)
        result_message = f'Новый статус пациента: "{new_status}"'
        return result_message

    def _cmd_calculate_statistics(self):
        result_message = 'Статистика по статусам:'
        statistics = self._hospital.get_statistics()
        for status in statistics:
            result_message += f'\n - в статусе "{status}": {statistics[status]} чел.'
        return result_message

    @staticmethod
    def _parse_text_to_command(command_as_text):
        command_as_text = command_as_text.lower()
        if command_as_text in ['стоп', 'stop']:
            return Command.STOP
        elif command_as_text == 'узнать статус пациента':
            return Command.GET_STATUS
        elif command_as_text == 'повысить статус пациента':
            return Command.STATUS_UP
        elif command_as_text == 'понизить статус пациента':
            return Command.STATUS_DOWN
        elif command_as_text == 'рассчитать статистику':
            return Command.CALCULATE_STATISTICS
        else:
            return Command.UNKNOWN

    def _get_patient_discharge_confirmation_from_input_stream(self):
        confirmation_text = self._input_stream.input('Желаете этого клиента выписать? (да/нет) ')
        return confirmation_text in ['да', 'yes']
