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

class StateMachine:
    def append_tmp(self, ctx, state = 0, event = 0):
        pass
    def comment_error(self, ctx, state = 0, event = 0):
        pass
    def append(self, ctx, state = 0, event = 0):
        pass
    def combine_tmp_comma_append(self, ctx, state = 0, event = 0):
        pass
    def combine_tmp_comma_action(self, ctx, state = 0, event = 0):
        pass
    def action(self, ctx, state = 0, event = 0):
        pass
    def state_error(self, ctx, state = 0, event = 0):
        pass
    def state(self, ctx, state = 0, event = 0):
        pass
    def __init__(self, delegate):
        self.append_tmp = delegate.append_tmp
        self.comment_error = delegate.comment_error
        self.append = delegate.append
        self.combine_tmp_comma_append = delegate.combine_tmp_comma_append
        self.combine_tmp_comma_action = delegate.combine_tmp_comma_action
        self.action = delegate.action
        self.state_error = delegate.state_error
        self.state = delegate.state
        self.transform_states = [[State.READY, State.MINUS, State.STATE, State.READY_COMMENT, State.READY, State.ACTION, State.READY], [State.READY_COMMENT, State.READY_COMMENT, State.READY_COMMENT, State.READY, State.READY, State.READY_COMMENT, State.READY_COMMENT], [State.ACTION, State.MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS, State.ACTION, State.READY], [State.ACTION, State.MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS, State.ACTION, State.READY], [State.ACTION, State.MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.STATE, State.MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.MINUS_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION_LF, State.ACTION, State.STATE, State.ACTION_COMMENT, State.ACTION, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.STATE, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.STATE, State.ACTION_COMMENT, State.ACTION_LF_MINUS_MINUS_MINUS_MINUS, State.ACTION, State.READY], [State.ACTION_COMMENT, State.ACTION_COMMENT, State.ACTION_COMMENT, State.READY, State.ACTION, State.ACTION_COMMENT, State.READY], [State.READY, State.STATE, State.READY, State.STATE_COMMENT, State.READY, State.STATE, State.READY], [State.STATE_COMMENT, State.STATE_COMMENT, State.STATE_COMMENT, State.READY, State.STATE, State.STATE_COMMENT, State.READY]]
        self.transform_actions = [[None, self.append_tmp, None, None, self.comment_error, self.append, None], [None, None, None, self.comment_error, None, None, None], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [None, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, None], [self.append_tmp, self.append, self.action, None, None, self.append, self.action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.combine_tmp_comma_append, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.combine_tmp_comma_action], [self.action, self.append_tmp, self.combine_tmp_comma_action, None, None, self.combine_tmp_comma_append, self.action], [None, None, None, self.comment_error, None, None, self.action], [self.state_error, self.append, self.state_error, None, self.comment_error, self.append, self.state], [None, None, None, self.comment_error, None, None, self.state]]
        self.state = State.READY
    def process(self, ctx, event):
        if self.transform_actions[self.state][event]:
            self.transform_actions[self.state][event](ctx, self.state, event)
        self.state = self.transform_states[self.state][event]

