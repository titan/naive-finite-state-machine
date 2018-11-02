class State:
    READY = 0
    ROW_SPLITOR = 1
    ROW_LINE = 2
    ROW_LINE_LF = 3

class Event:
    PLUS = 0
    MINUS = 1
    PIPE = 2
    OTHERS = 3
    LF = 4

class Action:
    ERROR = 1
    APPEND = 2
    CELL = 3
    LINE = 4
    ROW = 5

class FSM:
    def __init__(self, action_handler = None):
        self.transform_states = [[State.ROW_SPLITOR, State.READY, State.ROW_LINE, State.READY, State.READY], [State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.READY], [State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE_LF], [State.ROW_SPLITOR, State.ROW_LINE_LF, State.ROW_LINE, State.ROW_LINE_LF, State.ROW_LINE_LF]]
        self.transform_actions = [[0, Action.ERROR, 0, Action.ERROR, 0], [0, 0, Action.ERROR, Action.ERROR, 0], [Action.APPEND, Action.APPEND, Action.CELL, Action.APPEND, Action.LINE], [Action.ROW, Action.ERROR, 0, Action.ERROR, 0]]
        self.handler = action_handler
        self.state = State.READY
    def process(self, event, data = None):
        if self.handler:
            self.handler(self.transform_actions[self.state][event], data)
        self.state = self.transform_states[self.state][event]

