from abc import ABC, abstractmethod
from requests.models import Response


class HttpClientAbstract(ABC):

    @abstractmethod
    def post_request(url: str, data: dict, headers: dict) -> Response:
        pass
