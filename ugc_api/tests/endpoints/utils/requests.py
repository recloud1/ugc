from http import HTTPStatus
from typing import Tuple

from endpoints.core.constants import ApiRoutes, RequestMethods
from starlette.responses import Response
from starlette.testclient import TestClient

from core.config import envs


async def api_request(
    request_client: TestClient,
    method: RequestMethods,
    route: ApiRoutes,
    route_detail: str = "",
    query_params: dict | None = None,
    data: dict | None = None,
    headers: dict | None = None,
    with_check: bool = True,
) -> Tuple[Response, dict]:
    if not headers:
        headers = {}

    headers.update({"Authorization": "Bearer test_token"})
    response = request_client.request(
        method=method,
        url=f"http://{envs.app.host}:{envs.app.port}/{route}{route_detail}",
        params=query_params,
        json=data,
        headers=headers,
    )

    if with_check:
        assert response.status_code == HTTPStatus.OK

    data = response.json()

    return response, data
