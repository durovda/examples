from model.db import HospitalListDB
from model.application import Application

if __name__ == '__main__':
    statuses = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке',
    }
    hospital = HospitalListDB([1] * 200)
    dlg = Application(hospital, statuses)
    dlg.start_dialog_with_user()
