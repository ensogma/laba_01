import unittest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)


class TestConverter(unittest.TestCase):
    def test_km_to_m(self):
        self.assertAlmostEqual(convert("1", "km", "m"), 1000.0)

    def test_cm_to_m(self):
        self.assertAlmostEqual(convert("100", "cm", "m"), 1.0)

    def test_mm_to_cm(self):
        self.assertAlmostEqual(convert("50", "mm", "cm"), 5.0)

    def test_kg_to_g(self):
        self.assertAlmostEqual(convert("2.5", "kg", "g"), 2500.0)

    def test_g_to_kg(self):
        self.assertAlmostEqual(convert("500", "g", "kg"), 0.5)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(convert("0", "c", "k"), 273.15)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(convert("212", "f", "c"), 100.0)

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert("100", "c", "f"), 212.0)

    def test_absolute_zero_is_allowed(self):
        self.assertAlmostEqual(convert("0", "k", "c"), -273.15)

    def test_units_case_insensitive(self):
        self.assertAlmostEqual(convert("1", "KM", "M"), 1000.0)

    def test_same_unit(self):
        self.assertAlmostEqual(convert("5", "m", "m"), 5.0)

    def test_result_is_float(self):
        self.assertIsInstance(convert("1", "km", "m"), float)

    def test_number_instead_of_string(self):
        self.assertAlmostEqual(convert(3, "m", "cm"), 300.0)

    def test_unknown_from_unit(self):
        with self.assertRaises(UnknownUnitError):
            convert("5", "mile", "m")

    def test_unknown_to_unit(self):
        with self.assertRaises(UnknownUnitError):
            convert("5", "m", "mile")

    def test_incompatible_units(self):
        with self.assertRaises(IncompatibleUnitsError):
            convert("5", "km", "kg")

    def test_incompatible_temperature_and_length(self):
        with self.assertRaises(IncompatibleUnitsError):
            convert("5", "c", "m")

    def test_below_absolute_zero_celsius(self):
        with self.assertRaises(BelowAbsoluteZeroError):
            convert("-300", "c", "k")

    def test_below_absolute_zero_kelvin(self):
        with self.assertRaises(BelowAbsoluteZeroError):
            convert("-1", "k", "c")

    def test_invalid_value(self):
        with self.assertRaises(InvalidValueError):
            convert("abc", "m", "km")

    def test_nan_value(self):
        with self.assertRaises(InvalidValueError):
            convert("nan", "m", "km")


if __name__ == "__main__":
    unittest.main()
