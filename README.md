# extended-enum

## Introduction

Package that expands the capabilities of the standard `Enum`.

There are times when you want to have constants that also carry additional information.
This functionality can be implemented in different ways, one of them is mapping, but there is a better approach - using `ExtendedEnum`.
`ExtendedEnum` - allows you to store dataclass as a value.
This allows you to store the value and additional information in one object and no longer need to use any auxiliary data containers.

It is important to note that the functionality of the standard `Enum` is preserved. `ExtendedEnum` is just an add-on.

## Install

Installation does not require any additional dependencies.
`ExtendedEnum` was specifically designed to be a lightweight package that uses only standard Python functionality.

```shell
pip install extended-enum
```

## Features

- You can store a value and additional information inside an `Enum` member.
  Initially, the `ValueWithDescription` class is available, which additionally stores a description.
  You can create a custom class `SomeExtendedEnumValue`.

```python
from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription, EnumField

class DetailedEnum(ExtendedEnum):
    CONST1 = EnumField(BaseExtendedEnumValue(value='const1'))
    CONST2 = EnumField(ValueWithDescription(value='const2', description='some description 2'))
    CONST3 = EnumField(ValueWithDescription(value='const3', description='some description 3'))
```

```python
from dataclasses import dataclass, field
from extended_enum import ExtendedEnum, BaseExtendedEnumValue, EnumField
from typing import Optional

@dataclass(frozen=True)
class SomeExtendedEnumValue(BaseExtendedEnumValue):
    display_name: str = field(compare=False)
    description: Optional[str] = field(default=None, compare=False)

class DetailedEnum(ExtendedEnum):
    CONST1 = EnumField(SomeExtendedEnumValue(value='const1', display_name='ONE'))
    CONST2 = EnumField(SomeExtendedEnumValue(value='const2', display_name='TWO', description='some description 2'))
```

- The following types can be used as internal values: str, int, uuid.UUID [[ref: SimpleValueType](extended_enum/__init__.py#L7)]

```python
from uuid import UUID
from extended_enum import ExtendedEnum, EnumField

class MixedEnum(ExtendedEnum):
    CONST1 = EnumField('const1')
    CONST2 = EnumField(2)
    CONST3 = EnumField(UUID('79ff3431-3e98-4bec-9a4c-63ede2580f83'))
```

- Additionally created attributes:
  * `extended_value` - Get the expanded value of an enumeration member.
  * `get_values` - Get a list of values of an enumeration.
  * `get_extended_values` - Get a list of values (in expanded form) of an enumeration.
  * `get_members` - Get the members of the enumeration.
  * `get_simple_value_member` - Get a mapping of enumeration members to simple values.

```pycon
>>> from extended_enum import ExtendedEnum, BaseExtendedEnumValue, ValueWithDescription, EnumField
>>> class DetailedEnum(ExtendedEnum):
...     CONST1 = EnumField(ValueWithDescription(value='const1'))
...     CONST2 = EnumField(ValueWithDescription(value='const2', description='some description 2'))
...     CONST3 = EnumField(ValueWithDescription(value='const3', description='some description 3'))
>>> DetailedEnum.CONST2.value
'const2'
>>> DetailedEnum.CONST2.extended_value
ValueWithDescription(value='const2', description='some description 2')
>>> DetailedEnum.get_values()
('const1', 'const2', 'const3')
>>> DetailedEnum.get_extended_values()
(ValueWithDescription(value='const1', description=None), 
 ValueWithDescription(value='const2', description='some description 2'), 
 ValueWithDescription(value='const3', description='some description 3'))
>>> DetailedEnum.get_members()
mappingproxy({
    'CONST1': <DetailedEnum.CONST1: ValueWithDescription(value='const1', description=None)>, 
    'CONST2': <DetailedEnum.CONST2: ValueWithDescription(value='const2', description='some description 2')>, 
    'CONST3': <DetailedEnum.CONST3: ValueWithDescription(value='const3', description='some description 3')>
})
>>> DetailedEnum.get_simple_value_member()
{
    'const1': <DetailedEnum.CONST1: ValueWithDescription(value='const1', description=None)>, 
    'const2': <DetailedEnum.CONST2: ValueWithDescription(value='const2', description='some description 2')>, 
    'const3': <DetailedEnum.CONST3: ValueWithDescription(value='const3', description='some description 3')>
}
```

- You can make unique enumerations using `enum.unique` in the same way as with a standard `Enum`.

```pycon
>>> from enum import unique
>>> from extended_enum import ExtendedEnum, EnumField
>>> @unique
... class Mistake(ExtendedEnum):
...     ONE = EnumField(1)
...     TWO = EnumField(2)
...     THREE = EnumField(2)
...     FOUR = EnumField('four')
...     FIVE = EnumField('five')
...     SIX = EnumField('four')
...     SEVEN = EnumField(UUID('1a882a33-f0e2-4b9f-a880-30db10c2c7dc'))
...     EIGHT = EnumField(UUID('1a882a33-f0e2-4b9f-a880-30db10c2c7dc'))
...     NINE = EnumField(UUID('f0602460-77fb-4980-9900-4e3f50093b78'))
... 
ValueError: duplicate values found in <enum 'Mistake'>: THREE -> TWO, SIX -> FOUR, EIGHT -> SEVEN
>>> 
>>> # Or without decorator
>>> unique(Mistake)
ValueError: duplicate values found in <enum 'Mistake'>: THREE -> TWO, SIX -> FOUR, EIGHT -> SEVEN
```

- You can make a nice display in automatic documentation, for example in `/redoc`. Below is an example for FastAPI

<img width="1433" alt="extended-enum_in_fastapi" src="https://github.com/ilichev-andrey/python-extended-enum/assets/24242890/f58640a8-7122-4f3c-8e93-f9ef96a65186">

```python
from typing import Any, Literal, get_args, get_origin

import uvicorn
from extended_enum import ExtendedEnum, EnumField, ValueWithDescription, BaseExtendedEnumValue
from fastapi import FastAPI
from pydantic import Field, BaseModel

app = FastAPI()


class CompressedFileExtension(ExtendedEnum):
    LZ = EnumField(ValueWithDescription(
        value='.lz',
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    ))
    IZO = EnumField(ValueWithDescription(
        value='.izo',
        description='Lossless data compression algorithm that is focused on decompression speed'
    ))
    IZMA = EnumField(ValueWithDescription(
        value='.izma',
        description='Uses a dictionary compression scheme and features a high compression ratio while still maintaining decompression speed'
    ))
    ZIP = EnumField('.zip')


def format_enum_description(enum_cls: Any, delimiter: str = '\n') -> str:
    if get_origin(enum_cls) is not Literal and issubclass(enum_cls, ExtendedEnum):
        extended_values = enum_cls.get_extended_values()
    else:
        extended_values = (
            member.extended_value
            for member in get_args(enum_cls)
            if isinstance(member, ExtendedEnum)
        )

    items = (format_enum_value(enum_value=value) for value in extended_values)
    return delimiter.join(items)


def format_enum_value(enum_value: BaseExtendedEnumValue) -> str:
    description = ''
    if isinstance(enum_value, ValueWithDescription):
        description = ' - {description}'.format(description=enum_value.description)
    return '* `{value}`{description}'.format(value=enum_value.value, description=description)


FileExtension2Type = Literal[CompressedFileExtension.IZMA, CompressedFileExtension.ZIP]


class SomeRequestBody(BaseModel):
    file_path: str
    file_extension1: CompressedFileExtension = Field(
        default=CompressedFileExtension.ZIP,
        description='The following file extensions are supported.\n'
                    '{0}'.format(format_enum_description(CompressedFileExtension))
    )
    file_extension2: FileExtension2Type = Field(
        description='The following file extensions are supported.\n'
                    '{0}'.format(format_enum_description(FileExtension2Type))
    )


@app.get('/')
async def example(body: SomeRequestBody):
    return {}


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8000, workers=1)
```

## Usage

### Quick Start

`ExtendedEnum` is very easy to use.
Switching from standard `Enum` is not difficult.

Let's look at an example.
You have an enum that denotes file extensions declared like this:

```python
from enum import Enum

class FilenameExtension(Enum):
    LZ = '.lz'
    IZO = '.izo'
    IZMA = '.izma'
    ZIP = '.zip'
```

Let's clarify these incomprehensible character sets.
We will additionally need an `EnumField` wrapper for each value and a data 
class - `ValueWithDescription` to store additional information.
Let's add a description for 3 members, a `.zip` will be left without a description because everyone knows it.

```python
from extended_enum import ExtendedEnum, EnumField, ValueWithDescription

class CompressedFileExtension(ExtendedEnum):
    LZ = EnumField(ValueWithDescription(
        value='.lz',
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    ))
    IZO = EnumField(ValueWithDescription(
        value='.izo',
        description='Lossless data compression algorithm that is focused '
                    'on decompression speed'
    ))
    IZMA = EnumField(ValueWithDescription(
        value='.izma',
        description='Uses a dictionary compression scheme and features '
                    'a high compression ratio while still maintaining '
                    'decompression speed'
    ))
    ZIP = EnumField('.zip')
```

That's it, we have completed the transition.
Let's see what is stored inside the class.

```pycon
>>> from pprint import pprint
>>> pprint(list(CompressedFileExtension))
[
    <CompressedFileExtension.LZ: ValueWithDescription(
        value='.lz',
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    )>,
    <CompressedFileExtension.IZO: ValueWithDescription(
        value='.izo', 
        description='Lossless data compression algorithm that is focused on decompression speed'
    )>,
    <CompressedFileExtension.IZMA: ValueWithDescription(
        value='.izma', 
        description='Uses a dictionary compression scheme and features a high compression ratio while still maintaining decompression speed'
    )>,
    <CompressedFileExtension.ZIP: BaseExtendedEnumValue(value='.zip')>
]
```

Serializing values is also not difficult.

```pycon
>>> import json
>>> from enum import Enum
>>> from typing import Any
>>> def dump_enum(value: Any) -> str:
...    if isinstance(value, Enum):
...        return value.value
...    raise TypeError()
>>> json.dumps(
...     {
...         "file_extension1": CompressedFileExtension.IZO, 
...         "file_extension2": CompressedFileExtension.ZIP
...     },
...     default=dump_enum
... )
'{"file_extension1": ".izo", "file_extension2": ".zip"}'
>>> CompressedFileExtension('.lz')
<CompressedFileExtension.LZ: ValueWithDescription(
    value='.lz', 
    description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
)>
>>> CompressedFileExtension('.unknown')
ValueError: '.unknown' is not a valid CompressedFileExtension
```

Easily works with `orjson`.

```pycon
>>> import orjson
>>> orjson.dumps(
...     {
...         "file_extension1": CompressedFileExtension.IZO, 
...         "file_extension2": CompressedFileExtension.ZIP
...     }
... )
b'{"file_extension1":".izo","file_extension2":".zip"}'
```

Also works great with `Pydantic v1`.

```pycon
>>> from extended_enum import ExtendedEnum, EnumField, ValueWithDescription
>>> from pydantic import BaseModel
>>> class SomeModel(BaseModel):
...     file_path: str
...     file_extension: CompressedFileExtension
>>> obj = SomeModel(
...    file_path='/path/to/compressed_file.lz',
...    file_extension=CompressedFileExtension.LZ
...)
>>> obj.json()
'{"file_path": "/path/to/compressed_file.lz", "file_extension": ".lz"}'
>>> 
>>> SomeModel.parse_raw('{"file_path": "/path/to/compressed_file.lz", "file_extension": ".lz"}')
SomeModel(
    file_path='/path/to/compressed_file.lz', 
    file_extension=<CompressedFileExtension.LZ: ValueWithDescription(
        value='.lz', 
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    )>
)
>>> 
>>> import orjson
>>> data = orjson.loads('{"file_path": "/path/to/compressed_file.lz", "file_extension": ".lz"}')
>>> SomeModel(**data)
SomeModel(
    file_path='/path/to/compressed_file.lz', 
    file_extension=<CompressedFileExtension.LZ: ValueWithDescription(
        value='.lz', 
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    )>
)
```

Also works great with `Pydantic v2` with minor differences from the previous example.

```pycon
>>> obj.model_dump_json()
'{"file_path":"/path/to/compressed_file.lz","file_extension":".lz"}'
>>> 
>>> SomeModel.model_validate_json('{"file_path": "/path/to/compressed_file.lz", "file_extension": ".lz"}')
SomeModel(
    file_path='/path/to/compressed_file.lz', 
    file_extension=<CompressedFileExtension.LZ: ValueWithDescription(
        value='.lz', 
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    )>
)
>>> 
>>> import orjson
>>> data = orjson.loads('{"file_path": "/path/to/compressed_file.lz", "file_extension": ".lz"}')
>>> SomeModel(**data)
SomeModel(
    file_path='/path/to/compressed_file.lz', 
    file_extension=<CompressedFileExtension.LZ: ValueWithDescription(
        value='.lz', 
        description='Employs the Lempel–Ziv–Markov chain algorithm (LZMA)'
    )>
)
```


## License

This project is licensed under the [Apache-2.0](https://github.com/ilichev-andrey/python-extended-enum/blob/master/LICENSE) License.
