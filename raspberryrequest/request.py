import requests
from typing import Dict


def make_request(
    base_url: str,
    method: str,
    headers: Dict[str, str],
    params: Dict[str, str],
    session: requests.Session
) -> requests.Response:
    """
    Sends a request to the specified URL using the provided
    method, headers, parameters, and session.

    - :param `base_url`: The base URL of the request.
    - :type `base_url`: `str`
    - :param `method`: The HTTP method to be used for the
        request.
    - :type `method`: `str`
    - :param `headers`: The headers to be included in the request.
    - :type `headers`: Dict[`str`, `str`]
    - :param `params`: The parameters to be included in the request.
    - :type `params`: Dict[`str`, `str`]
    - :param `session`: The session to be used for the request.
    - :type `session`: `requests.Session`
    - :return: The response object returned by the request.
    - :rtype: `requests.Response`
    """
    request = requests.Request(method=method, url=base_url,
                               headers=headers, params=params)
    prepared_request = session.prepare_request(request)
    response = session.send(request=prepared_request)
    return response
