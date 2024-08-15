from ai_engine_sdk import AiEngine, FunctionGroup


class CreateFunctionGroupAndShare:
    client: AiEngine

    def __init__(self, client: AiEngine):
        self.client = client

    async def __call__(
            self,
            fg_is_private: bool,
            fg_name: str,
            target_user_email: str,
    ) -> dict:

        # Create a function group
        created_function_group: FunctionGroup = await self.client.create_function_group(is_private=fg_is_private, name=fg_name)

        # Share function group
        res = await self.client.share_function_group(
            function_group_id=created_function_group.uuid,
            target_user_email=target_user_email
        )

        return res

