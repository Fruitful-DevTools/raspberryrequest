import requests
from requests import RequestException, Session, Request
from typing import Literal, Dict


def make_request(
        base_url: str,
        method: Literal['GET', 'POST'],
        headers: Dict[str, str],
        params: Dict[str, str],
        session: Session) -> requests.Response:
    try:
        request = Request(method=method, url=base_url,
                          headers=headers, params=params)
        prepared_request = session.prepare_request(request)
        response = session.send(request=prepared_request)
        return response
    except RequestException as e:
        raise e
