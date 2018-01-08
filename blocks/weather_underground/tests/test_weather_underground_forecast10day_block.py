from unittest.mock import patch

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from requests import Response

from ..weather_underground_forecast10day_block \
    import WeatherUndergroundForecast10Day


class TestWeatherUndergroundForecast10Day(NIOBlockTestCase):

    @patch("requests.get")
    @patch("requests.Response.json")
    def test_process_good_response(self, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        mock_json.return_value = {
            'current_observation': {
                'stuff': 'things'
            }
        }
        blk = WeatherUndergroundForecast10Day()
        city = 'San Francisco'
        state = 'California'
        self.configure_block(blk, {
            'retry_options': {
                'multiplier': 1,
                'max_retry': 1
            },
            'state': state,
            'city': city,
            'log_level': 'DEBUG'
        })
        blk.start()
        blk.process_signals([Signal()])
        self.assert_num_signals_notified(1)
        self.assertEqual(mock_get.call_args[0][0],
                         blk.URL_FORMAT.format(
                             blk.api_key(),
                             blk._api_endpoint,
                             state,
                             city)
                         )
        blk.stop()
