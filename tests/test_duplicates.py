from enum import unique
from uuid import UUID

import pytest

from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ExtendedEnumType, ValueWithDescription, EnumField


class StringEnum(ExtendedEnum):
    """An enumeration in which the values of all members are strings."""

    CONST1 = EnumField('const1')
    DUPLICATE_CONST1 = EnumField('const1')


class IntegerEnum(ExtendedEnum):
    """An enumeration in which the values of all members are integers."""

    CONST1 = EnumField(1)
    DUPLICATE_CONST1 = EnumField(1)


class UUIDEnum(ExtendedEnum):
    """An enumeration in which the values of all members are UUID."""

    CONST1 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
    DUPLICATE_CONST1 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
    NOT_DUPLICATE_CONST1 = EnumField('79ff3431-3e98-4bec-9a4c-63ede2580f83')


class DetailedEnum1(ExtendedEnum):
    """An enumeration containing the values of all members of the extended type."""

    CONST1 = EnumField(BaseExtendedEnumValue(value='const1'))
    DUPLICATE_CONST1 = EnumField(BaseExtendedEnumValue(value='const1'))

    CONST2 = EnumField(BaseExtendedEnumValue(value=2))
    DUPLICATE_CONST2 = EnumField(BaseExtendedEnumValue(value=2))

    CONST3 = EnumField(BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')))
    DUPLICATE_CONST3 = EnumField(BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')))


class DetailedEnum2(ExtendedEnum):
    """An enumeration containing the values of all members of the extended type."""

    CONST1 = EnumField(ValueWithDescription(value='const1', description='some description'))
    DUPLICATE_CONST1 = EnumField(ValueWithDescription(value='const1'))
    DUPLICATE_CONST1_2 = EnumField(ValueWithDescription(value='const1', description='some description'))
    NOT_DUPLICATE_CONST1 = EnumField(ValueWithDescription(value='other_const', description='some description'))

    CONST2 = EnumField(ValueWithDescription(value=2, description='some description'))
    DUPLICATE_CONST2 = EnumField(ValueWithDescription(value=2))
    DUPLICATE_CONST2_2 = EnumField(ValueWithDescription(value=2, description='some description'))

    CONST3 = EnumField(ValueWithDescription(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'), description='some description'))
    DUPLICATE_CONST3 = EnumField(ValueWithDescription(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')))
    DUPLICATE_CONST3_2 = EnumField(ValueWithDescription(
        value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'), description='some description'
    ))


class MixedEnum(ExtendedEnum):
    """A combined enumeration in which member values are of different types."""

    CONST1 = EnumField('const1')
    DUPLICATE_CONST1 = EnumField('const1')

    CONST2 = EnumField(1)
    DUPLICATE_CONST2 = EnumField(1)
    NOT_DUPLICATE_CONST2 = EnumField('1')

    CONST3 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
    DUPLICATE_CONST3 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
    NOT_DUPLICATE_CONST3 = EnumField('79ff3431-3e98-4bec-9a4c-63ede2580f83')

    CONST4 = EnumField(BaseExtendedEnumValue(value='const4'))
    DUPLICATE_CONST4 = EnumField(BaseExtendedEnumValue(value='const4'))

    CONST5 = EnumField(BaseExtendedEnumValue(value=2))
    DUPLICATE_CONST5 = EnumField(BaseExtendedEnumValue(value=2))
    NOT_DUPLICATE_CONST5 = EnumField(BaseExtendedEnumValue(value='2'))

    CONST6 = EnumField(BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')))
    DUPLICATE_CONST6 = EnumField(BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')))

    DUPLICATE_CONST1_2 = EnumField(BaseExtendedEnumValue(value='const1'))
    DUPLICATE_CONST2_2 = EnumField(BaseExtendedEnumValue(value=1))
    DUPLICATE_CONST3_2 = EnumField(BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')))


@pytest.mark.parametrize(
    'enum_cls,expected',
    [
        {
            'enum_cls': StringEnum,
            'expected': 'DUPLICATE_CONST1 -> CONST1'
        }.values(),
        {
            'enum_cls': IntegerEnum,
            'expected': 'DUPLICATE_CONST1 -> CONST1'
        }.values(),
        {
            'enum_cls': UUIDEnum,
            'expected': 'DUPLICATE_CONST1 -> CONST1'
        }.values(),
        {
            'enum_cls': DetailedEnum1,
            'expected': 'DUPLICATE_CONST1 -> CONST1, DUPLICATE_CONST2 -> CONST2'
        }.values(),
        {
            'enum_cls': DetailedEnum2,
            'expected': (
                'DUPLICATE_CONST1 -> CONST1, '
                'DUPLICATE_CONST1_2 -> CONST1, '
                'DUPLICATE_CONST2 -> CONST2, '
                'DUPLICATE_CONST2_2 -> CONST2, '
                'DUPLICATE_CONST3 -> CONST3, '
                'DUPLICATE_CONST3_2 -> CONST3'
            )
        }.values(),
        {
            'enum_cls': MixedEnum,
            'expected': (
                'DUPLICATE_CONST1 -> CONST1, '
                'DUPLICATE_CONST2 -> CONST2, '
                'DUPLICATE_CONST3 -> CONST3, '
                'DUPLICATE_CONST4 -> CONST4, '
                'DUPLICATE_CONST5 -> CONST5, '
                'DUPLICATE_CONST6 -> CONST6, '
                'DUPLICATE_CONST1_2 -> CONST1, '
                'DUPLICATE_CONST2_2 -> CONST2, '
                'DUPLICATE_CONST3_2 -> CONST3'
            )
        }.values(),
    ]
)
def test_unique_values(enum_cls: ExtendedEnumType, expected: str):
    """
    Checks whether an exception occurs when calling the `enum.unique`.
    Expected:
        - Exception raised.
        - Exclusion includes only those fields that are duplicated.
    """

    with pytest.raises(ValueError, match=f'duplicate values found in <.+>: {expected}'):
        unique(enum_cls)
