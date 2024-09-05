from typing import Generic, TypeVar


Request = TypeVar("Request", contravariant=True)
Response = TypeVar("Response", covariant=True)


class Interactor(Generic[Request, Response]):
    async def __call__(self, request: Request) -> Response:
        raise NotImplementedError
