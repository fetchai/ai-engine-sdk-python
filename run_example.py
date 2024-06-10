import asyncio
import logging
import os
import sys

from ai_engine_sdk_py.client import AiEngine, FunctionGroup
from ai_engine_sdk_py.api_models.api_message import is_ai_engine_message, is_agent_message, \
    is_stop_message, ApiBaseMessage
from ai_engine_sdk_py.api_models.agents_json_messages import is_agent_json_confirmation_message, is_task_selection_message, \
    TaskSelectionMessage, is_data_request_message

logger = logging.getLogger(__name__)

api_key = os.getenv("AV_API_KEY", "")


async def main():
    logger.debug("🚀 Starting example execution")
    ai_engine = AiEngine(api_key)

    function_groups: list[FunctionGroup] = await ai_engine.get_function_groups()

    public_group = next((g for g in function_groups if g.name == "Fetch Verified"), None)
    if public_group is None:
        raise Exception('Could not find "Public" function group.')

    # TODO: proper function group, not hardcoded
    # Assuming '523a7194-214f-48fd-b5be-b0e953cc35a3' is meant to be used:
    # session = await ai_engine.create_session(function_group="523a7194-214f-48fd-b5be-b0e953cc35a3")
    session = await ai_engine.create_session(function_group=public_group.uuid)
    default_objective: str = "Find a flight to warsaw."
    objective = input(f"What is your objective [default: {default_objective}]: ") or "Find a flight to warsaw."
    await session.start(objective)

    try:
        empty_count = 0
        session_ended = False
        while empty_count < 12:
            messages: list[ApiBaseMessage] = await session.get_messages()
            if len(messages) == 0:
                empty_count += 1
            else:
                empty_count = 0

            message: ApiBaseMessage
            for message in messages:
                if is_task_selection_message(message_type=message.type):
                    task_selection_message: TaskSelectionMessage = message
                    print("Please select a option from the list below:\n")
                    for _, option in task_selection_message.options.items():
                        print(f"{option.key}: {option.title}")

                    option_key = str(input("\nEnter task number: "))

                    # check the index
                    if option_key not in task_selection_message.options.keys():
                        raise Exception("Invalid task number")

                    logger.debug(option_key)
                    await session.submit_task_selection(message, [task_selection_message.options[option_key]])
                    del task_selection_message
                elif is_agent_message(message):
                    print("Agent: ", message.text)

                    response = input("User (enter to skip): ")
                    if response == "exit":
                        break

                    if response != "":
                        await session.submit_response(message, response)
                elif is_ai_engine_message(message):
                    print("Engine:", message.text)
                elif is_agent_json_confirmation_message(message_type=message.type):
                    # TODO: RENAME/REFACTOR: This checker is functionally okay but confusing interface for clients.
                    print("Confirm:", message.payload)

                    response = input("\nPress enter to confirm, otherwise explain issue:\n")

                    if response == "":
                        await session.submit_confirmation(message)
                    else:
                        await session.reject_confirmation(message, response)
                elif is_stop_message(message):
                    print("\nSession has ended")
                    session_ended = True
                    break
                elif is_data_request_message(message_type=message.type):
                    # This is just for entering data.
                    # TODO: How could we detect, for parsing, any entry data apart than the type?
                    #  Of course, we can rely on the user's ability for the nonce.
                    print("Insert data: ", message.text)
                    response = input("User (enter to skip): ")
                    if response != "":
                        await session.submit_response(message, response)

            # if the session has concluded then break
            if session_ended:
                break

            await asyncio.sleep(1.5)
            logger.debug(f"No messages: {empty_count} times in a row")
    except Exception as e:
        logger.debug(f"Unhandled exception: {e}")
        print("Error", e)
        # TODO: should this be raised?
        raise e
    finally:
        # clean up the session
        await session.delete()


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
    )
    asyncio.run(main())
