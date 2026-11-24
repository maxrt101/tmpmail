from urllib.parse import urljoin
from typing import Optional
import requests
import random

from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


class TempMailPlusClient(MailClient):
    __NAME__ = 'tempmail.plus'
    __API_BASE__ = 'https://tempmail.plus/api/'

    DOMAINS = [
        'mailto.plus',
        'fexpost.com',
        'fexbox.org',
        'mailbox.in.ua',
        'rover.info',
        'fextemp.com',
        'any.pink',
        'merepost.com'
    ]

    class Letter(Letter):
        def __init__(self, data: dict, address: str, proxies: Optional[dict] = None):
            super().__init__(
                sender=Sender(data['from_mail'], data['from_name']),
                subject=data['subject']
            )
            self.address = address
            self.proxies = proxies
            self.id = data['mail_id']

        @property
        def body(self) -> str:
            response = requests.get(
                url=urljoin(TempMailPlusClient.__API_BASE__, f'mails/{self.id}'),
                params={'email': self.address},
                proxies=self.proxies
            )

            RequestFailedError.check_raise(response, 'Failed to get tempmail.plus letter body')

            return response.json()['text']

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        super().__init__(address, proxies)

    def inbox(self) -> list[Letter]:
        response = requests.get(
            url=urljoin(self.__API_BASE__, 'mails'),
            params={'email': self.address}, # TODO: &limit={>10}
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get tempmail.plus emails')

        return [self.Letter(x, self.address, self.proxies) for x in response.json()['mail_list']]

    def generate_address(self):
        return f'{self.generate_username()}@{random.choice(self.DOMAINS)}'
