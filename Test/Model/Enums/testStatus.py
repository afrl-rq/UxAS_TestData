from enum import Enum, auto

# the execution status of a test
class TestStatus(Enum):
    Pending = auto() #using auto ensures unique int representation
    Executing = auto()
    Passed = auto()
    Failed = auto()