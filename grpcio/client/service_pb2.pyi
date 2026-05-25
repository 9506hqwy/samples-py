import datetime

from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnumerationValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VALUE0: _ClassVar[EnumerationValue]
    VALUE1: _ClassVar[EnumerationValue]
    VALUE2: _ClassVar[EnumerationValue]
VALUE0: EnumerationValue
VALUE1: EnumerationValue
VALUE2: EnumerationValue

class ScalarValueTypes(_message.Message):
    __slots__ = ("double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64", "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes", "array", "map", "enumvalue", "oneint32", "onestring", "any", "timestamp")
    class MapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_NUMBER: _ClassVar[int]
    INT64_FIELD_NUMBER: _ClassVar[int]
    UINT32_FIELD_NUMBER: _ClassVar[int]
    UINT64_FIELD_NUMBER: _ClassVar[int]
    SINT32_FIELD_NUMBER: _ClassVar[int]
    SINT64_FIELD_NUMBER: _ClassVar[int]
    FIXED32_FIELD_NUMBER: _ClassVar[int]
    FIXED64_FIELD_NUMBER: _ClassVar[int]
    SFIXED32_FIELD_NUMBER: _ClassVar[int]
    SFIXED64_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ENUMVALUE_FIELD_NUMBER: _ClassVar[int]
    ONEINT32_FIELD_NUMBER: _ClassVar[int]
    ONESTRING_FIELD_NUMBER: _ClassVar[int]
    ANY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    double: float
    float: float
    int32: int
    int64: int
    uint32: int
    uint64: int
    sint32: int
    sint64: int
    fixed32: int
    fixed64: int
    sfixed32: int
    sfixed64: int
    bool: bool
    string: str
    bytes: bytes
    array: _containers.RepeatedScalarFieldContainer[str]
    map: _containers.ScalarMap[str, int]
    enumvalue: EnumerationValue
    oneint32: int
    onestring: str
    any: _any_pb2.Any
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, double: _Optional[float] = ..., float: _Optional[float] = ..., int32: _Optional[int] = ..., int64: _Optional[int] = ..., uint32: _Optional[int] = ..., uint64: _Optional[int] = ..., sint32: _Optional[int] = ..., sint64: _Optional[int] = ..., fixed32: _Optional[int] = ..., fixed64: _Optional[int] = ..., sfixed32: _Optional[int] = ..., sfixed64: _Optional[int] = ..., bool: bool = ..., string: _Optional[str] = ..., bytes: _Optional[bytes] = ..., array: _Optional[_Iterable[str]] = ..., map: _Optional[_Mapping[str, int]] = ..., enumvalue: _Optional[_Union[EnumerationValue, str]] = ..., oneint32: _Optional[int] = ..., onestring: _Optional[str] = ..., any: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
