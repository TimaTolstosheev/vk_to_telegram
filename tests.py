import unittest

import requests

class RequestSender:
    def sendRequestWithParams(self, url, params):
        raise NotImplementedError()
    def receiveRequestWithParams(self, url, params):
        raise NotImplementedError()

class FakeRequestSender(RequestSender):
    def sendRequestWithParams(self, url, params):
        self.url = url
        self.params = params

    def receiveRequestWithParams(self, url, params):
        self.url = url
        self.params = params

class RealRequestSender(RequestSender):
    def sendRequestWithParams(self, url, params):
        return requests.get(url, params = params)

    def receiveRequestWithParams(self, url, parameters):
        return requests.get(url, params=parameters).text

class APIConnector:
    def __init__(self, api_url, app_token,
                 request_sender = RealRequestSender):
        self._api_url = api_url
        self._app_token = app_token
        self._request_sender = request_sender

class VK_APIConnector(APIConnector):
    def __init__(self, api_url, app_token,
                 request_sender = RealRequestSender):
        super().__init__(api_url, app_token, 
                         request_sender)

    def receiveRequest(self, request_name, parameters):
        vk_request = self._api_url + request_name
        parameters['access_token'] = self._app_token

        return self._request_sender.\
            receiveRequestWithParams(vk_request, 
                                     parameters)


class VK_API_Tester(unittest.TestCase):
    def test_ReceiveRequest(self):
        test_sender = FakeRequestSender()
        test_url = 'https://test.vk.api.com/'
        test_token = 'test_token'
        test_method = 'method/wall.get'
        test_params = {'a': 1, 'b': 2}
        test_connector = VK_APIConnector(
                        test_url,
                        test_token,
                        test_sender)

        test_connector.receiveRequest(test_method,
                                      test_params)

        self.assertEqual(test_sender.url,
                        test_url + test_method)

        self.assertEqual(
                test_sender.params['access_token'],
                test_token)

if __name__ == '__main__':
    unittest.main()
