import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import AiEngine


async def main(target_environment: str, agentverse_api_key: str):
    # Request from cli args.
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}

    c = AiEngine(api_key=agentverse_api_key, options=options)

    user_functions = await c.get_functions()
    pprint(user_functions)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("AV_API_KEY", "")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--target_environment",
        type=str,
        required=False,
        help="The target environment: staging, localhost, production... You need to explicitly add the domain. By default it will be production."
    )
    args = parser.parse_args()

    target_environment = args.target_environment

    asyncio.run(main(agentverse_api_key=api_key, target_environment=target_environment))

