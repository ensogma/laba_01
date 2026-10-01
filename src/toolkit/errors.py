class ToolkitError(Exception):
    'basic error'


#       --calculator--
class EmptyExpressionError(ToolkitError):
    """empty expression"""


class InvalidCharacterError(ToolkitError):
    """invalid character"""


class MissingOperandError(ToolkitError):
    """missing operand"""


class TwoBinaryOperatorsError(ToolkitError):
    """two binary operators"""


class DivisionByZeroError(ToolkitError):
    """division by zero"""


#      --converter
class UnknownUnitError(ToolkitError):
    """unknown unit"""


class IncompatibleUnitsError(ToolkitError):
    """incompatible units"""


class InvalidValueError(ToolkitError):
    """invalid value"""

