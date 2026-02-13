from collections.abc import Callable

import pytest
from pybotx import SmartAppEvent
from pybotx_smart_logger.contextvars import (
    get_debug_enabled,
    get_grouping_enabled,
    set_debug_enabled,
    set_grouping_enabled,
)
from pytest_mock import MockerFixture

from pybotx_smartapp_smart_logger import wrap_system_event


@pytest.mark.parametrize(
    ("debug", "expected_clear_calls"),
    (
        (False, 2),
        (True, 1),
    ),
)
def test_wrap_system_event_restores_context(
    debug: bool,
    expected_clear_calls: int,
    smartapp_event_factory: Callable[..., SmartAppEvent],
    mocker: MockerFixture,
) -> None:
    event = smartapp_event_factory("get_api_version")
    clear_accumulated_logs = mocker.patch(
        "pybotx_smartapp_smart_logger.smartapp_event_wrapper.clear_accumulated_logs",
    )
    smart_log = mocker.patch(
        "pybotx_smartapp_smart_logger.smartapp_event_wrapper.smart_log",
    )

    set_debug_enabled(True)
    set_grouping_enabled(True)

    try:
        with wrap_system_event(event, debug=debug):
            assert get_debug_enabled() is debug
            assert get_grouping_enabled() is False

        assert get_debug_enabled() is True
        assert get_grouping_enabled() is True
        assert clear_accumulated_logs.call_count == expected_clear_calls
        smart_log.assert_called_once()
    finally:
        set_grouping_enabled(False)
        set_debug_enabled(False)
