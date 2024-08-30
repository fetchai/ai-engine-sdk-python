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


'bcd181fa-14dd-4d94-8094-c9b4c085e8aa' '319c5771-0587-4a6f-9385-f3a0099e4471' '69d191b2-68a3-4b47-9be5-496ce6b389a0' '2148759e-ab68-46b7-b276-fcd1bca54a59' '23a20a1c-e0ce-45d3-b44a-dc88db1b8b57' 'fe9f72a3-53be-4dd9-a991-ebf0915939f3' '4e88fe59-6b23-40d4-86f0-55276453cb4a' 'a8eef980-154f-4e4d-912e-d7cf766b9d0d' '635846a3-5268-4575-a776-ff98bf023d4a' '91451d32-2c7f-461b-b01e-73be9d979e85' '4616a8c6-f3ed-4b40-95ee-2a2a5a6c6c75' 'd6586f19-94bb-4dcd-a203-ab7dd477e5ea' '72df4011-9e29-4e74-93c9-3ae777034dec' '0033b364-3328-4aa7-9152-32b32464cdf2' 'df831203-0704-470b-968d-fbf9623f4a10' 'd36ed21c-599c-4003-8370-89c48d242805' 'c429943f-b6b7-4c3f-8a02-d3c7ae880391' 'a0f0c23a-6ba8-4e95-9aee-44698a96e825' '00fddeb7-dca1-42f9-9624-84404220ba56' '3aa4ade3-b02b-4e43-b48e-d315e6b82049' '912e9de1-604d-4f9d-9f75-bbe8480c218a' '49f7ea7b-10f7-40ef-9bc6-93406dd68dc8' '97238632-91c8-4516-acfa-ae90208a0013' 'e504eabb-4bc7-458d-aa8c-7c3748f8952c'

"""
python examples/list_function_groups_by_user.py -e "https://engine-staging.sandbox-london-b.fetch-ai.com";
python examples/functions_by_function_group.py -e "https://engine-staging.sandbox-london-b.fetch-ai.com" -fgs 'bcd181fa-14dd-4d94-8094-c9b4c085e8aa' '319c5771-0587-4a6f-9385-f3a0099e4471' '69d191b2-68a3-4b47-9be5-496ce6b389a0' '2148759e-ab68-46b7-b276-fcd1bca54a59' '23a20a1c-e0ce-45d3-b44a-dc88db1b8b57' 'fe9f72a3-53be-4dd9-a991-ebf0915939f3' '4e88fe59-6b23-40d4-86f0-55276453cb4a' 'a8eef980-154f-4e4d-912e-d7cf766b9d0d' '635846a3-5268-4575-a776-ff98bf023d4a' '91451d32-2c7f-461b-b01e-73be9d979e85' '4616a8c6-f3ed-4b40-95ee-2a2a5a6c6c75' 'd6586f19-94bb-4dcd-a203-ab7dd477e5ea' '72df4011-9e29-4e74-93c9-3ae777034dec' '0033b364-3328-4aa7-9152-32b32464cdf2' 'df831203-0704-470b-968d-fbf9623f4a10' 'd36ed21c-599c-4003-8370-89c48d242805' 'c429943f-b6b7-4c3f-8a02-d3c7ae880391' 'a0f0c23a-6ba8-4e95-9aee-44698a96e825' '00fddeb7-dca1-42f9-9624-84404220ba56' '3aa4ade3-b02b-4e43-b48e-d315e6b82049' '912e9de1-604d-4f9d-9f75-bbe8480c218a' '49f7ea7b-10f7-40ef-9bc6-93406dd68dc8' '97238632-91c8-4516-acfa-ae90208a0013' 'e504eabb-4bc7-458d-aa8c-7c3748f8952c' ;
"""


# e504eabb-4bc7-458d-aa8c-7c3748f8952c