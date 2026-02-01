import json
import os
import re
from dataclasses import asdict, fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Type, TypeVar

T = TypeVar('T')
DATA_DIRECTORY = "data"
TEMPLATE_DIRECTORY="templates"
ICON_DIRECTORY="assets/icons"

def read_icon_path(file_name: str) -> str:
    icon_path = Path(ICON_DIRECTORY) / file_name
    svg_content = icon_path.read_text()
    match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL)

    if match:
        return match.group(1).strip()

    return svg_content


def write_json(obj: object, file_name: str):
    data_dir = Path(DATA_DIRECTORY)
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / file_name
    with open(file_path, "w") as file:
        json.dump(obj, file, indent=2, default=json_serializer)


def read_json(file_name: str, cls: Type[T]) -> T:
    data_dir = Path(DATA_DIRECTORY)
    file_path = data_dir / file_name

    with open(file_path, "r") as file:
        data = json.load(file)

    return deserialize_dataclass(data, cls)

def read_template() -> str:
    template_dir = Path(TEMPLATE_DIRECTORY)
    file_path = template_dir / os.getenv("TEMPLATE")
    return file_path.read_text()

def write_template(template: str):
    data_dir = Path(DATA_DIRECTORY)
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / os.getenv("TEMPLATE")
    with open(file_path, "w") as file:
        file.write(template)

def json_serializer(obj):
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, Enum):
        return obj.name
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def deserialize_dataclass(data: dict, cls: Type[T]) -> T:
    if not is_dataclass(cls):
        return data

    field_values = {}
    for field in fields(cls):
        value = data.get(field.name)

        if value is None:
            field_values[field.name] = None
        elif is_dataclass(field.type):
            field_values[field.name] = deserialize_dataclass(value, field.type)
        elif isinstance(field.type, type) and issubclass(field.type, Enum):
            field_values[field.name] = field.type[value]
        else:
            field_values[field.name] = value

    return cls(**field_values)
