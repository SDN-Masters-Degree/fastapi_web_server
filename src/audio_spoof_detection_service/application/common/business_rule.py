from typing import Generic, TypeVar


InputEntity = TypeVar('InputEntity')


class BusinessRule(Generic[InputEntity]):
    async def __call__(self, input_entity: InputEntity) -> None:
        raise NotImplementedError()
