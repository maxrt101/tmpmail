from urllib.parse import urljoin, urlparse
from typing import Optional, Iterable
import requests
import os

from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


class EMailinatorClient(MailClient):
    __NAME__ = 'emailnator.com'
    __API_BASE__ = 'https://gmailnator.p.rapidapi.com/api/'
    __TYPES__ = ['public_email_domain', 'public_gmail_plus', 'public_gmail_dot', 'public_googlemail', 'private_email_domain', 'private_gmail_plus', 'private_gmail_dot', 'private_googlemail']
    __EXCLUDE__ = 'RAPID_API_KEY' not in os.environ

    @staticmethod
    def _headers():
        return {
            'x-rapidapi-host': urlparse(EMailinatorClient.__API_BASE__).netloc,
            'x-rapidapi-key':  os.environ['RAPID_API_KEY'],
        }

    class Letter(Letter):
        def __init__(self, data: dict, proxies: Optional[dict] = None):
            super().__init__(
                sender=Sender.parse(data['from']),
                subject=data['subject']
            )
            self.proxies = proxies
            self.id = data['id']

        @property
        def body(self) -> str:
            response = requests.get(
                url=urljoin(EMailinatorClient.__API_BASE__, f'inbox/{self.id}'),
                headers=EMailinatorClient._headers(),
                proxies=self.proxies
            )

            RequestFailedError.check_raise(response, 'Failed to get emailnator.com letter body')

            return response.json()['content']

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None, types: Iterable[str] = ('private_gmail_plus', 'private_gmail_dot')):
        self.types = types
        super().__init__(address, proxies)

    def inbox(self) -> list[Letter]:
        response = requests.post(
            url=urljoin(self.__API_BASE__, 'inbox'),
            headers=self._headers(),
            json={'email': self.address}, # TODO: increase limit (default=10, max=20)
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get emailnator.com emails')

        return [self.Letter(x, self.proxies) for x in response.json()['messages']]

    def generate_address(self):
        response = requests.post(
            url=urljoin(self.__API_BASE__, 'emails/generate'),
            headers=self._headers(),
            json={
                'type': self.types
            },
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get emailnator.com emails')

        return response.json()['email']
