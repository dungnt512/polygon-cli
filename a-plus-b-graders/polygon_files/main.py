import solution

# solution -- is a python package with a participant's solution

import sys

_input = input

if sys.version_info[0] < 3:
    _input = raw_input

a, b = map(int, _input().split())
print(solution.sum_ab(a, b))
