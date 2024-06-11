from dataclasses import dataclass
from typing import NamedTuple, TypedDict


@dataclass
class UserData:
    full_name: str
    id: int
    image: str
    url: str


class UserInitChatDataT(NamedTuple):
    user1: UserData
    user2: UserData


class DataMessageT(TypedDict):
    action: str
    author: str
    content: str
    chatId: str


class ChatMessageT(TypedDict):
    type: str
    data: DataMessageT
