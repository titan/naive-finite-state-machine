from abc import ABC, abstractmethod

class State:
    READY = 0
    READY_COMMENT = 1
    MINUS = 2
    MINUS_MINUS = 3
    MINUS_MINUS_MINUS = 4
    MINUS_MINUS_MINUS_MINUS = 5
    ACTION = 6
    ACTION_LF = 7
    ACTION_LF_MINUS = 8
    ACTION_LF_MINUS_MINUS = 9
    ACTION_LF_MINUS_MINUS_MINUS = 10
    ACTION_LF_MINUS_MINUS_MINUS_MINUS = 11
    ACTION_COMMENT = 12
    STATE = 13
    STATE_COMMENT = 14

class Event:
    LF = 0
    MINUS = 1
    BACKSLASH = 2
    OPEN_PARENTHESIS = 3
    CLOSE_PARENTHESIS = 4
    OTHERS = 5
    EOI = 6

class Delegate(ABC):
    @abstractmethod
    def append_tmp(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def comment_error(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def append(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def combine_tmp_comma_append(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def combine_tmp_comma_action(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def action(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def state_error(self, ctx, state = 0, event = 0):
        return NotImplemented
    @abstractmethod
    def state(self, ctx, state = 0, event = 0):
        return NotImplemented

transform_states = [[State.READY, State.MINUS, State.STATE, State.READY_COMMENT, State.READY, State.ACTION, State.READY], [State.READY_COMMENT, State.READY_COMMENT, State.READY_COMMENT, State.READY, State.READY, State.READY_COMMENT, State.READY_COMMENT], [State.ACTION, State.MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS, State.ACTION, State.READY], [State.ACTION, State.MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS, State.ACTION, State.READY], [State.ACTION, State.MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.STATE, State.MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION_LF, State.ACTION, State.STATE, State.ACTION_COMMENT, State.ACTION, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.STATE, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION_COMMENT, State.ACTION_COMMENT, State.ACTION_COMMENT, State.READY, State.ACTION, State.ACTION_COMMENT, State.READY], [State.READY, State.STATE, State.READY, State.STATE_COMMENT, State.READY, State.STATE, State.READY], [State.STATE_COMMENT, State.STATE_COMMENT, State.STATE_COMMENT, State.READY, State.STATE, State.STATE_COMMENT, State.READY]]

class StateMachine:
    def __init__(self, delegate):
        self.state = State.READY
        self.delegate = delegate
        self.transform_actions = [[None, self.delegate.append_tmp, None, None, self.delegate.comment_error, self.delegate.append, None], [None, None, None, self.delegate.comment_error, None, None, None], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [None, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, None], [self.delegate.append_tmp, self.delegate.append, self.delegate.action, None, None, self.delegate.append, self.delegate.action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.combine_tmp_comma_append, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.combine_tmp_comma_action], [self.delegate.action, self.delegate.append_tmp, self.delegate.combine_tmp_comma_action, None, None, self.delegate.combine_tmp_comma_append, self.delegate.action], [None, None, None, self.delegate.comment_error, None, None, self.delegate.action], [self.delegate.state_error, self.delegate.append, self.delegate.state_error, None, self.delegate.comment_error, self.delegate.append, self.delegate.state], [None, None, None, self.delegate.comment_error, None, None, self.delegate.state]]
    def process(self, ctx, event):
        global transform_states
        if self.transform_actions[self.state][event]:
            self.transform_actions[self.state][event](ctx, self.state, event)
        self.state = transform_states[self.state][event]

