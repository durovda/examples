class CommandType:
    STOP = 'стоп'
    STATUS_UP = 'повысить статус пациента'
    STATUS_DOWN = 'понизить статус пациента'
    GET_STATUS = 'узнать статус пациента'
    CALCULATE_STATISTICS = 'рассчитать статистику'
    UNKNOWN = 'неизвестная команда'


class Application:
    def __init__(self, dialog_with_user=None, commands=None):
        self._dialog_with_user = dialog_with_user
        self._commands = commands

    def main(self):
        stop = False
        while not stop:
            command = self._dialog_with_user.request_command()
            if command == CommandType.GET_STATUS:
                result_message = self._commands.get_status()
                self._dialog_with_user.send_message(result_message)
            elif command == CommandType.STATUS_UP:
                result_message = self._commands.status_up()
                self._dialog_with_user.send_message(result_message)
            elif command == CommandType.STATUS_DOWN:
                result_message = self._commands.status_down()
                self._dialog_with_user.send_message(result_message)
            elif command == CommandType.CALCULATE_STATISTICS:
                result_message = self._commands.calculate_statistics()
                self._dialog_with_user.send_message(result_message)
            elif command == CommandType.STOP:
                result_message = self._commands.stop()
                self._dialog_with_user.send_message(result_message)
                stop = True
            elif command == CommandType.UNKNOWN:
                self._dialog_with_user.send_message('Неизвестная команда! Попробуйте ещё раз')
