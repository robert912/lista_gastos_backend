import pytest
from app_tests import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(1, 2) == 3

def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2

def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6

def test_divide(calculator):
    assert calculator.divide(6, 3) == 2

def test_divide_by_zero(calculator):
    with pytest.raises(ValueError):
        calculator.divide(1, 0)
