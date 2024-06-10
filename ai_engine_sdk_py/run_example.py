import asyncio
import logging
import os
import sys

from client import AiEngine, FunctionGroup
from api_models.agents_messages import (
    is_task_selection_message,
    is_agent_message,
    is_ai_engine_message,
    is_confirmation_message,
    is_stop_message
)

logger = logging.getLogger(__name__)

api_key = os.getenv("AV_API_KEY", "")

async def snooze(ms: int):
    await asyncio.sleep(ms / 1000)


async def main():
    logger.debug("🚀 Starting example execution")
    ai_engine = AiEngine(api_key)

    function_groups: list[FunctionGroup] = await ai_engine.get_function_groups()

    public_group = next((g for g in function_groups if g.name == "Fetch Verified"), None)
    if public_group is None:
        raise Exception('Could not find "Public" function group.')

    # TODO: proper function group, not hardcoded
    # Assuming '523a7194-214f-48fd-b5be-b0e953cc35a3' is meant to be used:
    session = await ai_engine.create_session(function_group="523a7194-214f-48fd-b5be-b0e953cc35a3")

    objective = input("What is your objective: ")
    await session.start(objective)

    try:
        empty_count = 0
        session_ended = False
        while empty_count < 12:
            messages = await session.get_messages()
            if len(messages) == 0:
                empty_count += 1
            else:
                empty_count = 0

            for message in messages:
                if is_task_selection_message(message):
                    print("Please select a task from the list below:\n")
                    for option in message.options:
                        print(f"{option.key}: {option.title}")

                    option_index = int(input("\nEnter task number: "))

                    # check the index
                    if option_index < 0 or option_index >= len(message.options):
                        raise Exception("Invalid task number")

                    await session.submit_task_selection(message, [message.options[option_index]])
                elif is_agent_message(message):
                    print("Agent: ", message.text)

                    response = input("User (enter to skip): ")
                    if response == "exit":
                        break

                    if response != "":
                        await session.submit_response(message, response)
                elif is_ai_engine_message(message):
                    print("Engine:", message.text)
                elif is_confirmation_message(message):
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
                else:
                    print("???", message)

            # if the session has concluded then break
            if session_ended:
                break

            # Chilling for 1.2 seconds...
            await snooze(1200)
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
