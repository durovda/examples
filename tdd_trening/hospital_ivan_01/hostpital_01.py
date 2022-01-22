import argparse


def parse_script_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db",
                        help="Путь к файлу с БД больницы")
    parser.add_argument("--statuses",
                        help="Используемые настройки скриптов")
    args = parser.parse_args()
    return args


class Dialog:
    def __init__(self, db, statuses):
        self.db = db
        self.statuses = statuses

    def raise_user_status(self):
        index = self.ask_for_index()
        new_user_status = self.db.get_user_by_index(index) + 1
        if new_user_status > len(self.statuses):
            if self.release_from_hostpital():
                self.db.delete_user(index)
        else:
            self.db.update_user_status(index, new_user_status)

    def reduce_user_status(self):
        index = self.ask_for_index()  #
        new_user_status = self.db.get_user_by_index(index) - 1
        if new_user_status < len(self.statuses):
            self.reduce_unable()
        else:
            self.db.update_user_status(index, new_user_status)

    def release_from_hostpital(self):
        self.possible_healthy_patient()
        return self.ask_yes_or_no()

    def ask_for_index(self):
        pass

    def ask_yes_or_no(self):
        pass

    def reduce_unable(self):
        pass

    def possible_healthy_patient(self):
        pass


class ConsoleDialog(Dialog):
    def __init__(self, db, statuses):
        super().__init__(db, statuses)
        self.command_matcher = {
            'stat': self.print_statistics,
            'get_id': self.print_user_status
        }

    def match_command(self, command):
        #  Можно расписать более сложную логику
        return self.command_matcher.get(command)

    def run(self):
        while True:
            command = input("Подключение\n")
            is_matched = self.match_command(command)
            if is_matched:
                is_matched()

    def print_statistics(self):
        stats = self.db.get_stat()
        print(stats)

    def print_user_status(self):
        index = self.ask_for_index()
        user_status = self.db.get_user_by_index(index)
        print(self.statuses[user_status])

    def ask_for_index(self, text=None):
        return int(input(text))

    def ask_yes_or_no(self):
        voice = input('yes or no')
        if 'yes' in voice:
            return True
        if 'no' in voice:
            return False

    def reduce_unable(self):
        print('Ниже некуда')

    def possible_healthy_patient(self):
        print('Тут можно выписать человечка')


class HospitalListDB:
    def __init__(self, db):
        self.db = db

    def get_statistics(self):
        return 0

    def get_user_by_index(self, user_index):
        return self.db[user_index]

    def update_user_status(self, user_index, new_status):
        self.db[user_index] = new_status

    def delete_user(self, user_index):
        self.db.pop(user_index)


if __name__ == '__main__':
    init_args = parse_script_args()
    statuses = {''}
    hospital = HospitalListDB([])
    dlg = ConsoleDialog(hospital, statuses)
    dlg.run()
