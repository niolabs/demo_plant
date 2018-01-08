import requests

from nio.block.base import Block
from nio.block.mixins import Retry
from nio.properties.string import StringProperty
from nio.signal.base import Signal
from nio.util.discovery import not_discoverable


@not_discoverable
class WeatherUndergroundBase(Retry, Block):
    """ This base block polls the Weather Underground API.

    Blocks that extend this should specify the api endpoint and what to extract
    from the response. This base block uses 'conditions' as an example:
        http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        city (string): City to poll for weather conds.
        state (string): State to poll for weather conds.

    """
    URL_FORMAT = ("http://api.wunderground.com/api/{}/"
                  "{}/q/{}/{}.json")
    state = StringProperty(title='State', default='')
    city = StringProperty(title='City', default='')
    api_key = StringProperty(title='API Key',
                             default='[[WEATHER_UNDERGROUND_KEY_ID]]')

    def __init__(self):
        super().__init__()
        self._api_endpoint = None

    def get_signal_from_response(self, resp):
        return Signal(resp.json())

    def process_signals(self, signals):
        weather_signals = []
        for signal in signals:
            response = self.execute_with_retry(
                self.get_weather_from_city_state,
                self.state(signal),
                self.city(signal))

            weather_signals.append(self.get_signal_from_response(response))

        self.notify_signals(weather_signals)

    def get_weather_from_city_state(self, state, city):
        headers = {"Content-Type": "application/json"}
        get_url = self.URL_FORMAT.format(self.api_key(),
                                         self._api_endpoint,
                                         state,
                                         city)
        try:
            self.logger.debug("making request to url: {}".format(get_url))
            resp = requests.get(get_url, headers=headers)
            resp.raise_for_status()
        except:
            self.logger.exception("GET request failed")
            raise
        else:
            return resp
