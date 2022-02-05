from model.db import NonExistentPatientIdError


class NotIntegerError(Exception):
    def __init__(self, message):
        self.message = message


class YesOrNoError(Exception):
    def __init__(self, message):
        self.message = message


class Application:
    def __init__(self, db=None, statuses=None):
        if statuses is None:
            statuses = {
                0: 'Тяжело болен',
                1: 'Болен',
                2: 'Слегка болен',
                3: 'Готов к выписке',
            }
        self.db_interface = db
        self.statuses = statuses
        self.min_status = min(self.statuses.keys())
        self.max_status = max(self.statuses.keys())
        self.time_to_exit = False
        self._input_method = input
        self._print_method = print
        self.text_statistics_separate = \
            lambda stat, count: f' - в статусе "{stat}": {count} чел.'

    def raise_patient_status(self):
        """ Повысить статус пациента """
        try:
            index = self._ask_for_index()
            user_status = self.db_interface.get_patient_status_by_index(index)
            new_user_status = user_status + 1
            if new_user_status == len(self.statuses):
                if self._ask_about_discharge_from_hostpital():
                    self.db_interface.delete_patient(index)
                    return f'Пациент с ID={index + 1} выписан.'
                else:
                    return f'Пациент остался в статусе "{self.statuses[new_user_status-1]}"'
            else:
                self.db_interface.update_patient_status(index, new_user_status)
                return f'Новый статус пациента: "{self.statuses[new_user_status]}"'
        except (NonExistentPatientIdError, NotIntegerError) as err:
            return err.message
        except YesOrNoError as err:
            return err.message

    def reduce_patient_status(self):
        """ Понизить статус пациента """
        try:
            index = self._ask_for_index()
            user_status = self.db_interface.get_patient_status_by_index(index)
            new_user_status = user_status - 1
            if new_user_status < self.min_status:
                return (
                    'У этого пациента самый низкий статус '
                    f'"{self.statuses[self.min_status]}".\n'
                    'Статус пациента не изменился, т.к. в нашей больнице '
                    'пациенты не умирают!\n'
                )
            else:
                self.db_interface.update_patient_status(index, new_user_status)
                return f'Новый статус пациента: "{self.statuses[new_user_status]}"'
        except (NonExistentPatientIdError, NotIntegerError) as err:
            return err.message

    def print_patient_status(self):
        """ Получить и отобразить статус пациента """
        try:
            index = self._ask_for_index()
            user_status = self.db_interface.get_patient_status_by_index(index)
            return self.statuses[user_status]
        except (NonExistentPatientIdError, NotIntegerError) as err:
            return err.message

    def start_dialog_with_user(self):
        """ Начать диалог с пользователем """
        while not self.time_to_exit:
            command = self._input_method('Введите команду: ')
            matched_method = self.match_command(command)
            if matched_method:
                message = matched_method()
                self._print_method(message)
            else:
                self._print_method('Неизвестная команда! Попробуйте ещё раз')

    def match_command(self, command_as_text):
        command_as_text = command_as_text.lower()
        if command_as_text in ['стоп', 'stop']:
            return self.stop_dialog
        elif command_as_text in ['рассчитать статистику', 'calc stat']:
            return self.print_statistics_by_patients_groups
        elif command_as_text in ['узнать статус пациента', 'get status']:
            return self.print_patient_status
        elif command_as_text in ['повысить статус пациента', 'raise status']:
            return self.raise_patient_status
        elif command_as_text in ['понизить статус пациента', 'reduce status']:
            return self.reduce_patient_status

    def print_statistics_by_patients_groups(self):
        """ Отобразить статистику по группам пациентов """
        total_patients_count = self.db_interface.get_total_patients_count()
        total_text = 'В больнице на данный момент ' \
                     f'находится {total_patients_count} пациентов, ' \
                     'из них:\n'
        patients_groups_stat = self._calc_patients_stat_by_groups()

        statistics_text = [
            self.text_statistics_separate(
                stat=self.statuses[k], count=v)
            for k, v in patients_groups_stat.items()]

        return total_text + '\n'.join(statistics_text)

    def stop_dialog(self):
        """ Отстановить диалог с пользователем """
        self.time_to_exit = True
        return 'Сеанс завершён.'

    def _ask_about_discharge_from_hostpital(self):
        """ Отоборазить текст о возможной выписке и спросить о ней """
        text = 'У этого пациента самый высокий статус ' \
               f'"{self.statuses[self.max_status]}".\n' \
               'Желаете ли выписать этого пациента?'
        self._print_method(text)
        return self._ask_yes_or_no()

    def _ask_for_index(self, text=''):
        """ Спросить у пользователя ID пациента """
        if text == '':
            text = 'Введите ID пациента: '
        index = self._input_method(text)
        try:
            return int(index) - 1
        except ValueError:
            raise NotIntegerError(
                'Ошибка. Требуется ввести целочисленное значение!')

    def _ask_yes_or_no(self):
        """ Спросить у пользователя да или нет """
        voice = self._input_method('(да/нет) ')
        if 'да' in voice:
            return True
        elif 'нет' in voice:
            return False
        else:
            raise YesOrNoError('Ошибка. Нужно ответить "да" или "нет"')

    def _calc_patients_stat_by_groups(self):
        """ Рассчитываем статистику по группам """
        stat_with_zeros = {
            k: self.db_interface.get_patients_count_by_status(k)
            for k in self.statuses.keys()
        }
        return {k: v for k, v in stat_with_zeros.items() if v != 0}
