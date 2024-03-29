from typing import Type, Literal
from uuid import UUID

import pytest

from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription, EnumField
from extended_enum.tools import format_to_markdown


class MixedEnum(ExtendedEnum):
    """A combined enumeration in which member values are of different types."""

    CONST1 = EnumField('const1')
    CONST2 = EnumField(1)
    CONST3 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
    NOT_DUPLICATE_CONST3 = EnumField('79ff3431-3e98-4bec-9a4c-63ede2580f83')
    CONST4 = EnumField(BaseExtendedEnumValue(value='const4'))
    CONST5 = EnumField(BaseExtendedEnumValue(value=2))
    CONST6 = EnumField(BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')))
    CONST7 = EnumField(ValueWithDescription(value='const7'))
    CONST8 = EnumField(ValueWithDescription(value=3, description='some const8 description'))


@pytest.mark.parametrize(
    'enum_cls,params,expected',
    [
        {
            'enum_cls': MixedEnum,
            'params': {},  # use default function arguments
            'expected': (
                '* `const1`\n'
                '* `1`\n'
                '* `79ff3431-3e98-4bec-9a4c-63ede2580f83`\n'
                '* `79ff3431-3e98-4bec-9a4c-63ede2580f83`\n'
                '* `const4`\n'
                '* `2`\n'
                '* `e7b4b8ae-2224-47ec-afce-40aeb10b85e2`\n'
                '* `const7`\n'
                '* `3` — some const8 description'
            )
        }.values(),
        {
            'enum_cls': MixedEnum,
            'params': {'delimiter': ';', 'prefix': '', 'value_wrap': ''},
            'expected': (
                'const1;1;79ff3431-3e98-4bec-9a4c-63ede2580f83;79ff3431-3e98-4bec-9a4c-63ede2580f83;const4;2;'
                'e7b4b8ae-2224-47ec-afce-40aeb10b85e2;const7;3 — some const8 description'
            )
        }.values(),
        {
            'enum_cls': Literal[MixedEnum.CONST2, MixedEnum.CONST3, MixedEnum.CONST7, MixedEnum.CONST8],
            'params': {},  # use default function arguments
            'expected': (
                '* `1`\n'
                '* `79ff3431-3e98-4bec-9a4c-63ede2580f83`\n'
                '* `const7`\n'
                '* `3` — some const8 description'
            )
        }.values(),
        {
            'enum_cls': Literal[MixedEnum.CONST2, MixedEnum.CONST3, MixedEnum.CONST7, MixedEnum.CONST8],
            'params': {'delimiter': ';', 'prefix': '', 'value_wrap': ''},
            'expected': '1;79ff3431-3e98-4bec-9a4c-63ede2580f83;const7;3 — some const8 description'
        }.values(),
    ]
)
def test_formatting_to_markdown(enum_cls: Type[ExtendedEnum], params: dict, expected: str):
    """Check the creation of a markdown string using various parameters."""

    assert format_to_markdown(enum_cls=enum_cls, **params) == expected
