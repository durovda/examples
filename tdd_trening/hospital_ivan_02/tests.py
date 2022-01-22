import unittest
from tdd_trening.hospital_ivan_02.hostpital import Application, HospitalListDB


def extended_fake_inputs(chain):
    def inner(text):
        return chain.pop()
    return inner


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.statuses = {
            0: 'Тяжело болен',
            1: 'Болен',
            2: 'Слегка болен',
            3: 'Готов к выписке',
        }
        self.initiate_status = 1
        self.database = HospitalListDB([self.initiate_status] * 200)
        self.app = Application(self.database, self.statuses)
        self.fake_input_text = ''
        self.fake_input_chain = ['']
        self.app._input_method = lambda x: self.fake_input_text
        self.app._print_method = lambda x: x

    def test_patients_status_change(self):
        user_inputs = [1, 1, 1, 1, 'да']
        self.app._input_method = extended_fake_inputs(user_inputs[::-1])
        get_patient_status = self.app.\
            _get_method_matched_with_commands_dict('узнать статус пациента')
        # self.fake_input_text = 1
        current_patient_status = get_patient_status()
        self.assertEqual(current_patient_status, 'Болен')
        raise_patient_status = self.app.\
            _get_method_matched_with_commands_dict('повысить статус пациента')
        raised_patient_status = raise_patient_status()
        print(raised_patient_status)
        self.assertTrue('Слегка болен' in raised_patient_status)
        raised_patient_status = raise_patient_status()
        self.assertTrue('Готов к выписке' in raised_patient_status)

        # reduce_patient_status = self.app.\
        #     _get_method_matched_with_commands_dict('понизить статус пациента')
        # reduce_patient_status()

        # stop = self.app.\
        #     _get_method_matched_with_commands_dict('стоп')
        # stop()
        #
        # calc_stat = self.app.\
        #     _get_method_matched_with_commands_dict('рассчитать статистику')
        # calc_stat()

        raised_patient_status = raise_patient_status()
        # self.assertTrue('Готов к выписке' in raised_patient_status)

    def test_app(self):
        user_inputs = [
            'повысить статус пациента', 4,
            'повысить статус пациента', 4,
            'повысить статус пациента', 4,
            'да',
            'повысить статус пациента', 4,
            'повысить статус пациента', 4,
            'повысить статус пациента', 4,
            'нет',
            'понизить статус пациента', 6,
            'понизить статус пациента', 6,
            'понизить статус пациента', 6,
            'узнать статус пациента', 2001,
            'asdsdsdsd', 'рассчитать статистику',
            'стоп']
        self.app._input_method = extended_fake_inputs(user_inputs[::-1])
        self.app.start_dialog_with_user()
        self.app.start_dialog_with_user()


if __name__ == '__main__':
    unittest.main()
