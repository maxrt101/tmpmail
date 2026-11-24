from urllib.parse import urljoin
from typing import Optional
import requests

from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


class InboxkittenClient(MailClient):
    __NAME__ = 'inboxkitten.com'
    __API_BASE__ = 'https://inboxkitten.com/api/v1/'

    class Letter(Letter):
        def __init__(self, data: dict, proxies: Optional[dict] = None):
            super().__init__(
                sender=Sender.parse(data['message']['headers']['from']),
                subject=data['message']['headers']['subject']
            )
            self.proxies = proxies
            self.id = data['id']
            self.storage_key = data['storage']['key']
            self.storage_region = data['storage']['region']

        @property
        def body(self) -> str:
            response = requests.get(
                url=urljoin(InboxkittenClient.__API_BASE__, 'mail/getHtml'),
                params={'region': self.storage_region, 'key': self.storage_key},
                proxies=self.proxies
            )

            RequestFailedError.check_raise(response, 'Failed to get inboxkitten.com letter body')

            return response.text

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        super().__init__(address, proxies)

    def inbox(self) -> list[Letter]:
        response = requests.get(
            url=urljoin(self.__API_BASE__, 'mail/list'),
            params={'recipient': self.address},
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get inboxkitten.com emails')

        return [self.Letter(x, self.proxies) for x in response.json()]

    def generate_address(self):
        return f'{self.generate_username()}@inboxkitten.com'
