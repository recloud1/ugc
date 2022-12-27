from typing import Any, Optional, TypeVar
from uuid import UUID

from bson import Binary

SetType = TypeVar("SetType", bound=set)


def add_to_set(set_: Optional[SetType], value: Any) -> SetType:
    if set_ is None:
        set_ = set()
    set_.add(value)

    return set_


def convert_uuid(_id: UUID) -> Binary | str:
    result = str(_id)

    return result
