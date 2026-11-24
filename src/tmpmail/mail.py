from abc import ABC, abstractmethod
from typing import Optional
import random
import string

from tmpmail.letter import Letter


class MailClient(ABC):
    __NAME__: str

    def __init__(self, address: Optional[str] = None, proxies: Optional[dict] = None):
        self.proxies = proxies
        self.address = address or self.generate_address()

    @abstractmethod
    def inbox(self) -> list[Letter]:
        ...

    @abstractmethod
    def generate_address(self) -> str:
        ...

    def generate_username(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))


def select_provider(name: str):
    for sub_cls in MailClient.__subclasses__():
        if sub_cls.__NAME__ == name and not getattr(sub_cls, '__EXCLUDE__', False):
            return sub_cls
    raise ValueError(f'Invalid provider: {name}. Available providers: {[x.__NAME__ for x in MailClient.__subclasses__()]}')
