import argparse
import asyncio
import os
from pprint import pprint

from ai_engine_sdk import AiEngine, FunctionGroup
from dotenv import load_dotenv

load_dotenv()
AV_API_KEY=os.getenv("AV_API_KEY", "")


async def get_functions_groups_by_user(
        client: AiEngine,
) -> list[FunctionGroup]:
    return await client.get_function_groups()

async def get_fgs_by_function(client: AiEngine, function_id: str) -> list[FunctionGroup]:
    return await client.get_function_group_by_function(function_id)

def render(data: list[FunctionGroup], field: str) -> list:
    result = []
    if field:
        for i in data:
            # item = {f: i.__getattribute__(f) for f in fields}
            # result.append(item)
            result.append(i.__getattribute__(field))
    else:
        result = data
    pprint(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--target_environment",
        type=str,
        required=False,
        help="The target environment: staging, localhost, production... You need to explicitly add the domain. By default it will be production."
    )
    parser.add_argument(
        "-by",
        "--get-by",
        type=str,
        help="You can get function groups by: function, user",
        default="user",
        required=False
    )
    parser.add_argument(
        "-by-v",
        "--get-by-value",
        type=str,
        help="Value of the field you want filter by (if user do not provide anything)",
        required=False
    )
    # parser.add_argument(
    #     "-f",
    #     "--filter",
    #     required=False,
    #     nargs="+",
    #     help="You can ask for returning just a list of a concrete field."
    # )
    parser.add_argument(
        "-f",
        "--filter",
        required=False,
        type=str,
        help="You can ask for returning just a list of a concrete field."
    )
    args = parser.parse_args()
    target_environment = args.target_environment
    filter_fields = args.filter
    get_by = args.get_by
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}


    c = AiEngine(api_key=AV_API_KEY, options=options)

    if get_by == "function":
        function_id = args.get_by_value
        function_to_execute = get_fgs_by_function(client=c, function_id=function_id)
    elif get_by == "user":
        function_to_execute = get_functions_groups_by_user(client=c)
    result = asyncio.run(function_to_execute)
    print(filter_fields)


    render(data=result, field=filter_fields)
    