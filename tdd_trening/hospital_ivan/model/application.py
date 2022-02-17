from model.db import NonExistentPatientIdError, HospitalListDB, MinStatusExceedError


class NotIntegerError(Exception):
    pass


class YesOrNoError(Exception):
    pass


class Application:
    def __init__(self, db=None):
        if db is None:
            self.db_interface = HospitalListDB([])
        else:
            self.db_interface = db
        self.time_to_exit = False
        self._input_method = input
        self._print_method = print
        self.text_statistics_separate = \
            lambda stat, count: f' - в статусе "{stat}": {count} чел.'

    def _cmd_raise_patient_status(self):
        """ Повысить статус пациента """
        try:
            index = self._request_for_index()
            user_status = self.db_interface.get_patient_status_by_index(index)
            new_user_status = user_status + 1

            if new_user_status < len(self.db_interface.statuses):
                self.db_interface.raise_patient_status(index)
                return f'Новый статус пациента: "{self.db_interface.statuses[new_user_status]}"'
            else:
                confirmation_about_discharge_from_hospital = \
                    self._request_confirmation_about_discharge_from_hostpital()
                if not confirmation_about_discharge_from_hospital:
                    return f'Пациент остался в статусе "{self.db_interface.statuses[new_user_status - 1]}"'
                else:
                    self.db_interface.delete_patient(index)
                    return f'Пациент с ID={index + 1} выписан.'

        except (NonExistentPatientIdError, NotIntegerError) as err:
            return str(err)
        except YesOrNoError as err:
            return str(err)

    def _cmd_reduce_patient_status(self):
        """ Понизить статус пациента """
        try:
            index = self._request_for_index()
            self.db_interface.reduce_patient_status(index)
            new_status = self.db_interface.get_patient_status_by_index(index)
            return f'Новый статус пациента: "{self.db_interface.statuses[new_status]}"'

        except MinStatusExceedError as err:
            return str(err)
        except (NonExistentPatientIdError, NotIntegerError) as err:
            return str(err)

    def _cmd_get_patient_status(self):
        """ Получить и отобразить статус пациента """
        try:
            index = self._request_for_index()
            user_status = self.db_interface.get_patient_status_by_index(index)
            return self.db_interface.statuses[user_status]
        except (NonExistentPatientIdError, NotIntegerError) as err:
            return str(err)

    def start_dialog_with_user(self):
        """ Начать диалог с пользователем """
        self.time_to_exit = False
        while not self.time_to_exit:
            command = self._input_method('Введите команду: ')
            matched_method = self._match_command(command)
            if matched_method:
                message = matched_method()
                self._print_method(message)
            else:
                self._print_method('Неизвестная команда! Попробуйте ещё раз')

    def _match_command(self, command_as_text):
        command_as_text = str(command_as_text).lower()
        if command_as_text in ['стоп', 'stop']:
            return self._cmd_stop_dialog
        elif command_as_text in ['рассчитать статистику', 'calc stat']:
            return self._cmd_print_statistics_by_patients_groups
        elif command_as_text in ['узнать статус пациента', 'get status']:
            return self._cmd_get_patient_status
        elif command_as_text in ['повысить статус пациента', 'raise status']:
            return self._cmd_raise_patient_status
        elif command_as_text in ['понизить статус пациента', 'reduce status']:
            return self._cmd_reduce_patient_status

    def _cmd_print_statistics_by_patients_groups(self):
        """ Отобразить статистику по группам пациентов """
        total_patients_count = self.db_interface.get_total_patients_count()
        total_text = 'В больнице на данный момент ' \
                     f'находится {total_patients_count} пациентов, ' \
                     'из них:\n'
        patients_groups_stat = self.db_interface.calc_patients_stat_by_groups()

        statistics_text = [
            self.text_statistics_separate(
                stat=self.db_interface.statuses[k], count=v)
            for k, v in patients_groups_stat.items()]

        return total_text + '\n'.join(statistics_text)

    def _cmd_stop_dialog(self):
        """ Отстановить диалог с пользователем """
        self.time_to_exit = True
        return 'Сеанс завершён.'

    def _request_confirmation_about_discharge_from_hostpital(self):
        """ Отоборазить текст о возможной выписке и спросить о ней """
        text = 'У этого пациента самый высокий статус ' \
               f'"{self.db_interface.statuses[self.db_interface.max_status]}".\n' \
               'Желаете ли выписать этого пациента?'
        self._print_method(text)
        voice = self._input_method('(да/нет) ')
        if 'да' in voice:
            return True
        elif 'нет' in voice:
            return False
        else:
            raise YesOrNoError('Ошибка. Нужно ответить "да" или "нет"')

    def _request_for_index(self, text=''):
        """ Спросить у пользователя ID пациента """
        if text == '':
            text = 'Введите ID пациента: '
        index = self._input_method(text)
        try:
            return int(index) - 1
        except ValueError:
            raise NotIntegerError(
                'Ошибка. Требуется ввести целочисленное значение!')
