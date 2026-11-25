from tmpmail.mail import MailClient


def excluded(sub_cls: type[MailClient]) -> bool:
    if getattr(sub_cls, '__EXCLUDE__', False):
        return True

    if f := getattr(sub_cls, '__EXCLUDE_IF__', None):
        return f()

    return False


def get_provider_class(provider: str) -> type[MailClient]:
    for sub_cls in MailClient.__subclasses__():
        if sub_cls.__NAME__ == provider and not excluded(sub_cls):
            return sub_cls
    raise ValueError(f'Invalid provider: {provider}. Available providers: {[x.__NAME__ for x in MailClient.__subclasses__()]}')

