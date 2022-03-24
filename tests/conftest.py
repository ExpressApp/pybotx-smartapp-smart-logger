import logging
from typing import Any, Callable, Dict, Generator, Optional
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from loguru import logger
from pybotx import (
    Bot,
    BotAccount,
    Chat,
    ChatTypes,
    SmartAppEvent,
    UserDevice,
    UserSender,
)


@pytest.fixture
def bot_id() -> UUID:
    return UUID("24348246-6791-4ac0-9d86-b948cd6a0e46")


@pytest.fixture
def ref() -> UUID:
    return UUID("6fafda2c-6505-57a5-a088-25ea5d1d0364")


@pytest.fixture
def chat_id() -> UUID:
    return UUID("dea55ee4-7a9f-5da0-8c73-079f400ee517")


@pytest.fixture
def host() -> str:
    return "cts.example.com"


@pytest.fixture
def smartapp_event_factory(
    bot_id: UUID,
    ref: UUID,
    chat_id: UUID,
    host: str,
) -> Callable[..., SmartAppEvent]:
    def factory(
        method: str,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> SmartAppEvent:
        smartapp_data: Dict[str, Any] = {
            "type": "smartapp_rpc",
            "method": method,
        }
        if params is not None:
            smartapp_data["params"] = params

        return SmartAppEvent(
            ref=ref,
            smartapp_id=bot_id,
            bot=BotAccount(
                id=bot_id,
                host=host,
            ),
            data=smartapp_data,
            opts={},
            smartapp_api_version=1,
            files=[],
            sender=UserSender(
                huid=uuid4(),
                ad_login=None,
                ad_domain=None,
                username=None,
                is_chat_admin=True,
                is_chat_creator=True,
                device=UserDevice(
                    manufacturer=None,
                    device_name=None,
                    os=None,
                    pushes=None,
                    timezone=None,
                    permissions=None,
                    platform=None,
                    platform_package_id=None,
                    app_version=None,
                    locale=None,
                ),
            ),
            chat=Chat(
                id=chat_id,
                type=ChatTypes.GROUP_CHAT,
            ),
            raw_command={
                "async_files": [],
                "attachments": [],
                "bot_id": "0450ca08-638e-5d26-a1be-2cc9f2b7fb57",
                "command": {
                    "body": "system:smartapp_event",
                    "command_type": "system",
                    "data": {
                        "data": {
                            "method": "get_api_version",
                            "params": {},
                            "type": "smartapp_rpc",
                        },
                        "opts": {},
                        "ref": "24f7a94f-a030-454a-9cd5-fde6d6c4407a",
                        "smartapp_api_version": 1,
                        "smartapp_id": "b8ee9811-45b1-5660-b7a1-15fb22111d4c",
                    },
                    "metadata": {},
                },
                "entities": [],
                "from": {
                    "ad_domain": None,
                    "ad_login": None,
                    "app_version": "2.0.30",
                    "chat_type": "chat",
                    "device": "Chrome 98.0",
                    "device_meta": {
                        "permissions": {"microphone": True, "notifications": True},
                        "pushes": False,
                        "timezone": "Europe/Samara",
                    },
                    "device_software": "macOS 10.15.7",
                    "group_chat_id": "5847680e-b9f1-0e2e-3ea8-96968232f585",
                    "host": "cts31st.ccsteam.ru",
                    "is_admin": True,
                    "is_creator": True,
                    "locale": "ru",
                    "manufacturer": "Google",
                    "platform": "web",
                    "platform_package_id": "ru.unlimitedtech.express",
                    "user_huid": "e0a9f01f-fc40-584e-8909-836da023e8c9",
                    "username": None,
                },
                "proto_version": 4,
                "source_sync_id": None,
                "sync_id": "90e722fe-cf55-5e53-a63c-f35cde8e3523",
            },
        )

    return factory


@pytest.fixture
def bot() -> AsyncMock:
    return AsyncMock(spec=Bot)


@pytest.fixture()
def loguru_caplog(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture, None, None]:
    # https://github.com/Delgan/loguru/issues/59

    class PropogateHandler(logging.Handler):  # noqa: WPS431
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message}")
    yield caplog
    logger.remove(handler_id)
