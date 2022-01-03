

class MockInputStream:
    def __init__(self, expected_messages):
        self._expected_messages = expected_messages
        self._current_index = 0

    def get_message(self, question):
        current_message = self._expected_messages[self._current_index]
        self._current_index += 1
        return current_message


class MockOutputStream:
    def __init__(self):
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)
