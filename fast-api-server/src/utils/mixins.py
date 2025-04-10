import time

import requests


class HTTPMixin:
    def make_request(
        self,
        nb_retries: int = 3,
        sleep_time: float = 0.2,
        exponential_backoff: bool = False,
        **kwargs,
    ) -> requests.Response:
        response = requests.request(**kwargs)

        if response.status_code // 100 == 2:
            return response

        if nb_retries == 0 or response.status_code // 100 == 4:
            response.raise_for_status()

        time.sleep(sleep_time)

        if exponential_backoff:
            sleep_time *= 2

        return self.make_request(
            nb_retries=nb_retries - 1,
            sleep_time=sleep_time,
            exponential_backoff=exponential_backoff,
            **kwargs,
        )
