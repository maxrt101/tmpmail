import os
import random
from importlib.metadata import version, PackageNotFoundError

from tmpmail.data import Sender
from tmpmail.letter import Letter
from tmpmail.mail import MailClient

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
import tmpmail.utils

try:
    __version__ = version('pytmpmail')
except PackageNotFoundError:
    __version__ = '0.0.0'

DefaultClient = tmpmail.utils.get_provider_class(os.environ['TMPMAIL_PROVIDER']) if 'TMPMAIL_PROVIDER' in os.environ else InboxkittenClient
RandomClient = random.choice([x for x in MailClient.__subclasses__() if not tmpmail.utils.excluded(x)])
