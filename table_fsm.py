from abc import ABC, abstractmethod

class State:
    READY = 1
    ROW_SPLITOR = 2
    ROW_LINE = 3
    ROW_LINE_LF = 4

class Delegate(ABC):

    @abstractmethod
    def error(self, ctx):
        return NotImplemented

    @abstractmethod
    def append(self, ctx):
        return NotImplemented

    @abstractmethod
    def cell(self, ctx):
        return NotImplemented

    @abstractmethod
    def line(self, ctx):
        return NotImplemented

    @abstractmethod
    def row(self, ctx):
        return NotImplemented


_transform_states = [[0, 0, 0, 0, 0], [1, 0, 2, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, 1], [-2, 0, -1, 0, 0]]

class StateMachine:

    def __init__(self, delegate):
        self.state = State.READY
        self.delegate = delegate
        self._transform_actions = [[self._noop, self._noop, self._noop, self._noop, self._noop], [self._noop, self.delegate.error, self._noop, self.delegate.error, self._noop], [self._noop, self._noop, self.delegate.error, self.delegate.error, self._noop], [self.delegate.append, self.delegate.append, self.delegate.cell, self.delegate.append, self.delegate.line], [self.delegate.row, self.delegate.error, self._noop, self.delegate.error, self._noop]]

    def _noop(self, ctx):
        pass

    def plus(self, ctx):
        global _transform_states
        self._transform_actions[self.state][0](ctx)
        self.state += _transform_states[self.state][0]

    def minus(self, ctx):
        global _transform_states
        self._transform_actions[self.state][1](ctx)
        self.state += _transform_states[self.state][1]

    def pipe(self, ctx):
        global _transform_states
        self._transform_actions[self.state][2](ctx)
        self.state += _transform_states[self.state][2]

    def others(self, ctx):
        global _transform_states
        self._transform_actions[self.state][3](ctx)
        self.state += _transform_states[self.state][3]

    def lf(self, ctx):
        global _transform_states
        self._transform_actions[self.state][4](ctx)
        self.state += _transform_states[self.state][4]


