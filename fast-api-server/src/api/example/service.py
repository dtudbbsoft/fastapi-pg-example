from datetime import datetime
from uuid import UUID

from src.api.example.schema import Example


class ExampleService:
    @staticmethod
    def get_example(id: UUID) -> Example:
        print(f"ExampleService - get_example - id = {id}")
        return Example(id=id, date=str(datetime.now()))


async def get_example_service() -> ExampleService:
    return ExampleService()
