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

class StateMachine:
    def error(self, ctx, state = 0, event = 0):
        pass
    def append(self, ctx, state = 0, event = 0):
        pass
    def cell(self, ctx, state = 0, event = 0):
        pass
    def line(self, ctx, state = 0, event = 0):
        pass
    def row(self, ctx, state = 0, event = 0):
        pass
    def __init__(self, delegate):
        self.error = delegate.error
        self.append = delegate.append
        self.cell = delegate.cell
        self.line = delegate.line
        self.row = delegate.row
        self.transform_states = [[State.ROW_SPLITOR, State.READY, State.ROW_LINE, State.READY, State.READY], [State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.READY], [State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE_LF], [State.ROW_SPLITOR, State.ROW_LINE_LF, State.ROW_LINE, State.ROW_LINE_LF, State.ROW_LINE_LF]]
        self.transform_actions = [[None, self.error, None, self.error, None], [None, None, self.error, self.error, None], [self.append, self.append, self.cell, self.append, self.line], [self.row, self.error, None, self.error, None]]
        self.state = State.READY
    def process(self, ctx, event):
        if self.transform_actions[self.state][event]:
            self.transform_actions[self.state][event](ctx, self.state, event)
        self.state = self.transform_states[self.state][event]

