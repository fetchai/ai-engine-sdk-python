from ai_engine_sdk_py.api_models.agents_json_messages import TaskOption


def get_options_from_raw_api_response(raw_api_response: dict) -> list[dict[str, str]]:
    return [
        {
            'key': str(o['key']), 'title': o['value']
        }
        for o in raw_api_response['agent_json']['options']
    ]


def get_task_options_from_options(options: list[dict[str, str]]) -> list[TaskOption]:
    return [
        TaskOption.parse_obj({
            "key": option['key'],
            "title": option['title']
        })
        for option in options
    ]


def get_indexed_task_options_from_raw_api_response(raw_api_response: dict) -> dict[TaskOption]:
    options_list = get_options_from_raw_api_response(raw_api_response=raw_api_response)
    task_options_list = get_task_options_from_options(options=options_list)

    return {task_option.key: task_option for task_option in task_options_list}
