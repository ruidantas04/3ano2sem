from hypothesis import given
from hypothesis.strategies import lists, integers
import pytest

def myIndex(input_list, value):
    if len(input_list) == 0:
        raise ValueError("Value not found in list")
    if input_list[0] == value:
        return 0
    return 1 + myIndex(input_list[1:], value)

@given(lists(integers(), min_size=0, max_size=0), integers())
def test_empty_listRaisesError(x: list[int], y: int):
    with pytest.raises(ValueError):  # Expect a ValueError to be raised
        myIndex(x, y)
        
@given(lists(integers(), min_size=1), integers())
def test_myindex(x: list[int], y: int):
    if y in x:
        assert myIndex(x, y) == x.index(y)  # Should return the correct index
    else:
        with pytest.raises(ValueError):     # Should raise an error if y not in x
            myIndex(x, y)
            
@given(lists(integers(), min_size=0, max_size=0), integers())
def test_empty_list(x: list[int], y: int):
    with pytest.raises(ValueError):         # Deve levantar erro para lista vazia
        myIndex(x, y)