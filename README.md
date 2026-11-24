# tmpmail

A single interface for working with temporary email services.

### How to install
```commandline
pip install pytmpmail
```

### Example

```python
import tmpmail

mail = tmpmail.DefaultClient() # Or RandomClient, or any of the supported clients directly

for letter in mail.inbox():
    print(f'A letter "{letter.subject}" from {letter.sender}:\n{letter.body}')
```

To test locally, use `tmpmail.InteractiveMockMailClient`, it will prompt you for an address and then for a path to `.eml` file on each `.inbox()` call.

### Supported providers

| URL | Class | Needs API Key? | Details |
| :--- | :--- | :---: | :--- |
| none(local) | InteractiveMockMailClient | No | Prompts the user in commandline |
| https://emailnator.com | EMailinatorClient | Yes | Go to https://rapidapi.com/johndevz/api/gmailnator for API key |
| https://inboxkitten.com | InboxkittenClient | No | Has public mailboxes |
| https://tempmail.lol | TempMailLolClient | No | |
| https://temp-mail.org | TempMailOrgClient | Yes | Go to https://rapidapi.com/Privatix/api/temp-mail for API key |
| https://temp-mail.org | TempMailOrgScrapperClient | No | DOESN'T WORK & requires additional package - cloudscrapper |
| https://tempmail.plus | TempMailPlusClient | No | |

### Architecture

There are 2 half-abstract base classes: `MailClient` & `Letter`.  
Each of the providers subclass the `MailClient` and implement their own `Letter` if needed.  
Each `MailClient` receives 2 arguments in `__init__`: `address` & `proxies`:  
 - `address` can be specified to use a pre-determined address for the client, otherwise a random one will be generated based on available provider's domains. Some clients (like `tempmail.lol`) don't support specifying an address and can only use a random generated one.  
 - `proxies` are a standardized dictionary fed to `requests` module, which may include `http`, `https` & `socks5` entries.  

Each client has an `inbox()` method, which returns a list of `Letter` subclasses, in order they arrived to the client.  

There are no webhooks, or background polling for now: each `inbox()` call polls the server once.  

Each `Letter` has 3 required properties: `sender`, `subject` and `body`.  
Based on provider's architecture, this properties may make another API request to retrieve the data, if inbox doesn't provide it (many providers return only sender & subject, with body being retrieved through a separate request).  

The only requirement is `requests` module, and the only exceptions specifically raised are:  
 - `RequestFailedError` on any failed request; contains raw response.  
 - `ValueError` when invalid default provider was selected via env.  
 - `NotImplementedError` when trying to specify address for `TempMailLolClient`.  

For testing, there is a `tmpmail.test.send_email` function, which uses https://maileroo.com service to send test mails.  

### Environment Variables

Currently only `TempMailOrgClient` requires an API key, and it expects it to be in `RAPID_API_KEY` env variable.  

For `tmpmail.test.send_email` (which uses https://maileroo.com) to work, maileroo api key and address is needed, it's expected to be in `MAILEROO_API_KEY` & `MAILEROO_ADDRESS` variables.  

There is also an optional `TMPMAIL_PROVIDER` variable, which overrides to which class `DefautProvider` points too. Provider names can be looked up in each provider class under `__NAME__` static field.
