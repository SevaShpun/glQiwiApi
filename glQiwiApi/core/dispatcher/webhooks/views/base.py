import abc
import logging
from typing import Generic, TypeVar, Type, TYPE_CHECKING as MYPY, Any

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import ValidationError

from glQiwiApi.core.dispatcher.implementation import Dispatcher
from glQiwiApi.core.dispatcher.webhooks.dto.errors import WebhookAPIError
from glQiwiApi.core.dispatcher.webhooks.services.collision_detector import UnexpectedCollision, \
    AbstractCollisionDetector

if MYPY:
    from glQiwiApi.types.base import HashableBase  # pragma: no cover  # noqa

try:
    import orjson as json
except ImportError:
    import json  # type: ignore

Event = TypeVar("Event", bound="HashableBase")

logger = logging.getLogger("glQiwiApi.webhooks.base")


class BaseWebhookView(web.View, Generic[Event]):
    """
    Base webhook view for processing events
    You can make own view and than use it in code,
    just inheriting this base class

    """

    def __init__(
            self,
            request: Request,
            dispatcher: Dispatcher,
            collision_detector: AbstractCollisionDetector[Any],
            event_cls: Type[Event],
            secret_key: str
    ) -> None:
        super().__init__(request)
        self._dispatcher = dispatcher
        self._collision_detector = collision_detector
        self._event_cls = event_cls
        self._secret_key = secret_key

    @abc.abstractmethod
    async def ok_response(self) -> web.Response:
        pass

    async def get(self) -> web.Response:
        return web.Response(text="")

    async def post(self) -> web.Response:
        event = await self.parse_raw_request()

        try:
            self._collision_detector.remember_processed_object(event)
        except UnexpectedCollision:
            logger.debug("Detect collision on event %s", event)
            return await self.ok_response()

        self._validate_event_signature(event)
        await self.process_event(event)
        return await self.ok_response()

    async def parse_raw_request(self) -> Event:
        """Parse raw update and return pydantic model"""
        data = await self.request.json(loads=json.loads)
        try:
            if isinstance(data, str):
                return self._event_cls.parse_raw(data)
            elif isinstance(data, dict):  # pragma: no cover
                return self._event_cls.parse_obj(data)
            else:
                raise ValidationError  # pragma: no cover
        except ValidationError as ex:
            raise web.HTTPBadRequest(
                body=WebhookAPIError(
                    status="Validation error", detail=ex.json(indent=4)
                ).json(),
                content_type="application/json"
            )

    @abc.abstractmethod
    def _validate_event_signature(self, update: Event) -> None:
        raise NotImplementedError

    async def process_event(self, event: Event) -> None:
        await self._dispatcher.process_event(event)