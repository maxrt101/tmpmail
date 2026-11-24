from typing import Optional

from tmpmail.letter import Letter
from tmpmail.mail import MailClient


class InteractiveMockMailClient(MailClient):
    __NAME__ = 'interactive-mock'

    class Letter(Letter):
        def __init__(self, sender, subject, body):
            super().__init__(sender=sender, subject=subject, body=body)

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        super().__init__(address, proxies)
        self.emails = []

    def inbox(self):
        eml_path = input('InteractiveMockMailClient requests inbox, enter path to .eml file: ')

        if eml_path:
            with open(eml_path, 'rb') as f:
                self.emails.append(self.Letter.from_eml(f))

        return self.emails

    def generate_address(self) -> str:
        return input('InteractiveMockMailClient requests an email address: ')
