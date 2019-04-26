from abc import ABC, abstractmethod

class State:
  INIT = 0
  TOKEN = 1
  NUMBER = 2
  CHAR_READY = 3
  CHAR = 4
  ESCAPED_CHAR_READY = 5
  ESCAPED_CHAR = 6
  STRING = 7
  ESCAPED_STRING = 8
  EQUALS = 9
  DOUBLE_EQUALS = 10
  EXCLAM = 11
  NOT_EQUAL_TO = 12
  LESS_THAN = 13
  LESS_THAN_OR_EQUAL_TO = 14
  GREATER_THAN = 15
  GREATER_THAN_OR_EQUAL_TO = 16


class ActionDelegate(ABC):

  @abstractmethod
  def open_parenthesis(self, ctx):
    return NotImplemented

  @abstractmethod
  def close_parenthesis(self, ctx):
    return NotImplemented

  @abstractmethod
  def open_bracket(self, ctx):
    return NotImplemented

  @abstractmethod
  def close_bracket(self, ctx):
    return NotImplemented

  @abstractmethod
  def open_brace(self, ctx):
    return NotImplemented

  @abstractmethod
  def close_brace(self, ctx):
    return NotImplemented

  @abstractmethod
  def error(self, ctx):
    return NotImplemented

  @abstractmethod
  def quit(self, ctx):
    return NotImplemented

  @abstractmethod
  def colon(self, ctx):
    return NotImplemented

  @abstractmethod
  def comma(self, ctx):
    return NotImplemented

  @abstractmethod
  def pipe(self, ctx):
    return NotImplemented

  @abstractmethod
  def add_to_buffer(self, ctx, ch):
    return NotImplemented

  @abstractmethod
  def token(self, ctx):
    return NotImplemented

  @abstractmethod
  def clear_buffer(self, ctx):
    return NotImplemented

  @abstractmethod
  def dot(self, ctx):
    return NotImplemented

  @abstractmethod
  def number(self, ctx):
    return NotImplemented

  @abstractmethod
  def empty_char(self, ctx):
    return NotImplemented

  @abstractmethod
  def char_error(self, ctx):
    return NotImplemented

  @abstractmethod
  def char(self, ctx):
    return NotImplemented

  @abstractmethod
  def escaped_char_error(self, ctx):
    return NotImplemented

  @abstractmethod
  def escaped_char(self, ctx):
    return NotImplemented

  @abstractmethod
  def string(self, ctx):
    return NotImplemented

  @abstractmethod
  def string_error(self, ctx):
    return NotImplemented

  @abstractmethod
  def escaped_string_error(self, ctx):
    return NotImplemented

  @abstractmethod
  def assignment(self, ctx):
    return NotImplemented

  @abstractmethod
  def equals(self, ctx):
    return NotImplemented

  @abstractmethod
  def my_not(self, ctx):
    return NotImplemented

  @abstractmethod
  def not_equal_to(self, ctx):
    return NotImplemented

  @abstractmethod
  def less_than(self, ctx):
    return NotImplemented

  @abstractmethod
  def less_than_or_equal_to(self, ctx):
    return NotImplemented

  @abstractmethod
  def greater_than(self, ctx):
    return NotImplemented

  @abstractmethod
  def greater_than_or_equal_to(self, ctx):
    return NotImplemented



class GuardDelegate(ABC):

  @abstractmethod
  def isescaped(self, ctx, ch):
    return NotImplemented

  @abstractmethod
  def isdigit(self, ctx, ch):
    return NotImplemented

  @abstractmethod
  def isalpha(self, ctx, ch):
    return NotImplemented

  @abstractmethod
  def isspace(self, ctx, ch):
    return NotImplemented



class VariableDelegate(ABC):

  @abstractmethod
  def on_output_changed(self, output):
    return NotImplemented



_transactions_target = [[State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.EQUALS, State.EXCLAM, State.LESS_THAN, State.GREATER_THAN, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.EQUALS, State.EXCLAM, State.LESS_THAN, State.GREATER_THAN, State.INIT, State.TOKEN, State.TOKEN, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.EQUALS, State.EXCLAM, State.LESS_THAN, State.GREATER_THAN, State.NUMBER, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.INIT, State.ESCAPED_CHAR_READY, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.CHAR, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.ESCAPED_CHAR, State.ESCAPED_CHAR, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.ESCAPED_CHAR, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT], [State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.INIT, State.STRING, State.ESCAPED_STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.STRING, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.STRING, State.STRING, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.DOUBLE_EQUALS, State.EXCLAM, State.LESS_THAN_OR_EQUAL_TO, State.GREATER_THAN_OR_EQUAL_TO, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.EXCLAM, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.NOT_EQUAL_TO, State.INIT, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.EXCLAM, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.LESS_THAN_OR_EQUAL_TO, State.INIT, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.GREATER_THAN_OR_EQUAL_TO, State.INIT, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT], [State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.STRING, State.CHAR_READY, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.INIT, State.TOKEN, State.NUMBER, State.TOKEN, State.INIT, State.INIT, State.INIT]]


class StateMachine:
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE = 0
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE = 1
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE = 2
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE = 3
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE = 4
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE = 5
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE = 6
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE = 7
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE = 8
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE = 9
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE = 10
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE = 11
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE = 12
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE = 13
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE = 14
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE = 15
  INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE = 16
  INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS = 17
  INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS = 18
  INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS = 19
  INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS = 20
  NEW_LINE = 21
  EOF = 22

  def __init__(self, action_delegate = None, guard_delegate = None, variable_delegate = None):
    self.state = State.INIT
    self.action_delegate = action_delegate
    self.guard_delegate = guard_delegate
    self.variable_delegate = variable_delegate
    self._transactions_action = [[self._action_block_0, self._action_block_1, self._action_block_2, self._action_block_3, self._action_block_4, self._action_block_5, None, None, self._action_block_6, self._action_block_7, self._action_block_8, self._action_block_9, None, None, None, None, self._action_block_6, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, None, None, None], [self._action_block_10, self._action_block_11, self._action_block_12, self._action_block_13, self._action_block_14, self._action_block_15, self._action_block_16, self._action_block_16, self._action_block_6, self._action_block_17, self._action_block_18, self._action_block_19, self._action_block_16, self._action_block_16, self._action_block_16, self._action_block_16, self._action_block_20, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_16, self._action_block_21, self._action_block_21], [self._action_block_22, self._action_block_23, self._action_block_24, self._action_block_25, self._action_block_26, self._action_block_27, self._action_block_28, self._action_block_28, self._action_block_6, self._action_block_29, self._action_block_30, self._action_block_31, self._action_block_28, self._action_block_28, self._action_block_28, self._action_block_28, self.action_delegate.add_to_buffer, self._action_block_32, self.action_delegate.add_to_buffer, self._action_block_32, self._action_block_28, self._action_block_33, self._action_block_33], [self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_34, None, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_35, self._action_block_35], [self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_37, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_36, self._action_block_35, self._action_block_35], [self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self.action_delegate.add_to_buffer, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_39, self._action_block_39], [self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_40, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_38, self._action_block_39, self._action_block_39], [self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_41, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_42, self._action_block_42], [self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self.action_delegate.add_to_buffer, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_43, self.action_delegate.add_to_buffer, self._action_block_43, self._action_block_43, self._action_block_43, self._action_block_44, self._action_block_44], [self._action_block_45, self._action_block_46, self._action_block_47, self._action_block_48, self._action_block_49, self._action_block_50, self._action_block_51, self._action_block_51, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, None, self._action_block_51, None, None, self._action_block_6, self._action_block_52, self._action_block_52, self._action_block_52, self._action_block_51, self._action_block_53, self._action_block_53], [self._action_block_54, self._action_block_55, self._action_block_56, self._action_block_57, self._action_block_58, self._action_block_59, self._action_block_60, self._action_block_60, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_60, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_61, self._action_block_61, self._action_block_61, self._action_block_60, self._action_block_53, self._action_block_53], [self._action_block_62, self._action_block_63, self._action_block_64, self._action_block_65, self._action_block_66, self._action_block_67, self._action_block_68, self._action_block_68, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, None, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_69, self._action_block_69, self._action_block_69, self._action_block_68, self._action_block_53, self._action_block_53], [self._action_block_70, self._action_block_71, self._action_block_72, self._action_block_73, self._action_block_74, self._action_block_75, self._action_block_76, self._action_block_76, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_76, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_77, self._action_block_77, self._action_block_77, self._action_block_76, self._action_block_53, self._action_block_53], [self._action_block_78, self._action_block_79, self._action_block_80, self._action_block_81, self._action_block_82, self._action_block_83, self._action_block_84, self._action_block_84, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, None, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_85, self._action_block_85, self._action_block_85, self._action_block_84, self._action_block_53, self._action_block_53], [self._action_block_86, self._action_block_87, self._action_block_88, self._action_block_89, self._action_block_90, self._action_block_91, self._action_block_92, self._action_block_92, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_93, self._action_block_93, self._action_block_93, self._action_block_92, self._action_block_53, self._action_block_53], [self._action_block_94, self._action_block_95, self._action_block_96, self._action_block_97, self._action_block_98, self._action_block_99, self._action_block_100, self._action_block_100, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, None, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_101, self._action_block_101, self._action_block_101, self._action_block_100, self._action_block_53, self._action_block_53], [self._action_block_102, self._action_block_103, self._action_block_104, self._action_block_105, self._action_block_106, self._action_block_107, self._action_block_108, self._action_block_108, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_6, self._action_block_109, self._action_block_109, self._action_block_109, self._action_block_108, self._action_block_53, self._action_block_53]]

  def input(self, ctx, ch):
    if ch == '(':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_PARENTHESIS_APOSTROPHE]
    elif ch == ')':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_PARENTHESIS_APOSTROPHE]
    elif ch == '[':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACKET_APOSTROPHE]
    elif ch == ']':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACKET_APOSTROPHE]
    elif ch == '{':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_OPEN_BRACE_APOSTROPHE]
    elif ch == '}':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_CLOSE_BRACE_APOSTROPHE]
    elif ch == '"':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOUBLE_QUOTES_APOSTROPHE]
    elif ch == '\'':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_APOSTROPHE_APOSTROPHE]
    elif ch == '\\':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_BACKSLASH_BACKSLASH_APOSTROPHE]
    elif ch == ':':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COLON_APOSTROPHE]
    elif ch == ',':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_COMMA_APOSTROPHE]
    elif ch == '|':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_PIPE_APOSTROPHE]
    elif ch == '=':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EQUALS_APOSTROPHE]
    elif ch == '!':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_EXCLAM_APOSTROPHE]
    elif ch == '<':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_LESS_THAN_APOSTROPHE]
    elif ch == '>':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_GREATER_THAN_APOSTROPHE]
    elif ch == '.':
      if self.state == _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE]:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE]:
          self._transactions_action[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_CH_DOUBLE_EQUALS_APOSTROPHE_DOT_APOSTROPHE]
    elif self.guard_delegate.isescaped(ch):
      if self.state == _transactions_target[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
        if self._transactions_action[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_ISESCAPED_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]
    elif self.guard_delegate.isdigit(ch):
      if self.state == _transactions_target[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
        if self._transactions_action[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_ISDIGIT_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]
    elif self.guard_delegate.isalpha(ch):
      if self.state == _transactions_target[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
        if self._transactions_action[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_ISALPHA_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]
    elif self.guard_delegate.isspace(ch):
      if self.state == _transactions_target[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
        if self._transactions_action[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
      else:
        if self._transactions_action[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]:
          self._transactions_action[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS](ctx, ch)
        self.state = _transactions_target[self.state][self.INPUT_ISSPACE_OPEN_PARENTHESIS_CH_CLOSE_PARENTHESIS]

  def new_line(self, ctx):
    if self.state == _transactions_target[self.state][self.NEW_LINE]:
      if self._transactions_action[self.state][self.NEW_LINE]:
        self._transactions_action[self.state][self.NEW_LINE](ctx)
    else:
      if self._transactions_action[self.state][self.NEW_LINE]:
        self._transactions_action[self.state][self.NEW_LINE](ctx)
      self.state = _transactions_target[self.state][self.NEW_LINE]

  def eof(self, ctx):
    if self.state == _transactions_target[self.state][self.EOF]:
      if self._transactions_action[self.state][self.EOF]:
        self._transactions_action[self.state][self.EOF](ctx)
    else:
      if self._transactions_action[self.state][self.EOF]:
        self._transactions_action[self.state][self.EOF](ctx)
      self.state = _transactions_target[self.state][self.EOF]

  def _action_block_0(self, ctx, ch):
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_1(self, ctx, ch):
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_2(self, ctx, ch):
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_3(self, ctx, ch):
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_4(self, ctx, ch):
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_5(self, ctx, ch):
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_6(self, ctx, ch):
      self.action_delegate.error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_7(self, ctx, ch):
      output = self.action_delegate.colon(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_8(self, ctx, ch):
      output = self.action_delegate.comma(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_9(self, ctx, ch):
      output = self.action_delegate.pipe(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_10(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_11(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_12(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_13(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_14(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_15(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_16(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_17(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.colon(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_18(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.comma(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_19(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.pipe(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_20(self, ctx, ch):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.dot(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_21(self, ctx):
      output = self.action_delegate.token(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_22(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_23(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_24(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_25(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_26(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_27(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_28(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_29(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.colon(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_30(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.comma(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_31(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      output = self.action_delegate.pipe(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_32(self, ctx, ch):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_33(self, ctx):
      output = self.action_delegate.number(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_34(self, ctx, ch):
      output = self.action_delegate.empty_char(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_35(self, ctx):
      self.action_delegate.char_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_36(self, ctx, ch):
      self.action_delegate.char_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_37(self, ctx, ch):
      output = self.action_delegate.char(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_38(self, ctx, ch):
      self.action_delegate.escaped_char_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_39(self, ctx):
      self.action_delegate.escaped_char_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_40(self, ctx, ch):
      output = self.action_delegate.escaped_char(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_41(self, ctx, ch):
      output = self.action_delegate.string(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.clear_buffer(ctx)

  def _action_block_42(self, ctx):
      self.action_delegate.string_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_43(self, ctx, ch):
      self.action_delegate.escaped_string_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_44(self, ctx):
      self.action_delegate.escaped_string_error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_45(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_46(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_47(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_48(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_49(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_50(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_51(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_52(self, ctx, ch):
      output = self.action_delegate.assignment(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_53(self, ctx):
      self.action_delegate.error(ctx)
      self.action_delegate.quit(ctx)

  def _action_block_54(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_55(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_56(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_57(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_58(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_59(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_60(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_61(self, ctx, ch):
      output = self.action_delegate.equals(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_62(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_63(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_64(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_65(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_66(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_67(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_68(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_69(self, ctx, ch):
      output = self.action_delegate.my_not(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_70(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_71(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_72(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_73(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_74(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_75(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_76(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_77(self, ctx, ch):
      output = self.action_delegate.not_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_78(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_79(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_80(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_81(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_82(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_83(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_84(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_85(self, ctx, ch):
      output = self.action_delegate.less_than(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_86(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_87(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_88(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_89(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_90(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_91(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_92(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_93(self, ctx, ch):
      output = self.action_delegate.less_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_94(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_95(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_96(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_97(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_98(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_99(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_100(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_101(self, ctx, ch):
      output = self.action_delegate.greater_than(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

  def _action_block_102(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_103(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_parenthesis(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_104(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_105(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_bracket(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_106(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.open_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_107(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      output = self.action_delegate.close_brace(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_108(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)

  def _action_block_109(self, ctx, ch):
      output = self.action_delegate.greater_than_or_equal_to(ctx)
      self.variable_delegate.on_output_changed(output)
      self.action_delegate.add_to_buffer(ctx, ch)

