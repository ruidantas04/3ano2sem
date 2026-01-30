from hypothesis import given
from hypothesis.strategies import lists, integers

@given(lists(integers()), lists(integers()), lists(integers()))
def test_list_append_associative(x, y, z):
    assert (x + y) + z == x + (y + z)  

@given(lists(integers()))
def test_list_reverse(x:list[int]):
    assert list(reversed(list(reversed(x)))) == x  

@given(lists(integers()), lists(integers()))
def test_list_append_reverse(x:list[int], y:list[int]):
    assert list(reversed(x + y)) == list(reversed(y)) + list(reversed(x))  

@given(integers(),lists(integers()))
def test_list_remove(x:int,l:list[int]):
    l2=[x]+l
    l2.remove(x)
    assert l2==l