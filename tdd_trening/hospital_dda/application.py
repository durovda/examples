from tdd_trening.hospital_dda.command_type import CommandType


class Application:
    def __init__(self, dialog_with_user=None, commands=None):
        self._dialog_with_user = dialog_with_user
        self._commands = commands

    def main(self):
        stop = False
        while not stop:
            command = self._dialog_with_user.request_command()
            if command == CommandType.GET_STATUS:
                self._commands.get_status()
            elif command == CommandType.STATUS_UP:
                self._commands.status_up()
            elif command == CommandType.STATUS_DOWN:
                self._commands.status_down()
            elif command == CommandType.CALCULATE_STATISTICS:
                self._commands.calculate_statistics()
            elif command == CommandType.STOP:
                self._commands.stop()
                stop = True
            elif command == CommandType.UNKNOWN:
                self._dialog_with_user.send_message('Неизвестная команда! Попробуйте ещё раз')
