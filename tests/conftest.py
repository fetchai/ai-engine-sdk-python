import os

import pytest

from ai_engine_sdk import AiEngine, FunctionGroup


def get_ai_engine_client(api_key) -> AiEngine:
    ai_engine_client = AiEngine(api_key=api_key)
    return ai_engine_client


@pytest.fixture(scope="module")
def ai_engine_client(request) -> AiEngine:
    if hasattr(request, "param"):
        api_key = request.param["api_key"]
    else:
        api_key = os.getenv("AV_API_KEY", "")

    return get_ai_engine_client(api_key)


@pytest.fixture(scope="module")
async def function_groups(ai_engine_client) -> list[FunctionGroup]:
    function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
