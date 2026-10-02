import math

from .errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)

LENGTH_TO_M = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
MASS_TO_G = {"g": 1.0, "kg": 1000.0}
TEMPERATURES = {"c", "f", "k"}
ABSOLUTE_ZERO = -273.15
EPS = 1e-9


def execute_length(val, from_, to_):
    return val * LENGTH_TO_M[from_] / LENGTH_TO_M[to_]


def execute_mass(val, from_, to_):
    return val * MASS_TO_G[from_] / MASS_TO_G[to_]


def execute_temper(val, from_, to_):
    if from_ == "c":
        in_c = val
    elif from_ == "f":
        in_c = (val - 32) * 5 / 9
    else:
        in_c = val - 273.15
    if in_c < ABSOLUTE_ZERO - EPS:
        raise BelowAbsoluteZeroError("temperature below absolute zero")
    if to_ == "c":
        return in_c
    elif to_ == "f":
        return in_c * 9 / 5 + 32
    return in_c + 273.15


def get_group(unit):
    if unit in LENGTH_TO_M:
        return "length"
    elif unit in MASS_TO_G:
        return "mass"
    elif unit in TEMPERATURES:
        return "temperature"
    raise UnknownUnitError(f"unknown unit '{unit}'")


def evaluate_from(val, from_, to_):
    group_from = get_group(from_)
    group_to = get_group(to_)
    if group_from != group_to:
        raise IncompatibleUnitsError(f"can't convert {from_} to {to_}")
    if group_from == "length":
        return execute_length(val, from_, to_)
    elif group_from == "mass":
        return execute_mass(val, from_, to_)
    return execute_temper(val, from_, to_)


def convert(val, from_, to_):
    try:
        val = float(val)
    except (ValueError, TypeError):
        raise InvalidValueError(f"invalid value '{val}'")
    if not math.isfinite(val):
        raise InvalidValueError(f"invalid value '{val}'")
    return float(evaluate_from(val, from_.lower(), to_.lower()))
