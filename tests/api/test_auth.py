import pytest
from httpx import AsyncClient
from starlette import status


class Test01Login:
    @pytest.mark.anyio
    async def test_login(self, async_client: AsyncClient, admin_entity):
        data = {"username": admin_entity.username.value, "password": "<PASSWORD>"}

        response = await async_client.post("/api/v1/auth/login", json=data)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert "access_token" in response_data
