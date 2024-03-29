# noqa: D100
from typing import Any, get_origin, Literal, get_args

from extended_enum import ExtendedEnum, BaseExtendedEnumValue


def format_to_markdown(enum_cls: Any, delimiter: str = '\n', prefix: str = '*', value_wrap: str = '`') -> str:
    """Convert ExtendedEnum to a markdown string."""
    if get_origin(enum_cls) is not Literal and issubclass(enum_cls, ExtendedEnum):
        extended_values = enum_cls.get_extended_values()
    else:
        extended_values = (
            member.extended_value
            for member in get_args(enum_cls)
            if isinstance(member, ExtendedEnum)
        )

    items = (
        format_value_to_markdown(extended_value=value, prefix=prefix, value_wrap=value_wrap)
        for value in extended_values
    )
    return delimiter.join(items)


def format_value_to_markdown(extended_value: BaseExtendedEnumValue, prefix: str = '*', value_wrap: str = '`') -> str:
    """Convert ExtendedEnum member to a markdown string."""
    description = ''
    if hasattr(extended_value, 'description') and extended_value.description is not None:  # noqa: WPS421
        description = ' — {description}'.format(description=extended_value.description)
    if prefix:
        prefix = f'{prefix} '
    value = ''.join((value_wrap, str(extended_value.value), value_wrap))
    return ''.join((prefix, value, description))
