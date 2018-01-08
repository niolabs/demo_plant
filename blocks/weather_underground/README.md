WeatherUndergroundConditions
============================
Gets current conditions weather data from WeatherUnderground for the given city and state.

Properties
----------
- **api_key**: WeatherUnderground API key
- **city**: City to get conditions for
- **retry_options**: Options for retrying requests to WeatherUnderground
- **state**: State to get conditions for

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals, one signal for each input signal with added weather data attributes.

Commands
--------
None

Dependencies
------------
requests

WeatherUndergroundForecast10Day
===============================
Gets 10 day forecast weather data from WeatherUnderground for the given city and state.

Properties
----------
- **api_key**: API credentials.
- **city**: City to get forecast for
- **retry_options**: Options for retrying requests to WeatherUnderground
- **state**: State to poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals, one signal for each input signal with added weather data attributes.

Commands
--------
None

Dependencies
------------
requests
