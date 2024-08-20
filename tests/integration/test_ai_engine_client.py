import os
from symtable import Function

import pytest
from faker import Faker

from ai_engine_sdk import FunctionGroup
from ai_engine_sdk.client import CreditBalance, Model, Session
from tests.conftest import ai_engine_client

api_key = os.getenv("AV_API_KEY", "")
fake = Faker()

# TODO: define environment for tests (by default the sdk is pointing to prod, and maybe SHOULD point to PRODUCTION).
# TODO: environment as secret for CI.
# TODO: should we exclude tests from the sdk package? how?
class TestAiEngineClient:
    # Canonical successful tests

    @pytest.mark.asyncio
    # @pytest.mark.parametrize("ai_engine_client", [{"api_key": api_key}], indirect=True)
    async def test_get_function_groups_should_return_private_and_public(self, ai_engine_client):
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert isinstance(function_groups, list)
        # Should I test the content... ?

    @pytest.mark.asyncio
    async def test_create_function_groups(self, ai_engine_client):
        name = fake.company()
        result: FunctionGroup = await ai_engine_client.create_function_group(is_private=True, name=name)
        assert isinstance(result, FunctionGroup)

    @pytest.mark.asyncio
    async def test_get_credits_returns_credit_balance(self, ai_engine_client):
        result: CreditBalance = await ai_engine_client.get_credits()
        assert isinstance(result, CreditBalance)

    @pytest.mark.asyncio
    async def test_get_models_list(self, ai_engine_client):
        result: list[Model] = await ai_engine_client.get_models()
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], Model)

    @pytest.mark.asyncio
    async def test_create_session(self, ai_engine_client):
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        result: Session = await ai_engine_client.create_session(function_group=function_groups[0].uuid)
        assert isinstance(result, Session)

    # @pytest.mark.asyncio
    # async def test_start_session_with_a_given_function(self, ai_engine_client):
    #     ...

    @pytest.mark.asyncio
    async def test_create_function_group_and_list_them(self, ai_engine_client):
        name = fake.company()
        result: FunctionGroup = await ai_engine_client.create_function_group(is_private=True, name=name)
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert any(filter(lambda x: x.uuid == result.uuid, function_groups))


    # Negative tests
    @pytest.mark.asyncio
    async def test_not_created_function_group_isnt_in_the_function_group_list(self, ai_engine_client):
        uuid = fake.uuid4()
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert not any(filter(lambda x: x.uuid == uuid, function_groups))

