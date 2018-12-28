from abc import ABC, abstractmethod

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

class Delegate(ABC):
    @abstractmethod
    def error(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def append(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def cell(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def line(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def row(self, ctx, state = 0, event = 0):
        return NotImplemented

transform_states = [[State.ROW_SPLITOR, State.READY, State.ROW_LINE, State.READY, State.READY], [State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.ROW_SPLITOR, State.READY], [State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE, State.ROW_LINE_LF], [State.ROW_SPLITOR, State.ROW_LINE_LF, State.ROW_LINE, State.ROW_LINE_LF, State.ROW_LINE_LF]]

class StateMachine:
    def __init__(self, delegate):
        self.state = State.READY
        self.delegate = delegate
        self.transform_actions = [[None, self.delegate.error, None, self.delegate.error, None], [None, None, self.delegate.error, self.delegate.error, None], [self.delegate.append, self.delegate.append, self.delegate.cell, self.delegate.append, self.delegate.line], [self.delegate.row, self.delegate.error, None, self.delegate.error, None]]
    def process(self, ctx, event):
        global transform_states
        if self.transform_actions[self.state][event]:
            self.transform_actions[self.state][event](ctx, self.state, event)
        self.state = transform_states[self.state][event]

