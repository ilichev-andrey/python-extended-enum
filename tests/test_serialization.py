from contextlib import AbstractContextManager
from typing import Any, Type
from uuid import UUID

import orjson
import pytest

from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription


class MixedEnum(ExtendedEnum):
    """A combined enumeration in which member values are of different types."""

    CONST1 = 'const1'
    CONST2 = 1
    CONST3 = UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')
    NOT_DUPLICATE_CONST3 = '79ff3431-3e98-4bec-9a4c-63ede2580f83'
    CONST4 = BaseExtendedEnumValue(value='const4')
    CONST5 = BaseExtendedEnumValue(value=2)
    CONST6 = BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'))
    CONST7 = ValueWithDescription(value='const7')
    CONST8 = ValueWithDescription(value=3, description='some const8 description')


@pytest.mark.parametrize(
    'enum_cls,value,expected_enum_member',
    [
        (MixedEnum, 'const1', MixedEnum.CONST1),
        (MixedEnum, 1, MixedEnum.CONST2),
        (MixedEnum, UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'), MixedEnum.CONST3),
        (MixedEnum, '79ff3431-3e98-4bec-9a4c-63ede2580f83', MixedEnum.NOT_DUPLICATE_CONST3),
        (MixedEnum, BaseExtendedEnumValue(value='const4'), MixedEnum.CONST4),
        (MixedEnum, BaseExtendedEnumValue(value=2), MixedEnum.CONST5),
        (MixedEnum, BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')), MixedEnum.CONST6),
        (MixedEnum, ValueWithDescription(value='const7'), MixedEnum.CONST7),
        (MixedEnum, ValueWithDescription(value=3, description='some const8 description'), MixedEnum.CONST8),
        (MixedEnum, ValueWithDescription(value=3), MixedEnum.CONST8),
    ]
)
def test_successful_loads(enum_cls: Type[ExtendedEnum], value: Any, expected_enum_member: ExtendedEnum):
    """
    Check creation of enum constant from simple types.
    Expected:
        - Successful execution because constant exists.
    """

    assert enum_cls(value) == expected_enum_member


@pytest.mark.parametrize(
    'enum_cls,value,context',
    [
        {
            'enum_cls': MixedEnum,
            'value': 'const0',
            'context': pytest.raises(ValueError, match="'const0' is not a valid MixedEnum")
        }.values(),
        {
            'enum_cls': MixedEnum,
            'value': 0,
            'context': pytest.raises(ValueError, match="0 is not a valid MixedEnum")
        }.values(),
        {
            'enum_cls': MixedEnum,
            'value': None,
            'context': pytest.raises(ValueError, match="None is not a valid MixedEnum")
        }.values(),
        {
            'enum_cls': MixedEnum,
            'value': UUID('e51107a4-7f2b-4de3-9034-fdfb0a50e30f'),
            'context': pytest.raises(
                ValueError,
                match=r"UUID\('e51107a4-7f2b-4de3-9034-fdfb0a50e30f'\) is not a valid MixedEnum"
            )
        }.values(),
        {
            'enum_cls': MixedEnum,
            'value': 'e51107a4-7f2b-4de3-9034-fdfb0a50e30f',
            'context': pytest.raises(
                ValueError,
                match="'e51107a4-7f2b-4de3-9034-fdfb0a50e30f' is not a valid MixedEnum"
            )
        }.values(),
    ]
)
def test_error_loads(enum_cls: Type[ExtendedEnum], value: Any, context: AbstractContextManager):
    """
    Check creation of enum constant from simple types.
    Expected:
        - Execution failed because the constant does NOT exist.
    """
    with context:
        enum_cls(value)


@pytest.mark.parametrize(
    'obj,expected',
    [
        {
            'obj': {
                MixedEnum.CONST1.name: MixedEnum.CONST1,
                MixedEnum.CONST2.name: MixedEnum.CONST2,
                MixedEnum.CONST3.name: MixedEnum.CONST3,
                MixedEnum.NOT_DUPLICATE_CONST3.name: MixedEnum.NOT_DUPLICATE_CONST3,
                MixedEnum.CONST4.name: MixedEnum.CONST4,
                MixedEnum.CONST5.name: MixedEnum.CONST5,
                MixedEnum.CONST6.name: MixedEnum.CONST6,
                MixedEnum.CONST7.name: MixedEnum.CONST7,
                MixedEnum.CONST8.name: MixedEnum.CONST8,
            },
            'expected': {
                'CONST1': 'const1',
                'CONST2': 1,
                'CONST3': '79ff3431-3e98-4bec-9a4c-63ede2580f83',
                'NOT_DUPLICATE_CONST3': '79ff3431-3e98-4bec-9a4c-63ede2580f83',
                'CONST4': 'const4',
                'CONST5': 2,
                'CONST6': 'e7b4b8ae-2224-47ec-afce-40aeb10b85e2',
                'CONST7': 'const7',
                'CONST8': 3,
            }
        }.values(),
    ]
)
def test_conversion_to_json(obj: Any, expected: Any):
    """
    Check the conversion to JSON string.
    Expected:
        - Successfully converting enum members to JSON.
    """

    assert orjson.dumps(obj).decode() == orjson.dumps(expected).decode()
