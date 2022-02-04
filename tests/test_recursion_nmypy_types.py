from typing import TypeAlias
valueT: TypeAlias =  int | list["valueT"]
value: valueT = 123

if isinstance(value, int):
    int_check: int = value
else:
    val_check: valueT = value[0]