import re


def camel_to_snake(title: str) -> str:
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
    return pattern.sub('_', title).lower()
