from typing import Optional
import email.policy
import email

from tmpmail.data import Sender


class Letter:
    def __init__(self, *, sender: Optional[Sender] = None, subject: Optional[str] = None, body: Optional[str] = None):
        if sender: self.sender_ = sender
        if subject: self.subject_ = subject
        if body: self.body_ = body

    def __str__(self) -> str:
        return f'<Letter from="{self.sender}" subject="{self.subject}">'

    def __repr__(self) -> str:
        return f'<Letter from="{self.sender}" subject="{self.subject}">'

    @property
    def sender(self) -> Sender:
        return self.sender_

    @property
    def subject(self) -> str:
        return self.subject_

    @property
    def body(self) -> str:
        return self.body_

    @classmethod
    def from_eml(cls, file):
        msg = email.parser.BytesParser(policy=email.policy.default).parse(file)

        if body := msg.get_body(preferencelist=("html", "plain")):
            content = body.get_content()
        else:
            content = ''

        return cls(
            sender=Sender.parse(msg['from']),
            subject=msg['subject'],
            body=content
        )
