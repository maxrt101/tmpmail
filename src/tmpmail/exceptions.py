from typing import Optional
import requests


class RequestFailedError(Exception):
    def __init__(self, msg: str, response: requests.Response):
        super().__init__(f'{msg}: {response.status_code} {response.text}')
        self.res = response

    @classmethod
    def check_raise(cls, response: requests.Response, msg: Optional[str] = None):
        if response.status_code != 200:
            raise cls(msg or f'Failed a request to {response.url}', response)
