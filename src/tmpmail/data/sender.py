from dataclasses import dataclass
import email


@dataclass
class Sender:
    address: str
    name: str

    def __str__(self) -> str:
        return f'{self.name} <{self.address}>'

    @classmethod
    def parse(cls, sender: str):
        name, address = email.utils.parseaddr(sender)
        return cls(address, name)
