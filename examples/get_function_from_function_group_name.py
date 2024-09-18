import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import FunctionGroup, AiEngine
from tests.integration.test_ai_engine_client import api_key


async def main(
        function_group_name: str,
        agentverse_api_key: str,
        target_environment: str | None = None,
):
    # Request from cli args.
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}

    ai_engine: AiEngine = AiEngine(api_key=agentverse_api_key, options=options)
    function_groups: list[FunctionGroup] = await ai_engine.get_function_groups()

    target_function_group = next((g for g in function_groups if g.name == function_group_name), None)
    if target_function_group is None:
        raise Exception(f'Could not find "{target_function_group}" function group.')

    return await ai_engine.get_functions_by_function_group(function_group_id=target_function_group.uuid)
    
    
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("AV_API_KEY", "")

    # Parse CLI arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e",
        "--target_environment",
        type=str,
        required=False,
        help="The target environment: staging, localhost, production... You need to explicitly add the domain. By default it will be production."
    )
    parser.add_argument(
        "-fgn",
        "--fg_name",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    target_environment = args.target_environment

    res = asyncio.run(
        main(
            agentverse_api_key=api_key,
            function_group_name=args.fg_name,
            target_environment=args.target_environment
        )
    )
    pprint(res)