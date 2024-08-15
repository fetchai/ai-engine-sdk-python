import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import AiEngine
from dotenv import load_dotenv

load_dotenv()
AV_API_KEY=os.getenv("AV_API_KEY", "")


async def get_functions_by_user(
        client: AiEngine,
):
    return await client.get_function_groups()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--target_environment",
        type=str,
        required=False,
        help="The target environment: staging, localhost, production... You need to explicitly add the domain. By default it will be production."
    )
    args = parser.parse_args()

    # user_email = args.user_email
    target_environment = args.target_environment

    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}
    c = AiEngine(api_key=AV_API_KEY, options=options)


    result = asyncio.run(
        get_functions_by_user(
            client=c
        )
    )

    pprint(result)
