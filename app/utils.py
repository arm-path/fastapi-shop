import re
from typing import Literal


def camel_to_snake(title: str) -> str:
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
    return pattern.sub('_', title).lower()


def is_float(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def is_boolean(value: str) -> bool:
    if value == '1' or value == '0' or value == 'true' or value == 'false':
        return True
    return False


def check_type(str_type: Literal['integer', 'float', 'boolean', 'string'] | None, str_value: str) -> bool:
    if str_type == 'integer' and not str_value.isdigit():
        return False
    if str_type == 'float' and not is_float(str_value):
        return False
    if str_type == 'boolean' and not is_boolean(str_value):
        return False
    return True
