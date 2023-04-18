from enum import Enum

class PluginReturnStatus(Enum):
    SUCCESS = 0
    OTHER_ERROR = 1
    WRONG_CREDS = 2
    EXCEPTION = 3
    NO_PLUGIN = 4
    NEED_TWO_STEP_CODE = 5
