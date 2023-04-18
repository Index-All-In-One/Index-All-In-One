from enum import Enum

class PluginReturnStatus(Enum):
    SUCCESS = 0
    OTHER_ERROR = 1
    WRONG_CREDS = 2
    EXCEPTION = 3
    NO_PLUGIN = 4
    TWO_STEP_1 = 5
