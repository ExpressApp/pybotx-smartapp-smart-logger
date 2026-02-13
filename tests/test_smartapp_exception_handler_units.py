from collections.abc import Callable
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from freezegun import freeze_time
from pybotx import SmartAppEvent
from pybotx_smartapp_rpc import SmartApp

from pybotx_smartapp_smart_logger.smartapp_exception_handler import (
    _stringify_raw_command,
)


def test_stringify_raw_command_returns_none_for_empty_event(bot: AsyncMock) -> None:
    smartapp = SmartApp(
        bot=bot,
        bot_id=uuid4(),
        chat_id=uuid4(),
        event=None,
    )

    assert _stringify_raw_command(smartapp) is None


@freeze_time("2026-02-13 15:30:10")
def test_stringify_raw_command_formats_payload(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
) -> None:
    event = smartapp_event_factory("get_api_version")
    event.raw_command = {
        "z": 1,
        "a": {
            "timestamp": datetime.now(),
        },
    }
    smartapp = SmartApp(
        bot=bot,
        bot_id=event.bot.id,
        chat_id=event.chat.id,
        event=event,
    )

    assert _stringify_raw_command(smartapp) == (
        "{'a': {'timestamp': FakeDatetime(2026, 2, 13, 15, 30, 10)}, 'z': 1}"
    )
