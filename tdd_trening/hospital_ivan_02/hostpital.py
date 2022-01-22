from string import Template as str_template


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
        self.text_statistics_total = str_template(
            'В больнице на данный момент находится '
            '$total , из них:\n'
        )
        self.text_statistics_separate = str_template(
            ' - в статусе "$status": $count чел.'
        )
        self.text_new_patient_status = str_template(
            'Новый статус пациента: "$status"'
        )
        self.text_min_patient_status = str_template(
            f'У этого пациента самый низкий статус "$min_status".\n'
            'Статус пациента не изменился, т.к. в нашей больнице '
            'пациенты не умирают!\n'
        )
        self.text_max_patient_status = str_template(
            'У этого пациента самый высокий статус "$max_status".\n'
            'Желаете ли выписать этого пациента?'
        )
        self.text_wrong_command = 'Неизвестная команда! Попробуйте ещё раз'
        self.text_enter_command = 'Введите команду: '
        self.text_patient_doesnt_exists = 'Пациент с указанным индексом отсутствует'
        self.text_session_closed = 'Сеанс завершён.'
        self.text_yes_or_no_question = '(да/нет) '
        self.text_get_id_text = 'Введите ID пациента: '

    def raise_patient_status(self):
        # повысить статус пациент
        index = self._ask_for_index()
        new_user_status = self.db.get_patient_by_index(index) + 1
        if new_user_status == len(self.statuses):
            if self._ask_about_discharge_from_hostpital():
                self.db.delete_patient(index)
        else:
            self.db.update_patient_status(index, new_user_status)
            return self._print_new_patient_status(new_user_status)

    def reduce_patient_status(self):
        # понизить статус пациента
        index = self._ask_for_index()
        new_user_status = self.db.get_patient_by_index(index) - 1
        if new_user_status < self.min_status:
            self._print_what_reduce_is_unable()
        else:
            self.db.update_patient_status(index, new_user_status)
            self._print_new_patient_status(new_user_status)

    def start_dialog_with_user(self):
        # начать диалог с пользователем
        while not self.time_to_exit:
            command = self._input_method(self.text_enter_command)
            is_matched = self._get_method_matched_with_commands_dict(command)
            if is_matched:
                is_matched()
            else:
                self._print_unknown_command_error()
        return 0

    def print_statistics_by_patients_groups(self):
        # отобразить статистику по группам пациентов
        total_text = self.text_statistics_total.substitute(
            total=self.db.get_total_patients_count())
        patients_groups_stat = self._calc_patients_stat_by_groups()
        statistics_text = [
            self.text_statistics_separate.substitute(
                status=self.statuses[k], count=v)
            for k, v in patients_groups_stat.items()]

        return self._print_method(total_text + '\n'.join(statistics_text))

    def ask_and_print_patient_status(self):
        # получить и отобразить статус пациента
        index = self._ask_for_index()
        user_status = self.db.get_patient_by_index(index)
        if user_status:
            return self._print_method(self.statuses[user_status])
        else:
            return self._print_method(self.text_patient_doesnt_exists)

    def stop_dialog(self):
        # отстановить диалог с пользователем
        self.time_to_exit = True
        return self._print_method(self.text_session_closed)

    def _get_method_matched_with_commands_dict(self, command):
        # получить команду сопаставив текст из терминала с словарем команд
        #  Можно расписать более сложную логику
        return self.command_matcher.get(command)

    def _ask_about_discharge_from_hostpital(self):
        # отоборазить текст о возможной выписке и спросить о ней
        self._print_what_patient_can_be_discharged()
        return self._ask_yes_or_no()

    def _ask_for_index(self, text=''):
        # спросить у пользователя ID пациента
        if text == '':
            text = self.text_get_id_text
        index = self._input_method(text)
        return int(index)

    def _ask_yes_or_no(self):
        # спросить у пользователя да или нет
        voice = self._input_method(self.text_yes_or_no_question)
        if 'да' in voice:
            return True
        if 'нет' in voice:
            return False

    def _calc_patients_stat_by_groups(self):
        # рассчитываем статистику по группам
        stat_with_zeros = {
            k: self.db.get_patients_count_by_status(k)
            for k in self.statuses.keys()
        }
        return {k: v for k, v in stat_with_zeros.items() if v != 0}

    def _print_what_reduce_is_unable(self):
        # отобразить текст о невозможности понижения статуса пациента
        return self._print_method(
            self.text_min_patient_status.substitute(min_status=self.min_status)
        )

    def _print_what_patient_can_be_discharged(self):
        # отобразить текст о возможной выписке пациента
        return self._print_method(
            self.text_max_patient_status.substitute(max_status=self.max_status)
        )

    def _print_new_patient_status(self, status=''):
        # отобразить новый статус пациента
        return self._print_method(self.text_new_patient_status.substitute(
            status=self.statuses[status]))

    def _print_unknown_command_error(self):
        # отобразить ошибку о неизвестной команде
        return self._print_method(self.text_wrong_command)


class HospitalListDB:
    def __init__(self, db):
        self.db = db

    def get_patients_count_by_status(self, status: int):
        # Получить число пациентов с определенным статусом
        return len(list(filter(
            lambda patient_stat: patient_stat == status, self.db)))

    def get_total_patients_count(self):
        # Получить общее число пациентов
        return len(self.db)

    def get_patient_by_index(self, patient_index: int):
        # получить статус пациент по индекс
        if patient_index <= len(self.db):
            return self.db[patient_index-1]
        else:
            return None

    def update_patient_status(self, patient_index: int, new_status: int):
        # записать новый статус пациента
        self.db[patient_index-1] = new_status

    def delete_patient(self, patient_index: int):
        # удалить пациента
        self.db.pop(patient_index-1)


# if __name__ == '__main__':
#     statuses = {
#         0: 'Тяжело болен',
#         1: 'Болен',
#         2: 'Слегка болен',
#         3: 'Готов к выписке',
#     }
#     hospital = HospitalListDB([1] * 200)
#     dlg = Application(hospital, statuses)
#     dlg.start_dialog_with_user()
