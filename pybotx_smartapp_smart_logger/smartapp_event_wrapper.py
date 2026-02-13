from collections.abc import Generator
from contextlib import contextmanager
from pprint import pformat

from pybotx import SmartAppEvent
from pybotx_smart_logger import smart_log
from pybotx_smart_logger.contextvars import (
    clear_accumulated_logs,
    get_debug_enabled,
    get_grouping_enabled,
    set_debug_enabled,
    set_grouping_enabled,
)


def _restore_context(
    previous_debug: bool,
    previous_grouping: bool,
    debug: bool,
) -> None:
    if not debug:
        clear_accumulated_logs()

    set_grouping_enabled(previous_grouping)
    set_debug_enabled(previous_debug)


@contextmanager
def wrap_system_event(
    event: SmartAppEvent,
    debug: bool = False,
) -> Generator[None, None, None]:
    previous_debug = get_debug_enabled()
    previous_grouping = get_grouping_enabled()

    clear_accumulated_logs()
    set_debug_enabled(debug)
    set_grouping_enabled(False)

    context = pformat(event.raw_command, sort_dicts=True)
    smart_log(f"Processing incoming event:\n{context}")

    try:
        yield
    finally:
        _restore_context(previous_debug, previous_grouping, debug)
