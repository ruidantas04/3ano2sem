from hypothesis import given
from hypothesis.strategies import lists, integers
import math

def mulLR(list_nums):
    if len(list_nums) == 0:
        return 1
    elif len(list_nums)==1:
        return list_nums[0]
    else:
        return list_nums[0] * mulLR(list_nums[1:])

def mulLI(list_nums):
    res = 1
    if (len(list_nums)==1):
        return list_nums[0]
    for n in list_nums:
        res *= n
    return res

@given(lists(integers()))
def test_reverse_mull(x:list[int]):
    assert mulLI((x[::-1]))==mulLI(x)
    assert mulLR((x[::-1]))==mulLR(x)
    
@given(integers())
def test_single_mull(x:int):
    assert mulLI([x])==x
    assert mulLR([x])==x

@given(lists(integers()))
def test_prod_mull(x:list[int]):
    assert mulLI(x)==math.prod(x)
    assert mulLR(x)==math.prod(x)