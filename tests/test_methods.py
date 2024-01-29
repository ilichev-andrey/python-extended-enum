from typing import Type, Tuple
from uuid import UUID

import pytest

from extended_enum import (
    ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription, SimpleValueType, ExtendedEnumValueType, EnumField
)


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
    'enum_cls,expected',
    [
        {
            'enum_cls': MixedEnum,
            'expected': (
                'const1',
                1,
                UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'),
                '79ff3431-3e98-4bec-9a4c-63ede2580f83',
                'const4',
                2,
                UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'),
                'const7',
                3
            )
        }.values(),
    ]
)
def test_get_values(enum_cls: Type[ExtendedEnum], expected: Tuple[SimpleValueType, ...]):
    """
    Check out the function that gets all the simple values of an enum.
    Expected:
        - A tuple of simple enumeration values.
    """

    actual = enum_cls.get_values()
    assert isinstance(actual, tuple)
    assert actual == expected


@pytest.mark.parametrize(
    'enum_cls,expected',
    [
        {
            'enum_cls': MixedEnum,
            'expected': (
                BaseExtendedEnumValue(value='const1'),
                BaseExtendedEnumValue(value=1),
                BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')),
                BaseExtendedEnumValue(value='79ff3431-3e98-4bec-9a4c-63ede2580f83'),
                BaseExtendedEnumValue(value='const4'),
                BaseExtendedEnumValue(value=2),
                BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')),
                ValueWithDescription(value='const7'),
                ValueWithDescription(value=3, description='some const8 description'),
            )
        }.values(),
    ]
)
def test_get_extended_values(enum_cls: Type[ExtendedEnum], expected: Tuple[ExtendedEnumValueType, ...]):
    """
    Check out the function that gets all the extended values of an enum.
    Expected:
        - A tuple of extended enumeration values.
    """

    actual = enum_cls.get_extended_values()
    assert isinstance(actual, tuple)
    assert actual == expected

    actual = [repr(item) for item in actual]
    expected = [repr(item) for item in expected]
    assert actual == expected


@pytest.mark.parametrize(
    'enum_cls,expected',
    [
        {
            'enum_cls': MixedEnum,
            'expected': {
                'CONST1': MixedEnum.CONST1,
                'CONST2': MixedEnum.CONST2,
                'CONST3': MixedEnum.CONST3,
                'NOT_DUPLICATE_CONST3': MixedEnum.NOT_DUPLICATE_CONST3,
                'CONST4': MixedEnum.CONST4,
                'CONST5': MixedEnum.CONST5,
                'CONST6': MixedEnum.CONST6,
                'CONST7': MixedEnum.CONST7,
                'CONST8': MixedEnum.CONST8,
            }
        }.values()
    ]
)
def test_get_members(enum_cls: Type[ExtendedEnum], expected: Tuple[ExtendedEnumValueType, ...]):
    """
    Check out the function that gets all the members of an enum.
    Expected:
        - Dictionary in which the key is the name of the constant, and the value is the Enum class constant itself.
    """
    assert dict(enum_cls.get_members()) == expected


@pytest.mark.parametrize(
    'enum_member,expected',
    [
        (MixedEnum.CONST1, 'const1'),
        (MixedEnum.CONST2, 1),
        (MixedEnum.CONST3, UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')),
        (MixedEnum.NOT_DUPLICATE_CONST3, '79ff3431-3e98-4bec-9a4c-63ede2580f83'),
        (MixedEnum.CONST4, 'const4'),
        (MixedEnum.CONST5, 2),
        (MixedEnum.CONST6, UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')),
        (MixedEnum.CONST7, 'const7'),
        (MixedEnum.CONST8, 3),
    ]
)
def test_value(enum_member: ExtendedEnum, expected: SimpleValueType):
    """Check getting a simple enum value."""

    assert enum_member.value == expected


@pytest.mark.parametrize(
    'enum_member,expected',
    [
        (MixedEnum.CONST1, BaseExtendedEnumValue(value='const1')),
        (MixedEnum.CONST2, BaseExtendedEnumValue(value=1)),
        (MixedEnum.CONST3, BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))),
        (MixedEnum.NOT_DUPLICATE_CONST3, BaseExtendedEnumValue(value='79ff3431-3e98-4bec-9a4c-63ede2580f83')),
        (MixedEnum.CONST4, BaseExtendedEnumValue(value='const4')),
        (MixedEnum.CONST5, BaseExtendedEnumValue(value=2)),
        (MixedEnum.CONST6, BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'))),
        (MixedEnum.CONST7, ValueWithDescription(value='const7')),
        (MixedEnum.CONST8, ValueWithDescription(value=3, description='some const8 description')),
    ]
)
def test_extended_value(enum_member: ExtendedEnum, expected: ExtendedEnumValueType):
    """Check getting a extended enum value."""

    assert enum_member.extended_value == expected
