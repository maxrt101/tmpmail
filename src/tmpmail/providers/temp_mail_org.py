from urllib.parse import urlparse, urljoin
from typing import Optional
from pathlib import Path
from hashlib import md5
import requests
import random
import json
import os

from tmpmail.mail import MailClient
from tmpmail.letter import Letter
from tmpmail.data import Sender
from tmpmail.exceptions import RequestFailedError


class TempMailOrgClient(MailClient):
    __NAME__ = 'temp-mail.org'
    __API_BASE__ = 'https://privatix-temp-mail-v1.p.rapidapi.com'
    __EXCLUDE_IF__ = lambda: 'RAPID_API_KEY' not in os.environ
    __CACHE_FILE__ = Path('.cache/tempmailorg_domains.json')
    __DOMAIN_LIST__ = list()

    class Letter(Letter):
        def __init__(self, data: dict):
            super().__init__(
                sender=Sender.parse(data['mail_from']),
                subject=data['mail_subject'],
                body=data['mail_html'] or data['mail_text']
            )
            self.id = data['mail_id']

    def _get(self, path: str):
        return requests.get(
            url=urljoin(self.__API_BASE__, path),
            headers={
                'x-rapidapi-host': urlparse(self.__API_BASE__).netloc,
                'x-rapidapi-key':  os.environ['RAPID_API_KEY'],
            },
            proxies=self.proxies
        )

    def _domains(self, cache_ttl_s=86400) -> list:
        if not self.__DOMAIN_LIST__:
            self.__CACHE_FILE__.parent.mkdir(parents=True, exist_ok=True)
            self.__CACHE_FILE__.touch()

            with open(self.__CACHE_FILE__, 'r') as f:
                if content := f.read().strip():
                    self.__DOMAIN_LIST__ = json.loads(content)

        if not self.__DOMAIN_LIST__:
            self.__DOMAIN_LIST__ = self._get('request/domains').json()
            print(self.__DOMAIN_LIST__)
            print(type(self.__DOMAIN_LIST__))
            with open(self.__CACHE_FILE__, 'w') as f:
                f.write(json.dumps(self.__DOMAIN_LIST__, indent=4))

        return self.__DOMAIN_LIST__

    @staticmethod
    def _hash(s):
        return md5(s.lower().encode('utf-8')).hexdigest()

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        super().__init__(address, proxies)

    def inbox(self) -> list[Letter]:
        response = self._get(f'request/mail/id/{self._hash(self.address)}')

        RequestFailedError.check_raise(response, 'Failed to get temp-mail.org inbox')

        data = response.json()

        if 'error' in data:
            return []

        return [self.Letter(x) for x in data]

    def generate_address(self):
        username = self.generate_username()
        domain = random.choice(self._domains())
        return f'{username}{domain}'
