# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2023-12-06

## Changed

- get_session_data method to return dict.
- get_dict method in SessionData class to return dict.


## [1.1.0] - 2023-11-24

## Added

- SessionData class
- Functionality to retrieve and reset session data from APIRequestHandler class
- update_session_data function

## Changed

- Refractored valid_status.
- Changed name of valid_status to validate_status.
- StatusCodes to models.py

## Removed

- config.py

## [1.0.0] - 2023-11-23

## Added

- StatusCodes data class
- status code handling methods in APIRequestHandler class.

## Changed

- Put status code lists into status codes dataclass.
- Refractored APIRequestHandler
- Refractored valid_status function
- Refractored calculate_backoff function


## [Unreleased]

## [0.0.0-2a] - 2023-10-17

### Added

- config.py. Holds status codes configuration.
- session.prepare_request method in make_request.py

### Changed

- Changed erronious name in RaspberryRequestException exception class.
- Renamed valid_status.py to validate.py, make_request.py to request.py and calculate_backoff.py to backoff.py for brevity.
- Moved request.py into modules directory.

### Removed

- models.py. Status codes are now in config.py
- components directory.

### Fixed

- Import error for module package