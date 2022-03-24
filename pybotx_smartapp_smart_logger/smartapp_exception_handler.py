from loguru import logger
from pybotx_smart_logger import log_levels
from pybotx_smart_logger.contextvars import get_debug_enabled
from pybotx_smart_logger.logger import flush_accumulated_logs
from pybotx_smart_logger.output import attach_log_source, log_system_event
from pybotx_smartapp_rpc.models.errors import RPCError
from pybotx_smartapp_rpc.models.responses import RPCErrorResponse
from pybotx_smartapp_rpc.smartapp import SmartApp


async def smartapp_exception_handler(
    exc: Exception,
    smartapp: SmartApp,
) -> RPCErrorResponse:
    assert smartapp.event
    assert smartapp.event.raw_command

    if not get_debug_enabled():
        log_system_event(
            smartapp.event.raw_command,
            "Error while processing incoming SmartApp event:",
            log_levels.ERROR,
        )
        flush_accumulated_logs(log_levels.ERROR)

    logger.exception(attach_log_source(""))

    return RPCErrorResponse(
        errors=[RPCError(reason="Internal error", id=exc.__class__.__name__.upper())],
    )
