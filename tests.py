import unittest

import requests

class RequestSender:
    def sendRequestWithParams(self, url, params):
        raise NotImplementedError()

class FakeRequestSender(RequestSender):
    def sendRequestWithParams(self, url, params):
        self.url = url
        self.params = params

class RealRequestSender(RequestSender):
    def sendRequestWithParams(self, url, params):
        return requests.get(url, params = params)

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

    def sendRequest(self, request_name, parameters):
        vk_request = self._api_url + request_name
        parameters['access_token'] = self._app_token

        return self._request_sender.\
            sendRequestWithParams(vk_request, 
                                     parameters)

class VK_Group():
    def __init__(self, group_id, vk_connector):
        self._group_id = group_id
        self._connector = vk_connector
        self._request_params = {'owner_id': group_id}

    def getLastWallRecords(self, records_count):
        requestRecordParams = self._request_params
        requestRecordParams['count'] = records_count

        return self._connector.\
                     sendRequest('method/wall.get',
                                requestRecordParams)

class VK_API_Tester(unittest.TestCase):
    def setUp(self):
        self.test_sender = FakeRequestSender()
        self.test_url = 'https://test.vk.api.com/'
        self.test_token = 'test_token'

        self.test_connector = VK_APIConnector(
                                    self.test_url,
                                    self.test_token,
                                    self.test_sender)

    def test_VKConnectorTokenSet(self):
        test_method = 'method/wall.get'
        test_params = {'a': 1, 'b': 2}

        self.test_connector.sendRequest(test_method,
                                           test_params)

        self.assertEqual(self.test_sender.url,
                         self.test_url + test_method)

        self.assertEqual(
                self.test_sender.params['access_token'],
                self.test_token)

    def test_GroupGetWallRecords(self):
        test_group = VK_Group('test_id', 
                              self.test_connector)

        test_group.getLastWallRecords(2)

        self.assertEqual(self.test_sender.url,
                     self.test_url + 'method/wall.get')
        self.assertEqual(
                self.test_sender.params['owner_id'],
                'test_id')

        self.assertEqual(
                self.test_sender.params['count'], 2)

if __name__ == '__main__':
    unittest.main()
