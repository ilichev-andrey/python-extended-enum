import enum
from dataclasses import dataclass, field
from types import DynamicClassAttribute
from typing import Union, Optional, TypeVar, Any, cast, Tuple, Dict, ClassVar
from uuid import UUID

SimpleValueType = Union[UUID, int, str]
ExtendedEnumValueType = TypeVar('ExtendedEnumValueType', bound='BaseExtendedEnumValue')
ExtendedEnumType = TypeVar('ExtendedEnumType', bound='ExtendedEnum')


@dataclass(frozen=True)
class BaseExtendedEnumValue:
    """
    Base class for the extended form of the value of each enumeration member.

    Examples:
        1. Create your own class that will be used as the enum value.

        ```python
        from dataclasses import dataclass, field
        from extended_enum import BaseExtendedEnumValue
        from typing import Optional

        @dataclass(frozen=True)
        class SomeExtendedEnumValue(BaseExtendedEnumValue):
            display_name: str = field(compare=False)
            description: Optional[str] = field(default=None, compare=False)
        ```
    """

    value: SimpleValueType


@dataclass(frozen=True)
class ValueWithDescription(BaseExtendedEnumValue):
    """An expanded form of an enumeration value that contains a description of the value."""

    description: Optional[str] = field(default=None, compare=False)


class ExtendedEnum(enum.Enum):
    """
    A class that extends the capabilities of the standard Enum.

    Examples:
        1. An enumeration containing the values of all members of the extended type.

        ```python
        from enum import unique
        from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription

        class DetailedEnum(ExtendedEnum):
            CONST1 = BaseExtendedEnumValue(value='const1')
            CONST2 = ValueWithDescription(value='const2', description='some description 2')
            CONST3 = ValueWithDescription(value='const3', description='some description 3')

        unique(DetailedEnum)
        ```

        2. A combined enumeration in which member values are of different types.

        ```python
        from uuid import UUID
        from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription

        class MixedEnum(ExtendedEnum):
            CONST1 = 'const1'
            CONST2 = 1
            CONST3 = UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')
            NOT_DUPLICATE_CONST3 = '79ff3431-3e98-4bec-9a4c-63ede2580f83'
            CONST4 = BaseExtendedEnumValue(value='const4')
            CONST5 = BaseExtendedEnumValue(value=2)
            CONST6 = BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'))
            CONST7 = ValueWithDescription(value='const7')
            CONST8 = ValueWithDescription(value=3, description='some const8 description')
        ```

        3. An enumeration in which the values of all members are strings.

        ```python
        from extended_enum import ExtendedEnum

        class StringEnum(ExtendedEnum):
            CONST1 = 'const1'
            CONST2 = 'const2'
            CONST3 = 'const3'
        ```

        4. An enumeration in which the values of all members are integers.

        ```python
        from extended_enum import ExtendedEnum

        class IntegerEnum(ExtendedEnum):
            CONST1 = 1
            CONST2 = 2
            CONST3 = 3
        ```

        5. An enumeration in which the values of all members are UUID.

        ```python
        from uuid import UUID
        from extended_enum import ExtendedEnum

        class UUIDEnum(ExtendedEnum):
            CONST1 = UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')
            CONST2 = UUID('e51107a4-7f2b-4de3-9034-fdfb0a50e30f')
            CONST3 = UUID('a84fb294-edc8-46af-b6bc-103377dcee24')
        ```
    """

    value: SimpleValueType
    _value_: ExtendedEnumValueType  # noqa: WPS120

    _ignore_ = ['_simple_value2member']  # noqa: WPS120
    _simple_value2member: ClassVar[Dict[SimpleValueType, 'ExtendedEnumType']] = {}

    def __init__(self, value: Union[SimpleValueType, ExtendedEnumValueType]) -> None:
        """
        Initialize an enumeration object.

        Args:
            value: Simple or extended value.
                   The simple value will be converted to an expanded form to have the same interface.
        """
        self._check_type(value)
        if not isinstance(value, BaseExtendedEnumValue):
            value = BaseExtendedEnumValue(value)

        super().__init__()
        self._value_ = value  # noqa: WPS120

    @classmethod
    def get_values(cls) -> Tuple[SimpleValueType, ...]:
        """Get a list of values of an enumeration."""
        return tuple(item.value for item in cls.get_members().values())

    @classmethod
    def get_extended_values(cls) -> Tuple[ExtendedEnumValueType, ...]:
        """Get a list of values (in expanded form) of an enumeration."""
        return tuple(item.extended_value for item in cls.get_members().values())

    @classmethod
    def get_members(cls) -> Dict[str, ExtendedEnumType]:
        """Get the members of the enumeration."""
        return cast(dict, cls.__members__)

    @classmethod
    def get_simple_value_member(cls) -> Dict[SimpleValueType, ExtendedEnumType]:
        """Get a mapping of enumeration members to simple values."""
        if not hasattr(cls, '_simple_value2member'):  # noqa: WPS421
            simple_value2member = {member.value: member for member in cls.get_members().values()}
            cls._simple_value2member = simple_value2member
        return cls._simple_value2member

    @DynamicClassAttribute
    def value(self) -> SimpleValueType:
        """Get the value of the enumeration member."""
        return self._value_.value

    @DynamicClassAttribute
    def extended_value(self) -> ExtendedEnumValueType:
        """Get the expanded value of an enumeration member."""
        return self._value_

    @classmethod
    def _check_type(cls, value: Any) -> None:
        if isinstance(value, (UUID, int, str)):
            return
        if isinstance(value, BaseExtendedEnumValue):
            return
        raise TypeError(f'{value!r} (type={type(value)}) is not a valid {cls.__qualname__}')  # noqa: WPS221

    @classmethod
    def _missing_(cls, value: Any) -> ExtendedEnumType:  # noqa: WPS120
        cls._check_type(value)
        if isinstance(value, (UUID, int, str)):
            try:
                return cls.get_simple_value_member()[value]
            except KeyError:
                pass  # noqa: WPS420
        raise ValueError(f'{value!r} is not a valid {cls.__qualname__}')
