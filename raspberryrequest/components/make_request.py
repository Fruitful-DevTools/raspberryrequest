import requests
from typing import Literal, Dict


def make_request(
        base_url: str,
        method: Literal['GET', 'POST'],
        headers: Dict[str, str],
        params: Dict[str, str],
        data: Dict[str, str], session) -> requests.Response:

    if method == 'GET':
        return session.get(base_url, headers=headers, params=params)
    elif method == 'POST':
        return session.post(base_url, headers=headers, params=params, json=data)
    else:
        raise ValueError(f'Invalid HTTP method: {method}')
