"""

"""

# Version and library information
LIBRARY_NAME = "pywib"
LIBRARY_VERSION = "0.1.0"

# Event types for interaction tracking
class EventTypes:
    """ Event type constants for interaction tracking."""
    EVENT_ON_MOUSE_MOVE = 0
    EVENT_ON_CLICK = 1
    EVENT_ON_DOUBLE_CLICK = 2
    EVENT_ON_MOUSE_DOWN = 3
    EVENT_ON_MOUSE_UP = 4
    EVENT_ON_WHEEL = 5
    EVENT_CONTEXT_MENU = 6
    EVENT_ON_TOUCH_MOVE = 7
    EVENT_WINDOW_SCROLL = 11
    EVENT_WINDOW_RESIZE = 12
    EVENT_KEY_DOWN = 13
    EVENT_KEY_PRESS = 14
    EVENT_KEY_UP = 15
    EVENT_FOCUS = 16
    EVENT_BLUR = 17
    EVENT_ON_CHANGE_SELECTION_OBJECT = 18
    EVENT_ON_CLICK_SELECTION_OBJECT = 19
    EVENT_INIT_TRACKING = 100
    EVENT_TRACKING_END = 200

class ComponentTypes:
    """ Component type constants for UI elements."""
    COMPONENT_TEXT_FIELD = 1
    COMPONENT_COMBOBOX = 2
    COMPONENT_OPTION = 3
    COMPONENT_RADIO_BUTTON = 4
    COMPONENT_CHECK_BOX = 5

class ColumnNames:
    """ Standard column names for DataFrame operations."""
    SESSION_ID = 'sessionId'
    SCENE_ID = 'sceneId'
    EVENT_TYPE = 'eventType'
    ELEMENT_ID = 'elementId'
    TIME_STAMP = 'timeStamp'
    X = 'x'
    Y = 'y'
    KEY_VALUE_EVENT = 'keyValueEvent'
    KEY_CODE_EVENT = 'keyCodeEvent'
    SOURCE_SESSION_ID = 'sourceSessionId'
    DT = 'dt'
    DX = 'dx'
    DY = 'dy'