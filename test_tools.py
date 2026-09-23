import pytest 
from ai.tools import calculate_math, search_web, query_pdf_rag, WebSearchInput

# TEST 1: MATH TOOL SUCCESS

def test_calculate_math_success():
    "Test that the math tool exactly evaluates a valid mathematical expression."
    result = calculate_math.func("2 + 2 * 3")

    assert result["status"] == "success"
    assert result["result"] == 8
    assert result["expression"] == "2 + 2 * 3"

def test_calculate_math_invalid_expression():
    "Test that the math tool returns an error for an invalid mathematical expression."
    result = calculate_math.func("2 + * 3")

    assert result["status"] == "error"
    assert "Failed to evaluate" in result["message"]

# TEST 2: WEB SEARCH TOOL SUCCESS
def test_search_web_success():
    "Test that the web search tool returns results for a valid query."
    valid_input = WebSearchInput(query="python", max_results=3)
    assert valid_input.query == "python"
    assert valid_input.max_results == 3

    #This should FAIL because max_result is greater than 5 (le=5)
    with pytest.raises(Exception):
        WebSearchInput(query="python", max_results=10)

    #This should FAIL because max_result is less than 1 (ge=1)
    with pytest.raises(Exception):
        WebSearchInput(query="python", max_results=0)