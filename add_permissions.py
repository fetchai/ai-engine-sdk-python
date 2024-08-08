# WIP:  this has to be finished, refactored and create a client for this functionality
import asyncio

import json
import logging
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)
default_api_base_url = "https://agentverse.ai"

async def make_api_request(
    api_base_url: str,
    api_key: str,
    method: str,
    endpoint: str,
    payload: Optional[dict] = None
) -> dict:
    body = json.dumps(payload) if payload else None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with aiohttp.ClientSession() as session:
        logger.debug(f"\n\n 📤 Request triggered : {method} {api_base_url}{endpoint}")
        logger.debug(f"{body=}")
        logger.debug("---------------------------\n\n")
        async with session.request(method, f"{api_base_url}{endpoint}", headers=headers, data=body) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status {response.status} to {endpoint}")
            return await response.json()

class Client:
    def __init__(self, api_key: str):
        self._api_base_url = default_api_base_url
        self._api_key = api_key

    # Getters

    async def get_function_groups(self) -> list:
        logger.debug("get_function_groups")
        publicGroups, privateGroups = await asyncio.gather(
            self.get_public_function_groups(),
            self.get_private_function_groups()
        )
        return privateGroups + publicGroups

    async def get_private_function_groups(self) -> list:
        print("HEEELLLLOOOO PRIVATE")
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint="/v1beta1/function-groups/"
        )

        return raw_response

    async def get_public_function_groups(self) -> list:
        print("HEEELLLLOOOO")
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='GET',
            endpoint="/v1beta1/function-groups/public/"
        )
        a=1
        logger.debug(f"{raw_response=}")

        return raw_response

    # Creators
    async def create_function_group(self):
        payload = {
            "isPrivate": True,
            "name": "Oh my good, function group! Share, share, share!"
        }
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='POST',
            endpoint="/v1beta1/function-groups/",
            payload=payload
        )
        return raw_response

    async def create_function(self):
        letstryrandomvaluestr = "letstryrandomvaluestr"
        payload = {
            "agent": "agent1qdjp6xxhf08nw46yapj62yfurp4td7u0awpmnpy9ky4dj52n7ua4xq6aett",
            "name": "Function-sita! Dummy one.",
            "description": "Dummy function that does nothing.",
            "protocolDigest": letstryrandomvaluestr,
            "modelDigest": letstryrandomvaluestr,
            "modelName": letstryrandomvaluestr,
            "arguments": [{"name": "arg2", "required": False, "type": "str", "description": "You do not need it, I am dumb!"}],
            "type": "PRIMARY",
            "isDialogue": False
        }
        raw_response: dict = await make_api_request(
            api_base_url=self._api_base_url,
            api_key=self._api_key,
            method='POST',
            endpoint="/v1beta1/functions/",
            payload=payload
        )
        return raw_response


# --- End class ---

# endpoint ="/v1beta1/function-groups/public/"
async def remove_dummy_set_up():
    ...


async def create_and_share_function_and_function_group(client: Client):
    # create dummy f to be shared.
    await client.create_function_group()
    # create function and associate it to the prev fg


async def main():
    # Request from cli args.
    API_TOKEN = "eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3MzA3MzE4NTQsImdycCI6ImludGVybmFsIiwiaWF0IjoxNzIyOTU1ODU0LCJpc3MiOiJmZXRjaC5haSIsImp0aSI6IjJiOGNmMjc0NzczOGZkOTBiNTM1ZjJlNSIsInNjb3BlIjoiYXYiLCJzdWIiOiJlODlkYTkzMTFkNWNiY2EyMjg1NjllMjMwNmRjMGIyNDllOTQ4NjMwM2EwYzVmNTAifQ.TRRIdvs5-N96PebN9J-aB5P1yGhYh56wjV86zfhgPYQBKGr2lAztjguoB2FrjOvphydWgowE6wZEH_fYSqVHQHy6ys9STNletsT7hCbuNE1zl4M6PGYvARg7aa-3-Yf22Nc6x8edc4OSubADIG78Huk17k471RmVfFrLPK6feNpmvxS4lHzliscTFP8Lr7dI88kceIAHk1MBXyrnxI6_Q6rYRAxRCwkURscO02JbK3oQBmaWS1Q7fIUCOhLakm67uG-0J0e_1e7tAXDw0DTs15bqKduWEjjrrHaiwAhPEMKnFUcJe2M1Ii6DYJAgeDfxNriLdc3xmt8lMpod1K8RIA"
    c = Client(api_key=API_TOKEN)

    # GET and Check existing fgs
    fgs = await c.get_function_groups()


    a=1

if __name__ == "__main__":
    asyncio.run(main())
