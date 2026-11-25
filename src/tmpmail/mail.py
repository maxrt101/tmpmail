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
