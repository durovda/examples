import argparse

GET_ID_TEXT = 'Введите ID пациента: '


def parse_script_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db",
                        help="Путь к файлу с БД больницы")
    parser.add_argument("--statuses",
                        help="Используемые настройки скриптов")
    args = parser.parse_args()
    return args


class Application:
    def __init__(self, db, statuses):
        self.db = db
        self.statuses = statuses
        self.command_matcher = {
            'рассчитать статистику': self.calc_and_print_statistics_by_patients_groups,
            'узнать статус пациента': self.ask_and_print_patient_status,
            'повысить статус пациента': self.raise_patient_status,
            'понизить статус пациента': self.reduce_patient_status,
            'стоп': self.stop_dialog,
        }

    def raise_patient_status(self):
        # повысить статус пациент
        index = self.ask_for_index()
        new_user_status = self.db.get_patient_by_index(index) + 1
        if new_user_status == len(self.statuses):
            if self.ask_about_discharge_from_hostpital():
                self.db.delete_patient(index)
        else:
            self.db.update_patient_status(index, new_user_status)
            self.print_new_status(new_user_status)

    def reduce_patient_status(self):
        # понизить статус пациента
        index = self.ask_for_index()
        new_user_status = self.db.get_patient_by_index(index) - 1
        if new_user_status < min(self.statuses.keys()):
            self.print_that_reduce_is_unable()
        else:
            self.db.update_patient_status(index, new_user_status)
            self.print_new_status(new_user_status)

    def ask_about_discharge_from_hostpital(self):
        # отоборазить текст о возможной выписке и спросить о ней
        self.print_what_patient_can_be_discharged()
        return self.ask_yes_or_no()

    def get_method_matched_with_commands_dict(self, command):
        # получить команду сопаставив текст из терминала с словарем команд
        #  Можно расписать более сложную логику
        return self.command_matcher.get(command)

    def start_dialog_with_user(self):
        # начать диалог с пользователем
        while True:
            command = input("Введите команду: ")
            is_matched = self.get_method_matched_with_commands_dict(command)
            if is_matched:
                is_matched()
            else:
                self.print_error()

    def calc_and_print_statistics_by_patients_groups(self):
        # рассчитать статистику по группам пациентов и отобразить её
        total_text = f'В больнице на данный момент находится ' \
                     f'{self.db.get_total_patients_count()} , из них:\n'
        stat_with_zeros = {
            k: self.db.get_patients_count_by_status(k)
            for k in self.statuses.keys()
        }
        filtred = {k: v for k, v in stat_with_zeros.items() if v != 0}

        statistics_text = [
            f' - в статусе "{self.statuses[k]}": {v} чел.'
            for k, v in filtred.items()]

        print(total_text + '\n'.join(statistics_text))

    def ask_and_print_patient_status(self):
        # получить и отобразить статус пациента
        index = self.ask_for_index()
        user_status = self.db.get_patient_by_index(index)
        print(self.statuses[user_status])

    def ask_for_index(self, text=GET_ID_TEXT):
        # спросить у пользователя ID пациента
        index = input(text)
        return int(index)

    def ask_yes_or_no(self):
        # спросить у пользователя да или нет
        voice = input('(да/нет) ')
        if 'да' in voice:
            return True
        if 'нет' in voice:
            return False

    def print_what_reduce_is_unable(self):
        # отобразить текст о невозможности понижения статуса пациента
        print(
            'У этого пациента самый низкий статус "Тяжело болен".\n'
            'Статус пациента не изменился, т.к. в нашей больнице '
            'пациенты не умирают!\n'
        )

    def print_what_patient_can_be_discharged(self):
        # отобразить текст о возможной выписке пациента
        print(
            'У этого пациента самый высокий статус "Готов к выписке".\n'
            'Желаете ли выписать этого пациента?'
        )

    def print_new_status(self, status=''):
        # отобразить новый статус пациента
        print(f'Новый статус пациента: "{self.statuses[status]}"')

    def stop_dialog(self):
        # отстановить диалог с пользователем
        print('Сеанс завершён.')
        exit(0)

    def print_error(self):
        # отобразить ошибку о неизвестной команде
        print('Неизвестная команда! Попробуйте ещё раз')


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
        return self.db[patient_index]

    def update_patient_status(self, patient_index: int, new_status: int):
        # записать новый статус пациента
        self.db[patient_index] = new_status

    def delete_patient(self, patient_index: int):
        # удалить пациента
        self.db.pop(patient_index)


if __name__ == '__main__':
    init_args = parse_script_args()
    statuses = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке',
    }
    hospital = HospitalListDB([1] * 200)
    dlg = Application(hospital, statuses)
    dlg.start_dialog_with_user()
