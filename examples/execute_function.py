import argparse
import asyncio
import os
from pprint import pprint

from faker.utils.decorators import lowercase

from ai_engine_sdk import AiEngine, FunctionGroup, ApiBaseMessage
from ai_engine_sdk.client import Session
from tests.conftest import function_groups


async def main(
        target_environment: str,
        agentverse_api_key: str,
        function_uuid: str,
        function_group_uuid: str
):
    # Request from cli args.
    options = {}
    if target_environment:
        options = {"api_base_url": target_environment}

    ai_engine = AiEngine(api_key=agentverse_api_key, options=options)

    session: Session = await ai_engine.create_session(function_group=function_group_uuid)
    await session.execute_function(function_ids=[function_uuid], objective="", context="")

    try:
        empty_count = 0
        session_ended = False

        print("Waiting for execution:")
        while empty_count < 100:
            messages: list[ApiBaseMessage] = await session.get_messages()
            if messages:
                pprint(messages)
                if any((msg.type.lower() == "stop" for msg in messages)):
                    print("DONE")
                    break
            if len(messages) % 10 == 0:
                print("Wait...")
            if len(messages) == 0:
                empty_count += 1
            else:
                empty_count = 0


    except Exception as ex:
        pprint(ex)
        raise

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
        "-fg",
        "--function_group_uuid",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-f",
        "--function_uuid",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    result = asyncio.run(
        main(
            agentverse_api_key=api_key,
            target_environment=args.target_environment,
            function_group_uuid=args.function_group_uuid,
            function_uuid=args.function_uuid
        )
    )
    pprint(result)
