

class InputMessages:
    def __init__(self):
        self._messages = []
        self._current_index = 0

    def add(self, question, answer):
        self._messages.append((question, answer))

    def get(self):
        current_message = self._messages[self._current_index]
        self._current_index += 1
        return current_message[0], current_message[1]


class OutputMessages:
    def __init__(self):
        self._messages = []
        self._current_index = 0

    def add(self, expected_message):
        self._messages.append(expected_message)

    def get(self):
        current_expected_message = self._messages[self._current_index]
        self._current_index += 1
        return current_expected_message


class MockInputStream:
    def __init__(self):
        self._messages = InputMessages()

    def input(self, question):
        current_message = self._messages.get()
        assert question == current_message[0], f'\nactual_question = "{question}"' \
                                               f'\nexpected_question = "{current_message[0]}"'
        return current_message[1]

    def add_expected_answer(self, question, answer):
        self._messages.add(question, answer)


class MockOutputStream:
    def __init__(self):
        self._expected_messages = OutputMessages()

    def print(self, message):
        current_expected_message = self._expected_messages.get()
        assert message == current_expected_message, f'\nactual_message = "{message}"' \
                                                    f'\nexpected_message = "{current_expected_message}"'

    def add_expected_message(self, expected_message):
        self._expected_messages.add(expected_message)
