class MockConsole:
    def __init__(self):
        self._list_of_expected_requests_and_responses = []
        self._expected_messages = []

    def input(self, request):
        expected_request, expected_response = self._get_current_request_and_response()
        assert request == expected_request, f'\nactual_request = "{request}"' \
                                            f'\nexpected_request = "{expected_request}"'
        return expected_response

    def print(self, message):
        expected_message = self._get_current_expected_message()
        assert message == expected_message, f'\nactual_output_message = "{message}"' \
                                            f'\nexpected_output_message = "{expected_message}"'

    def add_expected_request_and_response(self, request, response):
        self._list_of_expected_requests_and_responses.append((request, response))

    def add_expected_output_message(self, expected_message):
        self._expected_messages.append(expected_message)

    def _get_current_request_and_response(self):
        request_and_response = self._list_of_expected_requests_and_responses.pop(0)
        return request_and_response[0], request_and_response[1]

    def _get_current_expected_message(self):
        return self._expected_messages.pop(0)

