# pybotx-smartapp-smart-logger

## Интеграция [pybotx-smart-logger](https://github.com/ExpressApp/pybotx-smart-logger) и [pybotx-smartapp-rpc](https://github.com/ExpressApp/pybotx-smartapp-rpc)

## Установка и использование

1. Устанавливаем библиотеку:  
```bash
poetry add pybotx-smartapp-smart-logger
```

2. Подключаем `pybotx-smart-logger` по инструкции из [README](https://github.com/ExpressApp/pybotx-smart-logger/blob/master/README.md)

3. Подключаем `pybotx-smartapp-rpc` по инструкции из [README](https://github.com/ExpressApp/pybotx-smartapp-rpc/blob/master/README.md)

4. Подключаем хендлер исключений к смартапу

```python
from pybotx_smartapp_smart_logger import smartapp_exception_handler

smartapp = SmartAppRPC(
    routers=...,
    exception_handlers={Exception: smartapp_exception_handler}
)
```

5. Оборачиваем вызов `handle_smartapp_event` в контекстный менеджер:

```python
from pybotx_smartapp_smart_logger import wrap_system_event

@collector.smartapp_event
async def handle_smartapp_event(event: SmartAppEvent, bot: Bot) -> None:
    with wrap_system_event(event, settings.DEBUG):
        await smartapp.handle_smartapp_event(event, bot)
```

## Гдe применять

Добавлять логи лучше везде, где информация из них поможет при диагностике ошибки. Например, здесь выводятся аргументы перед выполением деления.

```python
from pybotx_smart_logger import smart_log

@rpc.method("divide")
async def divide(
    smartapp: SmartApp, rpc_arguments: SumArgs
) -> RPCResultResponse[int]:
    smart_log(f"RPC method `divide` called with args: {rpc_arguments}")
    return RPCResultResponse(result=rpc_arguments.a / rpc_arguments.b)
```

## Разработка

```bash
# форматирование
poetry run ./scripts/format

# статические проверки
poetry run ./scripts/lint

# тесты (параллельно через xdist)
poetry run ./scripts/test
```
