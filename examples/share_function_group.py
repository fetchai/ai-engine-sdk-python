import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import AiEngine


async def main(
    fg_id: str,
    agentverse_api_key: str,
    target_user_email: str,
    target_environment: str
):
    # Request from cli args.
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}

    c = AiEngine(api_key=agentverse_api_key, options=options)

    result = await c.share_function_group(
        function_group_id=fg_id,
        target_user_email=target_user_email
    )
    return result


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser()
    api_key = os.getenv("AV_API_KEY", "")
    parser.add_argument(
        "-fg_id_to_share",
        "--function_group_id_to_share",
        type=str,
        required=False,
        help="The function group name. If you add this option, will be shared and not created."
    )
    parser.add_argument(
        "-e",
        "--target_environment",
        type=str,
        required=False,
        help="The target environment: staging, localhost, production... You need to explicitly add the domain. By default it will be production."
    )
    parser.add_argument(
        "-target_user_email",
        "--target_user_email",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    fg_id_to_share = args.function_group_id_to_share
    target_user_email = args.target_user_email
    target_environment = args.target_environment

    result = asyncio.run(
        main(
            agentverse_api_key=api_key,
            fg_id=fg_id_to_share,
            target_user_email=target_user_email,
            target_environment=target_environment
        )
    )

    # IF not exception triggered is OK
    pprint(result)
    print("SUCCESS")

