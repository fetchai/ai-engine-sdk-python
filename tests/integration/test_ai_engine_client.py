import os
from idlelib.iomenu import py_extensions
from pprint import pprint
from symtable import Function

import pytest
from faker import Faker

from ai_engine_sdk import FunctionGroup, AiEngine
from ai_engine_sdk.client import CreditBalance, Model, Session
from tests.conftest import ai_engine_client

api_key = os.getenv("AV_API_KEY", "")
environment_domain = os.getenv("TESTING_AV_ENVIRONMENT_DOMAIN", "")
fake = Faker()

# TODO: define environment for tests (by default the sdk is pointing to prod, and maybe SHOULD point to PRODUCTION).
# TODO: environment as secret for CI.
# TODO: should we exclude tests from the sdk package? how?
class TestAiEngineClient:
    @pytest.mark.asyncio
    # @pytest.mark.parametrize("ai_engine_client", [{"api_key": api_key}], indirect=True)
    async def test_get_function_groups_should_return_private_and_public(self, ai_engine_client):
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert isinstance(function_groups, list)
        # Should I test the content... ?

    @pytest.mark.asyncio
    async def test_create_and_delete_function_groups(self, ai_engine_client: AiEngine):
        new_function_group_name = fake.company()
        new_function_group: FunctionGroup = await ai_engine_client.create_function_group(
            is_private=True,
            name=f"TESTS: {new_function_group_name}"
        )
        assert isinstance(new_function_group, FunctionGroup)
        pprint(new_function_group)
        # TearDown + Test
        # 401 when staging or prod
        delete_res = await ai_engine_client.delete_function_group(function_group_id=new_function_group.uuid)

    @pytest.mark.asyncio
    async def test_get_credits_returns_credit_balance(self, ai_engine_client: AiEngine):
        result: CreditBalance = await ai_engine_client.get_credits()
        assert isinstance(result, CreditBalance)

    @pytest.mark.asyncio
    async def test_get_models_list(self, ai_engine_client: AiEngine):
        result: list[Model] = await ai_engine_client.get_models()
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], Model)

    @pytest.mark.asyncio
    async def test_create_session(self, ai_engine_client: AiEngine):
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        result: Session = await ai_engine_client.create_session(function_group=function_groups[0].uuid)
        assert isinstance(result, Session)

    # @pytest.mark.asyncio
    # async def test_delete_function_group(self, ai_engine_client: AiEngine):
    #     await ai_engine_client.delete_function_group()


    @pytest.mark.asyncio
    async def test_create_function_group_and_list_them(self, ai_engine_client: AiEngine):
        name = fake.company()
        new_function_group: FunctionGroup = await ai_engine_client.create_function_group(is_private=True, name=f"TESTS: {name}")
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert any(filter(lambda x: x.uuid == new_function_group.uuid, function_groups))

        # TearDown + Test delete
        # 401 when staging or prod
        await ai_engine_client.delete_function_group(function_group_id=new_function_group.uuid)


    # Negative tests
    @pytest.mark.asyncio
    async def test_not_created_function_group_isnt_in_the_function_group_list(self, ai_engine_client: AiEngine):
        uuid = fake.uuid4()
        function_groups: list[FunctionGroup] = await ai_engine_client.get_function_groups()
        assert not any(filter(lambda x: x.uuid == uuid, function_groups))

