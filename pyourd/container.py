import requests
import json


class OurdException(Exception):
    def __init__(self, message, error_type=None, code=None):
        self.error_type = error_type or 'UnknownError'
        self.message = message
        self.code = code
        super(OurdException, self).__init__(message)

    @classmethod
    def from_dict(cls, error_dict):
        error_type = error_dict.get('type', 'UnknownError')
        message = error_dict.get('message', None)
        code = error_dict.get('code', None)
        return cls(message, error_type, code)


def send_action(url, payload):
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

    return requests.post(url, data=json.dumps(payload), headers=headers).json()


class OurdContainer(object):
    endpoint = 'http://localhost:3000'
    api_key = None
    access_token = None

    def __init__(self, endpoint=None, api_key=None, access_token=None):
        if endpoint:
            self.endpoint = endpoint
        if api_key:
            self.api_key = api_key
        self.access_token = access_token

    def _request_url(self, action_name):
        endpoint = self.endpoint
        endpoint = endpoint[:-1] if endpoint[-1] == '/' else endpoint
        return endpoint + '/' + action_name.replace(':', '/')

    def _payload(self, action_name, params):
        payload = params.copy() if isinstance(params, dict) else {}
        payload['action'] = action_name
        if self.access_token:
            payload['access_token'] = self.access_token
        elif self.api_key:
            payload['api_key'] = self.api_key
        return payload

    @classmethod
    def set_default_endpoint(cls, endpoint):
        cls.endpoint = endpoint

    @classmethod
    def set_default_apikey(cls, api_key):
        cls.api_key = api_key

    def send_action(self, action_name, params):
        resp = send_action(self._request_url(action_name),
                           self._payload(action_name, params))
        if 'error' in resp:
            raise OurdException.from_dict(resp['error'])