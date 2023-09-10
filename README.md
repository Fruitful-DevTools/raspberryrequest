# RaspberryRequest

Py package for making and handling HTTP requests and responses.

**Features**
1. Handling of responses based on response status codes.
2. 
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Usage
### APIRequestHandler

The `APIRequestHandler` class is a utility for sending API requests with retry logic. It provides a convenient way to handle common API request scenarios, such as setting headers, handling retries, and implementing backoff logic.

1. Import the `APIRequestHandler` class:
```
from api_request_handler import APIRequestHandler
```
2. Create an instance of the `APIRequestHandler` class:

```
api_handler = APIRequestHandler(headers={'Authorization': 'Bearer YOUR_API_KEY'}, max_retry_attempts=3)
```

3. To send an API request, use the `send_api_request` method:

```

response = api_handler.send_api_request(
    base_url='https://api.example.com',
    method='GET',
    params={'param1': 'value1'},
    headers={'Content-Type': 'application/json'}
)

```

The `send_api_request` method returns the response JSON data as a dictionary if the request is successful. If a fatal status code is received, a `FatalStatusCodeError` will be raised.

## API Reference
[Overview of the API Reference section]

## Contributing
[Contributing guidelines]

## License
[License information]
