import pytest
from httpx import AsyncClient
from starlette import status

from app.domain.accounts.entity import Account


class Test01ReadAccounts:
    @pytest.mark.anyio
    async def test_to_take_list_of_accounts(self, async_client: AsyncClient, admin_entity: Account) -> None:
        response = await async_client.get('/api/v1/accounts/')
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data is not None
        fields = list(data.keys())
        assert ['items', 'count'] == fields
        assert len(data["items"]) == 1

    @pytest.mark.anyio
    async def test_another_try(self, async_client):
        response = await async_client.get('/api/v1/accounts/')
        data = response.json()

        assert len(data["items"]) == 0


class Test02UpdateAccount:
    @pytest.mark.anyio
    async def test_update_account(self, admin_client: AsyncClient, admin_entity: Account):
        data = {
            "uid": str(admin_entity.id.value),
            "username": "NewAccountUserName",
            "email": admin_entity.email.value
        }
        response = await admin_client.patch('/api/v1/accounts/', json=data)

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["uid"] == str(admin_entity.id.value)
        assert data["username"] == "NewAccountUserName"
