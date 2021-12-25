from .core import (
    AbstractBillHandler,
    AbstractTransactionHandler,
    AbstractTransactionWebhookHandler,
    BaseFilter,
    Handler,
    LambdaBasedFilter,
    async_as_sync,
    execute_async_as_sync,
)
from .qiwi import QiwiMaps, QiwiWrapper
from .yoo_money import YooMoneyAPI

try:
    import uvloop

    uvloop.install()  # pragma: no cover
except ImportError:
    pass

__version__ = "2.0.0b1"

__all__ = (
    "QiwiWrapper",
    "YooMoneyAPI",
    "QiwiMaps",
    "execute_async_as_sync",
    "async_as_sync",
    "LambdaBasedFilter",
    "BaseFilter",
    # class-based handlers
    "AbstractBillHandler",
    "AbstractTransactionHandler",
    "AbstractTransactionWebhookHandler",
    "Handler",
    # other
    "__version__",
)
