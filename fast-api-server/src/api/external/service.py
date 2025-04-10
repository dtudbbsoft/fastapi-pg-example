import requests

from src.utils.mixins import HTTPMixin
from src.settings import settings


class ExternalService(HTTPMixin):
    def __init__(self):
        self.base_url = settings.external_base_url,
        self.api_token = settings.external_api_token,

    def get_by_id(self, external_id: str, **kwargs):
        url = f"{self.base_url}/{external_id}"

        resp = self.make_request(method="GET", url=url, **kwargs)

        return resp.json()["response"]

    def create_object(self, fields: dict | None = None, **kwargs):
        resp = self.make_request(method="POST", url=self.base_url, json=fields, **kwargs)

        return resp.json()["id"]

    def update_object(self, external_id: str, fields: dict, **kwargs):
        url = f"{self.base_url}/{external_id}"

        self.make_request(method="PATCH", url=url, json=fields, **kwargs)

    def replace_object(self, external_id: str, fields: dict, **kwargs):
        url = f"{self.base_url}/{external_id}"

        self.make_request(method="PUT", url=url, json=fields, **kwargs)

    def delete_by_id(self, external_id: str, **kwargs):
        url = f"{self.base_url}/{external_id}"

        self.make_request(method="DELETE", url=url, **kwargs)

    def make_request(
        self,
        nb_retries: int = 3,
        sleep_time: float = 0.2,
        exponential_backoff: bool = False,
        **kwargs,
    ) -> requests.Response:
        if kwargs.get("headers") is None:
            kwargs["headers"] = self._get_headers()

        return super().make_request(
            nb_retries=nb_retries,
            sleep_time=sleep_time,
            exponential_backoff=exponential_backoff,
            **kwargs,
        )
