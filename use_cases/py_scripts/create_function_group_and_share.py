import asyncio
import argparse
import os

from ai_engine_sdk import AiEngine
from ai_engine_sdk.use_cases.create_function_group_and_share import CreateFunctionGroupAndShare


async def main(
    agentverse_api_key: str,
    fg_is_private: bool,
    fg_name: str,
    target_user_email: str,
):
    # Request from cli args.
    c = AiEngine(api_key=agentverse_api_key)
    create_fg_and_share_service = CreateFunctionGroupAndShare(client=c)
    result = await create_fg_and_share_service(fg_is_private=fg_is_private, fg_name=fg_name, target_user_email=target_user_email)

    return result


if __name__ == "__main__":
    api_key = os.getenv("AV_API_KEY", "")

    parser = argparse.ArgumentParser()
    parser.add_argument("-fg_name", "--function_group_name", type=str, required=True, help="The function group id")
    parser.add_argument("-fg_private", "--function_group_is_private", type=bool, required=True, help="The function group privacy: is private or not? boolean")
    parser.add_argument("-target_user_email", "--target_user_email", type=str, required=True, help="The function group privacy: is private or not? boolean")
    args = parser.parse_args()

    fg_is_private = args.function_group_is_private
    fg_name = args.function_group_name
    target_user_email = args.target_user_email
    result = asyncio.run(main(agentverse_api_key=api_key, fg_is_private=fg_is_private, fg_name=fg_name, target_user_email=target_user_email))

    # IF not exception triggered is OK
    print("SUCCESS")
