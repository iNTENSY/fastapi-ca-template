from httpx import AsyncClient
from starlette import status


class Test01ReadAccounts:
    async def test_to_take_list_of_accounts(self, async_client: AsyncClient):
        response = await async_client.get('/api/v1/accounts/')
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data is not None
        fields = list(data.keys())
        assert ['items', 'count'] == fields
