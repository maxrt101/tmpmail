from urllib.parse import urljoin
from typing import Optional
import requests


from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


# DOESNT WORK - Cloudflare blocks requests
class TempMailOrgScrapperClient(MailClient):
    __EXCLUDE__ = True

    __NAME__ = 'temp-mail.org_scrap'
    __API_BASE__ = 'https://web2.temp-mail.org/'

    class Letter(Letter):
        def __init__(self, data: dict):
            super().__init__(
                sender=Sender.parse(data['from']),
                subject=data['subject'],
                body=data['bodyPreview']
            )

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        import cloudscrapper
        self.scrapper = cloudscraper.create_scraper(delay=10, browser='chrome')
        self.token = None
        super().__init__(address, proxies)

    def inbox(self) -> list[Letter]:
        response = requests.get(
            url=urljoin(self.__API_BASE__, 'messages'),
            headers={'Authorization': f'Bearer {self.token}'},
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to get inbox from temp-mail.org')

        return [self.Letter(x) for x in response.json().get('messages', [])]

    def generate_address(self) -> str:
        response = requests.post(
            url=urljoin(self.__API_BASE__, 'mailbox'),
            proxies=self.proxies
        )

        RequestFailedError.check_raise(response, 'Failed to create mailbox for temp-mail.org')

        data = response.json()
        self.token = data['token']
        return data['mailbox']
