import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import AiEngine


async def main(target_environment: str, agentverse_api_key: str, function_groups: list[str]):
    # Request from cli args.
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}

    c = AiEngine(api_key=agentverse_api_key, options=options)

    for function_group in function_groups:
        print(f"======= function_group: {function_group} =======")
        user_functions = await c.get_functions_by_function_group(function_group_id=function_group)
        pprint(user_functions)
        print("-----")


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
    parser.add_argument(
        "-fgs",
        "--function_groups",
        nargs="+",
        required=True,
        help="List of function groups ids to get their functions."
    )
    args = parser.parse_args()

    target_environment = args.target_environment
    function_groups: list[str] = args.function_groups

    asyncio.run(main(agentverse_api_key=api_key,  target_environment=target_environment, function_groups=function_groups))

