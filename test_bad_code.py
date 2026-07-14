import pytest
from bad_code import calculate_division
def test_calculate_division_normal():
    assert calculate_division(10, 2) == 5.0
def test_calculate_division_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_division(10, 0)
