from time import sleep
from datetime import datetime

from src.util.logger import logger


class RequestDecorator:
    """
    Singleton class that provides a make_request decorator to be used on all requests. Ensures that all requests don't
    break the reddit API rate limiting.
    """
    _minimum_time = 1

    def __init__(self):
        self._last_request = None

    def make_request(self, func):
        """
        Makes sure that there is a minimum time between function calls that use this decorator.
        """

        def rate_limit(*args, **kwargs):
            now = datetime.now()

            if self._last_request:
                time_since_last_request = (
                    now - self._last_request).total_seconds()
                time_to_sleep = self._minimum_time - time_since_last_request
                if time_to_sleep > 0:
                    sleep(time_to_sleep)

            logger.debug(f'new request made at {datetime.now()}')
            self._last_request = datetime.now()
            return func(*args, **kwargs)

        return rate_limit
