import os

import pytest

from ai_engine_sdk import AiEngine, FunctionGroup
from ai_engine_sdk.client import Session


def get_ai_engine_client(api_key: str, environment_domain: str) -> AiEngine:
    ai_engine_client = AiEngine(api_key=api_key, options={"api_base_url": environment_domain})
    return ai_engine_client


@pytest.fixture(scope="module")
def ai_engine_client(request) -> AiEngine:
    if hasattr(request, "param"):
        api_key = request.param["api_key"]
        environment_domain = request.param["environment_domain"]
    else:
        api_key = os.getenv("AV_API_KEY", "")
        environment_domain = os.getenv("TESTING_AV_ENVIRONMENT_DOMAIN")

    return get_ai_engine_client(api_key=api_key, environment_domain=environment_domain)


@pytest.fixture(scope="module")
async def function_groups(ai_engine_client) -> list[FunctionGroup]:
    function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
    return function_groups

# @pytest.fixture(scope="module")
# async def session_with_next_generation_model(ai_engine_client) -> Session:
#     # TODO: We need a concrete function group id for the integration tests in the CI.
#     session: Session = await ai_engine_client.create_session(
#         function_group=function_groups, opts={"model": "next-gen"}
#     )
#     return session