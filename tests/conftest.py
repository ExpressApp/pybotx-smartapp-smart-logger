import logging
from collections.abc import Callable, Generator
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest
from loguru import logger
from pybotx import Bot, SmartAppEvent

from tests.factories import SmartAppEventFactory, build_raw_command, build_rpc_data


@pytest.fixture
def smartapp_event_factory() -> Callable[..., SmartAppEvent]:
    def factory(
        method: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> SmartAppEvent:
        return cast(
            SmartAppEvent,
            SmartAppEventFactory(
                data=build_rpc_data(method=method, params=params),
                raw_command=build_raw_command(method=method, params=params),
            ),
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

    class PropogateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message}")
    yield caplog
    logger.remove(handler_id)
