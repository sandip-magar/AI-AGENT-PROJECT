import pytest
from ai.tools import calculate_math

def test_calculator_tool_valid():
    """Test if the calculator correclty evaluates a simple math expression."""

    response = calculate_math.invoke({"expression": "25 * 5"})
    assert response['status'] == "success"
    assert response['result'] == "125"

def test_calculator_tool_addition():
    """Test basic addition."""

    response = calculate_math.invoke({"expression": " 500 + 1200"})
    assert response['status'] == "success"
    assert response['result'] == "1700"