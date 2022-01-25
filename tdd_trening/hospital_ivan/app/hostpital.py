class Application:
    def __init__(self, db, statuses):
        self.db = db
        self.statuses = statuses
        self.min_status = min(self.statuses.keys())
        self.max_status = max(self.statuses.keys())
        self.time_to_exit = False
        self._input_method = input
        self._print_method = print
        self.command_matcher = {
            'рассчитать статистику': self.print_statistics_by_patients_groups,
            'узнать статус пациента': self.ask_and_print_patient_status,
            'повысить статус пациента': self.raise_patient_status,
            'понизить статус пациента': self.reduce_patient_status,
            'стоп': self.stop_dialog,
        }
        self.text_statistics_separate = \
            lambda stat, count: f' - в статусе "{stat}": {count} чел.'
        self.text_new_patient_status = \
            lambda stat: f'Новый статус пациента: "{stat}"'

    def raise_patient_status(self):
        """ Повысить статус пациента """
        index = self._ask_for_index()
        new_user_status = self.db.get_patient_status_by_index(index) + 1
        if new_user_status == len(self.statuses):
            if self._ask_about_discharge_from_hostpital():
                self.db.delete_patient(index)
        else:
            self.db.update_patient_status(index, new_user_status)
            self._print_method(
                self.text_new_patient_status(
                    self.statuses[new_user_status]))

    def reduce_patient_status(self):
        """ Понизить статус пациента """
        index = self._ask_for_index()
        new_user_status = self.db.get_patient_status_by_index(index) - 1
        if new_user_status < self.min_status:
            self._print_method(
                'У этого пациента самый низкий статус '
                f'"{self.statuses[self.min_status]}".\n'
                'Статус пациента не изменился, т.к. в нашей больнице '
                'пациенты не умирают!\n'
            )
        else:
            self.db.update_patient_status(index, new_user_status)
            self._print_method(
                self.text_new_patient_status(
                    stat=self.statuses[new_user_status]))

    def start_dialog_with_user(self):
        """ Начать диалог с пользователем """
        while not self.time_to_exit:
            command = self._input_method('Введите команду: ')
            matched_method = self.command_matcher.get(command)
            if matched_method:
                matched_method()
            else:
                self._print_method('Неизвестная команда! Попробуйте ещё раз')

    def print_statistics_by_patients_groups(self):
        """ Отобразить статистику по группам пациентов """
        total_patients_count = self.db.get_total_patients_count()
        total_text = 'В больнице на данный момент ' \
                     f'находится {total_patients_count}, ' \
                     'из них:\n'
        patients_groups_stat = self._calc_patients_stat_by_groups()

        statistics_text = [
            self.text_statistics_separate(
                stat=self.statuses[k], count=v)
            for k, v in patients_groups_stat.items()]

        return self._print_method(total_text + '\n'.join(statistics_text))

    def ask_and_print_patient_status(self):
        """ Получить и отобразить статус пациента """
        index = self._ask_for_index()
        user_status = self.db.get_patient_status_by_index(index)
        if self.statuses.get(user_status):
            return self._print_method(self.statuses[user_status])
        else:
            return self._print_method('Пациент с указанным индексом отсутствует')

    def stop_dialog(self):
        """ Отстановить диалог с пользователем """
        self.time_to_exit = True
        return self._print_method('Сеанс завершён.')

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
        return int(index) + 1

    def _ask_yes_or_no(self):
        """ Спросить у пользователя да или нет """
        voice = self._input_method('(да/нет) ')
        if 'да' in voice:
            return True
        if 'нет' in voice:
            return False

    def _calc_patients_stat_by_groups(self):
        """ Рассчитываем статистику по группам """
        stat_with_zeros = {
            k: self.db.get_patients_count_by_status(k)
            for k in self.statuses.keys()
        }
        return {k: v for k, v in stat_with_zeros.items() if v != 0}
