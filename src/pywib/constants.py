"""

"""

# Version and library information
LIBRARY_NAME = "pywib"
LIBRARY_VERSION = "0.1.0"

# Event types for interaction tracking
class EventTypes:
    """ Event type constants for interaction tracking."""
    EVENT_ON_MOUSE_MOVE = 0
    """Event type for mouse move events."""
    EVENT_ON_CLICK = 1
    """Event type for mouse click events."""
    EVENT_ON_DOUBLE_CLICK = 2
    """Event type for mouse double click events."""
    EVENT_ON_MOUSE_DOWN = 3
    """Event type for mouse down events."""
    EVENT_ON_MOUSE_UP = 4
    """Event type for mouse up events."""
    EVENT_ON_WHEEL = 5
    """Event type for mouse wheel events, specificaly for wheel clicks."""
    EVENT_CONTEXT_MENU = 6
    """Event type for context menu events."""
    EVENT_ON_TOUCH_MOVE = 7
    """Event type for touch move events, specific for mobile and tablet devices."""
    EVENT_WINDOW_SCROLL = 11
    """Event type for window scroll events."""
    EVENT_WINDOW_RESIZE = 12
    """Event type for window resize events."""
    EVENT_KEY_DOWN = 13
    """Event type for key down events."""
    EVENT_KEY_PRESS = 14
    """Event type for key press events."""
    EVENT_KEY_UP = 15
    """Event type for key up events."""
    EVENT_FOCUS = 16
    """Event type for focus events."""
    EVENT_BLUR = 17
    """Event type for blur events."""
    EVENT_ON_CHANGE_SELECTION_OBJECT = 18
    """Event type for change selection events."""
    EVENT_ON_CLICK_SELECTION_OBJECT = 19
    """Event type for click selection events."""
    EVENT_INIT_TRACKING = 100
    """Custom event type for initializing tracking."""
    EVENT_TRACKING_END = 200
    """Custom event type for ending tracking."""

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
    VELOCITY= 'velocity'
    ACCELERATION = 'acceleration'
    JERKINESS = 'jerkiness'
    AUC_RATIO = 'auc_ratio'