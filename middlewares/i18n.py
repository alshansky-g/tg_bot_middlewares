from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import random

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')
        if user is None:
            return await handler(event, data)

        user_lang = ['en', 'ru']
        translations = data.get("translations")

        i18n = random.choice(user_lang)
        data["i18n"] = translations[i18n]  #type: ignore

        return await handler(event, data)
