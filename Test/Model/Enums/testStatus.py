from enum import Enum

# the execution status of a test
class TestStatus(Enum):
    Pending = 0
    Executing = 1
    Passed = 2
    Failed = 3