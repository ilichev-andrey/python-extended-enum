# extended-enum

## Introduction

Package that expands the capabilities of the standard Enum.

## Features

- store additional information inside Enum member

## Install

```shell
pip install extended-enum
```

## Usage

### Quick Start

```python
from dataclasses import dataclass, field
from enum import unique
from typing import Optional
from uuid import UUID
from extended_enum import ExtendedEnum, ValueWithDescription, BaseExtendedEnumValue, EnumField


@dataclass(frozen=True)
class SomeExtendedEnumValue(BaseExtendedEnumValue):
    display_name: str = field(compare=False)
    description: Optional[str] = field(default=None, compare=False)
    

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
    CONST9 = EnumField(SomeExtendedEnumValue(value='const9', display_name='some display name', description='some const9 description'))

unique(MixedEnum)
```

```pycon
>>> MixedEnum.CONST9
<MixedEnum.CONST9: SomeExtendedEnumValue(value='const9', display_name='some display name', description='some const9 description')>
>>> MixedEnum.CONST9.value
'const9'
>>> MixedEnum.CONST9.extended_value
SomeExtendedEnumValue(value='const9', display_name='some display name', description='some const9 description')
>>> MixedEnum.get_values()
Tuple 
('const1',
 1,
 UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'),
 '79ff3431-3e98-4bec-9a4c-63ede2580f83',
 'const4',
 2,
 UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2'),
 'const7',
 3,
 'const9')
>>> MixedEnum.get_extended_values()
Tuple 
(BaseExtendedEnumValue(value='const1'),
 BaseExtendedEnumValue(value=1),
 BaseExtendedEnumValue(value=UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83')),
 BaseExtendedEnumValue(value='79ff3431-3e98-4bec-9a4c-63ede2580f83'),
 BaseExtendedEnumValue(value='const4'),
 BaseExtendedEnumValue(value=2),
 BaseExtendedEnumValue(value=UUID('e7b4b8ae-2224-47ec-afce-40aeb10b85e2')),
 ValueWithDescription(value='const7', description=None),
 ValueWithDescription(value=3, description='some const8 description'),
 SomeExtendedEnumValue(value='const9', display_name='some display name', description='some const9 description'))
```

## License

This project is licensed under the [Apache-2.0](https://github.com/ilichev-andrey/python-extended-enum/blob/master/LICENSE) License.
