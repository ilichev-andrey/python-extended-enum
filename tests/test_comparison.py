from uuid import UUID

from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription, EnumField


class MixedEnum1(ExtendedEnum):
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


class MixedEnum2(ExtendedEnum):
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


def test_different_classes():
    """
    Comparison of identical values from different classes is checked.
    Expected:
        - Identical values located in different classes are NOT equal
    """

    for item1 in MixedEnum1:
        item2 = getattr(MixedEnum2, item1.name)
        assert item1 == item1
        assert item1.value == item2.value
        assert item1 != item2


def test_different_origins():
    """
    Comparison of identical values of different origins is checked.
    Expected:
        - Values that do not belong to the same class are NOT equal.
    """

    origins = {
        'CONST1': 'const1',
        'CONST2': 1,
        'CONST3': UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'),
        'NOT_DUPLICATE_CONST3': '79ff3431-3e98-4bec-9a4c-63ede2580f83',
        'CONST4': 'const4',
        'CONST5': 2,
        'CONST6': UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'),
        'CONST7': 'const7',
        'CONST8': 3,
    }
    for item in MixedEnum1:
        assert item != item.value
        origin = origins[item.name]
        assert item.value == origin
        assert item != origin

    origins = {
        'CONST4': BaseExtendedEnumValue(value='const4'),
        'CONST5': BaseExtendedEnumValue(value=2),
        'CONST6': BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')),
        'CONST7': ValueWithDescription(value='const7'),
        'CONST8': ValueWithDescription(value=3, description='some const8 description'),
    }
    for name, origin in origins.items():
        item = getattr(MixedEnum1, name)
        assert item.value == origin.value
        assert item != origin
