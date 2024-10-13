from requests.models import Response

from app.datsteam.http import http_client_abstract
from app.datsteam.config import config


class HttpClient(http_client_abstract):
    __base_url = config['url']

    def post_request(url: str = __base_url, data: dict = {}, headers: dict = {}) -> Response:
        pass
