# -*-mode:python; coding:utf-8-*-

import math

# 只支持正整数

IDX_BASE = 0
IDX_ITOA = 1
IDX_ATOI = 2

__debug = False

def new_index(basemap):
    index=(len(basemap), basemap, {})
    for idx, char in enumerate(basemap):
        index[IDX_ATOI][char] = idx
    return index

def check_index(index):
    basen1=index[IDX_BASE]
    basen2=len(index[IDX_ITOA])
    basen3=len(index[IDX_ATOI].keys())
    return basen1 == basen2 and basen1 == basen3

def ntos(number, index):
    # Fix: Add input validation for negative numbers
    if not isinstance(number, int) or number < 0:
        raise ValueError("Only non-negative integers are supported")
    
    basen = index[IDX_BASE]
    if number == 0:
        return index[IDX_ITOA][0]
    chars = []  # Fix: Use list for better performance instead of string concatenation
    while number > 0:
        remainder = number % basen
        char = index[IDX_ITOA][remainder]
        chars.append(char)
        number = number // basen  # Fix: Use integer division for Python 3 compatibility
        if __debug:
            print("%d %s %d %s" % (remainder, char, number, ''.join(reversed(chars))))
    return ''.join(reversed(chars))

def ston(string, index):
    # Fix: Add input validation for string type and invalid characters
    if not isinstance(string, str):
        raise ValueError("Input must be a string")
    
    basen=index[IDX_BASE]
    number=0
    reversed_string=string[::-1]
    for idx, char in enumerate(reversed_string):
        # Fix: Provide better error message for invalid characters
        if char not in index[IDX_ATOI]:
            raise ValueError("Invalid character '{}' found in string. Valid characters are: {}".format(
                char, ''.join(index[IDX_ITOA])))
        value = index[IDX_ATOI][char]
        number = number + value * int(math.pow(basen, idx))
        if __debug:
            print("%d %s %d" % (value, char, number))
    return number



    
class BaseAny:
    def __init__(self, basemap):
        self.__index = new_index(basemap)
        assert(check_index(self.__index))
    def ntos(self, number):
        return ntos(number, self.__index)
    def ston(self, string):
        return ston(string, self.__index)

# export factory method
def new(basemap):
    return BaseAny(basemap)

# predefine base<N>
base32map="abcdefghijkmnpqrstuvwxyz23456789"
base32 = new(base32map)




# test methods
def test_one(baseany, number):
    string = baseany.ntos(number)
    n2 = baseany.ston(string)
    print("%d => %s" % (n2, string))
    assert(number == n2)

number_to_test = (0, 1, 9, 10, 42, 43, 51, 99,
                  255, 999, 1232, 3123, 323123, 43902349,
                  123312312, 312313312,34788785645)

def test(baseany, number_array = number_to_test):
    for n in number_array:  # Fix: Proper indentation
        test_one(baseany, n)

if __name__ == '__main__':
    base9 = new('dfasljthz')
    test(base9)
    test(base32)
    print("All test passed.")



