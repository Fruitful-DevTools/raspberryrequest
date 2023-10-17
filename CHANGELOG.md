# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2023-10-17

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