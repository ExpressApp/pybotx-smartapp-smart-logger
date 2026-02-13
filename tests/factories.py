from __future__ import annotations

from typing import Any
from uuid import uuid4

import factory
from pybotx import BotAccount, Chat, ChatTypes, SmartAppEvent, UserDevice, UserSender


def build_rpc_data(
    method: str = "get_api_version",
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "type": "smartapp_rpc",
        "method": method,
    }
    if params is not None:
        data["params"] = params

    return data


def build_raw_command(
    method: str = "get_api_version",
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "command": {
            "body": "system:smartapp_event",
            "command_type": "system",
            "data": {
                "data": {
                    "type": "smartapp_rpc",
                    "method": method,
                    "params": params or {},
                },
                "opts": {},
                "ref": str(uuid4()),
            },
            "metadata": {},
        },
        "proto_version": 4,
        "sync_id": str(uuid4()),
    }


class BotAccountFactory(factory.Factory):
    class Meta:
        model = BotAccount

    id = factory.LazyFunction(uuid4)
    host = factory.Faker("domain_name")


class ChatFactory(factory.Factory):
    class Meta:
        model = Chat

    id = factory.LazyFunction(uuid4)
    type = ChatTypes.GROUP_CHAT


class UserDeviceFactory(factory.Factory):
    class Meta:
        model = UserDevice

    manufacturer = None
    device_name = None
    os = None
    pushes = None
    timezone = None
    permissions = None
    platform = None
    platform_package_id = None
    app_version = None
    locale = None


class UserSenderFactory(factory.Factory):
    class Meta:
        model = UserSender

    huid = factory.LazyFunction(uuid4)
    udid = None
    ad_login = None
    ad_domain = None
    username = None
    is_chat_admin = True
    is_chat_creator = True
    device = factory.SubFactory(UserDeviceFactory)


class SmartAppEventFactory(factory.Factory):
    class Meta:
        model = SmartAppEvent

    bot = factory.SubFactory(BotAccountFactory)
    raw_command = factory.LazyFunction(build_raw_command)
    ref = factory.LazyFunction(uuid4)
    smartapp_id = factory.LazyAttribute(lambda event: event.bot.id)
    data = factory.LazyFunction(build_rpc_data)
    opts = factory.LazyFunction(dict)
    smartapp_api_version = 1
    files = factory.LazyFunction(list)
    chat = factory.SubFactory(ChatFactory)
    sender = factory.SubFactory(UserSenderFactory)
