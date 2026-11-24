from urllib.parse import urljoin
from typing import Optional
import requests

from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


class TempMailLolClient(MailClient):
    __NAME__ = 'tempmail.lol'
    __API_BASE__ = 'https://api.tempmail.lol/'

    class Letter(Letter):
        def __init__(self, data: dict):
            super().__init__(
                sender=Sender.parse(data['from']),
                subject=data['subject'],
                body=data['body']
            )
            self.id = data['_id']


    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        if address:
            raise NotImplementedError('Specifying address for tempmail.lol is not supported')

        self.token = None
        super().__init__(proxies=proxies)

    def inbox(self) -> list[Letter]:
        response = requests.get(
            url=urljoin(self.__API_BASE__, f'auth/{self.token}'),
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get tempmail.lol inbox')

        return [self.Letter(x) for x in response.json()['email']]

    def generate_address(self) -> str:
        # TODO: Community? (generate/ruff)
        response = requests.get(
            url=urljoin(self.__API_BASE__, 'generate'),
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to generate tempmail.lol address')

        data = response.json()
        self.token = data['token']
        return data['address']
