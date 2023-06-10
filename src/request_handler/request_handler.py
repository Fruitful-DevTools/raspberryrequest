import requests
from requests.models import Response
import json
from typing import Dict
from requests.exceptions import HTTPError
from request_handler import log


import time

class APIRequester:
    MAX_RETRIES = 5
    MAX_WAIT_TIME = 120  # Maximum wait time in seconds

    def __init__(self, base_url: str, headers: dict[str, str], endpoint: str = ''):
        self.url = str(base_url + endpoint)
        self.headers = headers

    def run(self, params: dict[str, str], url_substring: str = '') -> Dict[str, str]:
        request_url = self.url + url_substring
        response = self._request_api(request_url, params)
        response_dict = json.loads(response.text)
        return response_dict

    def _request_api(self, request_url, params):
        log.info('Sending request to API...')
        attempt = 1
        while attempt <= self.MAX_RETRIES:
            try:
                response: Response = requests.get(request_url, params=params, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    log.info('Response is valid')
                    return response
                elif response.status_code == 201:
                    log.info('The request was successful, and a new resource was created as a result.')
                    return response
                elif response.status_code == 400:
                    raise HTTPError('400 Bad Request: The server cannot process the request due to client error, such as invalid input or malformed request syntax.')
                elif response.status_code == 401:
                    raise HTTPError('401 Unauthorized: The request requires authentication, and the client needs to provide valid credentials.')
                elif response.status_code == 403:
                    raise HTTPError('403 Forbidden: The server understood the request but refuses to authorize it. The client does not have permission to access the requested resource.')
                elif response.status_code == 404:
                    raise HTTPError('404 Not Found: The requested resource could not be found on the server.')
                elif response.status_code == 429:
                    raise HTTPError('429 Requests Error: Maximum number of requests exceeded.')
                elif response.status_code == 500:
                    raise HTTPError('500 Not Found: The requested resource could not be found on the server.')
                else:
                    raise HTTPError('Unknown error encountered: %s', response.status_code)
            except HTTPError as e:
                log.error(e)
                log.info('Retrying...')
                if attempt < self.MAX_RETRIES:
                    delay = min(2 ** attempt * 1000, self.MAX_WAIT_TIME * 1000)  # Exponential backoff with maximum wait time
                    time.sleep(delay / 1000)  # Convert delay to seconds
                attempt += 1
