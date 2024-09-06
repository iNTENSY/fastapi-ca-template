import pytest
from httpx import AsyncClient
from starlette import status


class Test00HealthCheck:
    @pytest.mark.anyio
    async def test_healthcheck(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
