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
            'рассчитать статистику': self.print_statistics,
            'узнать статус пациента': self.print_user_status,
            'повысить статус пациента': self.raise_user_status,
            'понизить статус пациента': self.reduce_user_status,
            'стоп': self.stop_console,
        }

    def raise_user_status(self):
        index = self.ask_for_index()
        new_user_status = self.db.get_user_by_index(index) + 1
        if new_user_status == len(self.statuses):
            if self.release_from_hostpital():
                self.db.delete_user(index)
        else:
            self.db.update_user_status(index, new_user_status)
            self.display_new_status(new_user_status)

    def reduce_user_status(self):
        index = self.ask_for_index()
        new_user_status = self.db.get_user_by_index(index) - 1
        if new_user_status < min(self.statuses.keys()):
            self.reduce_unable()
        else:
            self.db.update_user_status(index, new_user_status)
            self.display_new_status(new_user_status)

    def release_from_hostpital(self):
        self.possible_healthy_patient()
        return self.ask_yes_or_no()

    def match_command(self, command):
        #  Можно расписать более сложную логику
        return self.command_matcher.get(command)

    def run(self):
        while True:
            command = input("Введите команду: ")
            is_matched = self.match_command(command)
            if is_matched:
                is_matched()
            else:
                self.display_error()

    def print_statistics(self):
        total_text = f'В больнице на данный момент находится ' \
                     f'{self.db.get_total()} , из них:\n'
        stat_with_zeros = {
            k: self.db.get_count_by_status(k)
            for k in self.statuses.keys()
        }
        filtred = {k: v for k, v in stat_with_zeros.items() if v != 0}

        statistics_text = [
            f' - в статусе "{self.statuses[k]}": {v} чел.'
            for k, v in filtred.items()]

        print(total_text + '\n'.join(statistics_text))

    def print_user_status(self):
        index = self.ask_for_index()
        user_status = self.db.get_user_by_index(index)
        print(self.statuses[user_status])

    def ask_for_index(self, text=GET_ID_TEXT):
        index = input(text)
        return int(index)

    def ask_yes_or_no(self):
        voice = input('(да/нет) ')
        if 'да' in voice:
            return True
        if 'нет' in voice:
            return False

    def reduce_unable(self):
        print(
            'У этого пациента самый низкий статус "Тяжело болен".\n'
            'Статус пациента не изменился, т.к. в нашей больнице '
            'пациенты не умирают!\n'
        )

    def possible_healthy_patient(self):
        print(
            'У этого пациента самый высокий статус "Готов к выписке".\n'
            'Желаете ли выписать этого пациента?'
        )

    def display_new_status(self, status=''):
        print(f'Новый статус пациента: "{self.statuses[status]}"')

    def stop_console(self):
        print('Сеанс завершён.')
        exit(0)

    def display_error(self):
        print('Неизвестная команда! Попробуйте ещё раз')


class HospitalListDB:
    def __init__(self, db):
        self.db = db

    def get_count_by_status(self, status: int):
        """
        Получить число пациентов с определенным статусом
        """
        return len(list(filter(
            lambda patient_stat: patient_stat == status, self.db)))

    def get_total(self):
        """
        Получить число пациентов с определенным статусом
        """
        return len(self.db)

    def get_user_by_index(self, user_index: int):
        return self.db[user_index]

    def update_user_status(self, user_index: int, new_status: int):
        self.db[user_index] = new_status

    def delete_user(self, user_index: int):
        self.db.pop(user_index)


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
    dlg.run()
