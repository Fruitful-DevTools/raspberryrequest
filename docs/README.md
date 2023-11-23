# RaspberryRequest - v0.0.1

RaspberryRequest is a simple, easy-to-use py package for making HTTP requests and managing responses. RaspberryRequest is designed for easy building around getting and posting data to APIs, utilising the well-known requests module.

**Features**
1. Custom Handling of responses based on response status codes.
2. Exponential backoff implementation, with custom number of retries and maximum delay time.
3. Call counter.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Installation

Installing raspberryrequest can be done simply and easily via pip:

```
pip install raspberryrequest # And you're good to go!
```

## Basic Usage

The `APIRequestHandler` class is a utility for sending API requests with retry logic. It provides a convenient way to handle common API request scenarios, such as setting headers, handling retries, and implementing backoff logic.

1. Import the `APIRequestHandler` class:

`from api_request_handler import APIRequestHandler`

2. Create an instance of the `APIRequestHandler` class:

```
handler = APIRequestHandler(headers={'some key', 'some val'}, max_attempts=3, max_delay=10)
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

## Contributing

If you have anything you think will be of a great addition to RaspberryRequest, or have a bug you would like to report, please follow the steps in [CONTRIBUTIONS](CONTRIBUTIONS.md) to see how you can do so!

## License
[License information](LICENSE.md)
