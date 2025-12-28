import re


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
