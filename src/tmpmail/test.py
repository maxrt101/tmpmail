from typing import Optional
import requests
import os


def send_email(
        *,
        to: str,
        from_user_name: str = 'test',
        from_display_name: str = 'Test',
        subject: str = 'Test',
        body: str = 'Test Body.',
        proxies: Optional[dict] = None
):
    return requests.post(
        url='https://smtp.maileroo.com/api/v2/emails',
        headers={
            'Authorization': f'Bearer {os.environ['MAILEROO_API_KEY']}',
            'Content-Type': 'application/json',
        },
        json={
            'from': {
                'address': f'{from_user_name}@{os.environ['MAILEROO_ADDRESS']}',
                'display_name': from_display_name
            },
            'to': {
                'address': to
            },
            'subject': subject,
            'plain': body,
        },
        proxies=proxies
    )
