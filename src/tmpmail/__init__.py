import os
import random

from tmpmail.data import Sender
from tmpmail.letter import Letter
from tmpmail.mail import MailClient, select_provider

from tmpmail.exceptions import RequestFailedError

from tmpmail.providers import (
    EMailinatorClient,
    InboxkittenClient,
    InteractiveMockMailClient,
    TempMailLolClient,
    TempMailOrgClient,
    TempMailOrgScrapperClient,
    TempMailPlusClient
)

import tmpmail.test

DefaultClient = select_provider(os.environ['TMPMAIL_PROVIDER']) if 'TMPMAIL_PROVIDER' in os.environ else InboxkittenClient
RandomClient = random.choice([x for x in MailClient.__subclasses__() if not getattr(x, '__EXCLUDE__', False)])
