from pprint import pformat

from loguru import logger
from pybotx_smart_logger import log_levels, smart_log
from pybotx_smart_logger.contextvars import get_debug_enabled
from pybotx_smart_logger.logger import flush_accumulated_logs
from pybotx_smartapp_rpc.models.errors import RPCError
from pybotx_smartapp_rpc.models.responses import RPCErrorResponse
from pybotx_smartapp_rpc.smartapp import SmartApp


def _stringify_raw_command(smartapp: SmartApp) -> str | None:
    if smartapp.event is None or smartapp.event.raw_command is None:
        return None

    return pformat(smartapp.event.raw_command, sort_dicts=True)


async def smartapp_exception_handler(
    exc: Exception,
    smartapp: SmartApp,
) -> RPCErrorResponse:
    if not get_debug_enabled():
        smart_log("Error while processing incoming SmartApp event:")

        raw_command = _stringify_raw_command(smartapp)
        if raw_command is not None:
            smart_log(raw_command)

        flush_accumulated_logs(log_levels.ERROR)

    logger.exception("")

    return RPCErrorResponse(
        errors=[RPCError(reason="Internal error", id=exc.__class__.__name__.upper())],
    )
