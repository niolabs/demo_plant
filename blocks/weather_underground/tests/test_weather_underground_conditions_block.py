from unittest.mock import patch

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from requests import Response
from requests.exceptions import HTTPError

from ..weather_underground_conditions_block import WeatherUndergroundConditions


class TestWeatherUndergroundConditions(NIOBlockTestCase):

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
        blk = WeatherUndergroundConditions()
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
        self.assertDictEqual(self.last_signal_notified().to_dict(),
                             mock_json.return_value["current_observation"])
        blk.stop()

    @patch("requests.get")
    @patch("requests.Response.json")
    def test_retry_on_bad_response(self, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 400
        mock_json.return_value = {
            'error_here': {
                'error': 'stop doing that'
            }
        }
        blk = WeatherUndergroundConditions()
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
        # retry should give up after one retry, and the request will have been
        # attempted twice
        with self.assertRaises(HTTPError):
            blk.process_signals([Signal()])
        self.assert_num_signals_notified(0)
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_get.call_args[0][0],
                         blk.URL_FORMAT.format(
                             blk.api_key(),
                             blk._api_endpoint,
                             state,
                             city)
                         )
        blk.stop()
