from collections.abc import Callable
from unittest.mock import AsyncMock

import pytest
from pybotx import SmartAppEvent
from pybotx_smart_logger import smart_log
from pybotx_smartapp_rpc import RPCResultResponse, RPCRouter, SmartApp, SmartAppRPC

from pybotx_smartapp_smart_logger import smartapp_exception_handler, wrap_system_event


async def test_rpc_call_error_logged(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
    loguru_caplog: pytest.LogCaptureFixture,
) -> None:
    # - Arrange -
    rpc = RPCRouter()

    @rpc.method("get_api_version")
    async def get_api_version(smartapp: SmartApp) -> RPCResultResponse[int]:
        smart_log("Hello from `get_api_version`!")
        raise ValueError("Test Error")

    smartapp_rpc = SmartAppRPC(
        routers=[rpc],
        exception_handlers={Exception: smartapp_exception_handler},
    )
    event = smartapp_event_factory("get_api_version")

    # - Act -
    with wrap_system_event(event):
        await smartapp_rpc.handle_smartapp_event(event, bot)

    # - Assert -
    assert "Hello from `get_api_version`!" in loguru_caplog.text
    assert "Error while processing incoming SmartApp event:" in loguru_caplog.text
    assert "'method': 'get_api_version'" in loguru_caplog.text
    assert "ValueError: Test Error" in loguru_caplog.text


async def test_rpc_call_error_logged_with_debug(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
    loguru_caplog: pytest.LogCaptureFixture,
) -> None:
    # - Arrange -
    rpc = RPCRouter()

    @rpc.method("get_api_version")
    async def get_api_version(smartapp: SmartApp) -> RPCResultResponse[int]:
        smart_log("Hello from `get_api_version`!")
        raise ValueError("Test Error")

    smartapp_rpc = SmartAppRPC(
        routers=[rpc],
        exception_handlers={Exception: smartapp_exception_handler},
    )
    event = smartapp_event_factory("get_api_version")

    # - Act -
    with wrap_system_event(event, debug=True):
        await smartapp_rpc.handle_smartapp_event(event, bot)

    # - Assert -
    assert "Processing incoming event:" in loguru_caplog.text
    assert "'method': 'get_api_version'" in loguru_caplog.text
    assert "Hello from `get_api_version`!" in loguru_caplog.text
    assert "ValueError: Test Error" in loguru_caplog.text


async def test_rpc_call_logs_empty(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
    loguru_caplog: pytest.LogCaptureFixture,
) -> None:
    # - Arrange -
    rpc = RPCRouter()

    @rpc.method("get_api_version")
    async def get_api_version(smartapp: SmartApp) -> RPCResultResponse[int]:
        smart_log("Hello from `get_api_version`!")
        return RPCResultResponse(result=42)

    smartapp_rpc = SmartAppRPC(
        routers=[rpc],
        exception_handlers={Exception: smartapp_exception_handler},
    )
    event = smartapp_event_factory("get_api_version")

    # - Act -
    with wrap_system_event(event):
        await smartapp_rpc.handle_smartapp_event(event, bot)

    # - Assert -
    assert "Processing incoming event:" not in loguru_caplog.text
    assert "'method': 'get_api_version'" not in loguru_caplog.text
    assert "Hello from `get_api_version`!" not in loguru_caplog.text


async def test_rpc_call_logs_with_debug(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
    loguru_caplog: pytest.LogCaptureFixture,
) -> None:
    # - Arrange -
    rpc = RPCRouter()

    @rpc.method("get_api_version")
    async def get_api_version(smartapp: SmartApp) -> RPCResultResponse[int]:
        smart_log("Hello from `get_api_version`!")
        return RPCResultResponse(result=42)

    smartapp_rpc = SmartAppRPC(
        routers=[rpc],
        exception_handlers={Exception: smartapp_exception_handler},
    )
    event = smartapp_event_factory("get_api_version")

    # - Act -
    with wrap_system_event(event, debug=True):
        await smartapp_rpc.handle_smartapp_event(event, bot)

    # - Assert -
    assert "Processing incoming event:" in loguru_caplog.text
    assert "'method': 'get_api_version'" in loguru_caplog.text
    assert "Hello from `get_api_version`!" in loguru_caplog.text


async def test_rpc_call_error_with_empty_raw_command(
    smartapp_event_factory: Callable[..., SmartAppEvent],
    bot: AsyncMock,
    loguru_caplog: pytest.LogCaptureFixture,
) -> None:
    # - Arrange -
    rpc = RPCRouter()

    @rpc.method("get_api_version")
    async def get_api_version(smartapp: SmartApp) -> RPCResultResponse[int]:
        smart_log("Hello from `get_api_version`!")
        raise ValueError("Test Error")

    smartapp_rpc = SmartAppRPC(
        routers=[rpc],
        exception_handlers={Exception: smartapp_exception_handler},
    )
    event = smartapp_event_factory("get_api_version")
    event.raw_command = None

    # - Act -
    with wrap_system_event(event):
        await smartapp_rpc.handle_smartapp_event(event, bot)

    # - Assert -
    assert "Hello from `get_api_version`!" in loguru_caplog.text
    assert "ValueError: Test Error" in loguru_caplog.text
