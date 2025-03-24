from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EventActActions(Enum):
    edit_event = "edit_event"
    delete_event = "delete_event"
    publish_event = "publish_event"
    unpublish_event = "unpublish_event"

class PublishStatus(Enum):
    none = "none"
    true = "true"
    false = "false"

class EventActCbData(CallbackData, prefix="event_act"):
    action: EventActActions
    publish: PublishStatus


def events_act_keyboard(publish) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✏️", callback_data=EventActCbData(action=EventActActions.edit_event, publish=PublishStatus.none).pack())
    builder.button(text="🗑️", callback_data=EventActCbData(action=EventActActions.delete_event, publish=PublishStatus.none).pack())

    if publish:
        builder.button(text="Зняти з публікації", callback_data=EventActCbData(action=EventActActions.unpublish_event, publish=PublishStatus.true).pack())
    else:
        builder.button(text="Опублікувати️", callback_data=EventActCbData(action=EventActActions.publish_event, publish=PublishStatus.false).pack())

    builder.button(text="🔙 Адмін-меню", callback_data="back_main_admin")
    builder.adjust(2,2,1)

    return builder.as_markup()

