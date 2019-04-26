from typing import List, NewType, Union
from abc import ABC, abstractmethod
from lexer_fsm import ActionDelegate as LexerActionDelegate, GuardDelegate as LexerGuardDelegate, VariableDelegate as LexerVariableDelegate, StateMachine as LexerStateMachine
from semantic import Expression, Assignment, Identifier, Literal, Delimiter, Call, Var, Type, UnionType, ListType, MapType

class LexerAdapter(ABC):

  @abstractmethod
  def on_call(self, token: Union[Expression, Assignment]):
    return NotImplemented


class _LexerContext:
  buffer: List[str]

  def __init__(self):
    self.buffer = []


class _LexerActionDelegate(LexerActionDelegate):

  def error(self, ctx):
    print('Unknown error')

  def quit(self, ctx):
    exit(1)

  def add_to_buffer(self, ctx, ch):
    ctx.buffer.append(ch)

  def clear_buffer(self, ctx):
    ctx.buffer.clear()

  def char_error(self, ctx):
    print('Char error')

  def escaped_char_error(self, ctx):
    print('Escaped char error')

  def string_error(self, ctx):
    print('String error')

  def escaped_string_error(self, ctx):
    print('Escaped string error')

  def token(self, ctx):
    tkn = ''.join(ctx.buffer)
    if tkn == 'true':
      return Literal(tkn, 'bool')
    elif tkn == 'false':
      return Literal(tkn, 'bool')
    else:
      return Identifier(tkn)

  def number(self, ctx):
    num = ''.join(ctx.buffer)
    return Literal(num, 'number')

  def char(self, ctx):
    ch = ''.join(ctx.buffer)
    return Literal(ch, 'char')

  def empty_char(self, ctx):
    return Literal('', 'char')

  def escaped_char(self, ctx):
    ch = ''.join(ctx.buffer)
    return Literal(ch, 'char')

  def string(self, ctx):
    string = ''.join(ctx.buffer)
    return Literal(string, 'string')

  def open_bracket(self, ctx):
    return Delimiter('[')

  def close_bracket(self, ctx):
    return Delimiter(']')

  def open_brace(self, ctx):
    return Delimiter('{')

  def close_brace(self, ctx):
    return Delimiter('}')

  def open_parenthesis(self, ctx):
    return Delimiter('(')

  def close_parenthesis(self, ctx):
    return Delimiter(')')

  def my_not(self, ctx):
    return Delimiter('!')

  def dot(self, ctx):
    return Delimiter('.')

  def colon(self, ctx):
    return Delimiter(':')

  def comma(self, ctx):
    return Delimiter(',')

  def pipe(self, ctx):
    return Delimiter('|')

  def assignment(self, ctx):
    return Delimiter('=')

  def equals(self, ctx):
    return Delimiter('==')

  def not_equal_to(self, ctx):
    return Delimiter('!=')

  def less_than(self, ctx):
    return Delimiter('<')

  def less_than_or_equal_to(self, ctx):
    return Delimiter('<=')

  def greater_than(self, ctx):
    return Delimiter('>')

  def greater_than_or_equal_to(self, ctx):
    return Delimiter('>=')


class _LexerGuardDelegate(LexerGuardDelegate):

  def isalpha(self, ch):
    return ch.isalpha()

  def isescaped(self, ch):
    escaped = ['a', 'b', 't', 'n', 'v', 'f', 'r']
    return ch in escaped

  def isdigit(self, ch):
    return ch.isdigit()

  def isspace(self, ch):
    return ch.isspace()


class _LexerVariableDelegate(LexerVariableDelegate):

  def __init__(self, listener: LexerAdapter):
    self._listener = listener

  def on_output_changed(self, output):
    self._listener.on_call(output)


class Lexer:
  def __init__(self, adapter: LexerAdapter = None):
    self._fsm = LexerStateMachine(_LexerActionDelegate(), _LexerGuardDelegate(), _LexerVariableDelegate(adapter))
    self._ctx = _LexerContext()

  def feed(self, ch):
    if ch == '\r' or ch == '\n':
      self._fsm.new_line(self._ctx)
    else:
      self._fsm.input(self._ctx, ch)

  def eof(self):
    self._fsm.eof(self._ctx)
