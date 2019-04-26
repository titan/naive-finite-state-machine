from typing import List, NewType, Union
from abc import ABC, abstractmethod
from action_fsm import ActionDelegate as ActionActionDelegate, GuardDelegate as ActionGuardDelegate, VariableDelegate as ActionVariableDelegate, StateMachine as ActionStateMachine
from semantic import Expression, Assignment, Identifier, Literal, Delimiter, Call, BoolExpression, UnaryBoolExpression, BinaryBoolExpression, CompareExpression, Accessor, Fun, Var, Type, UnionType, ListType, MapType


def find_call_in_expression(exp: Expression):
  if isinstance(exp, Call):
    yield exp
  elif isinstance(exp, BinaryBoolExpression):
    for x in find_call_in_expression(exp.left):
      yield x
    for y in find_call_in_expression(exp.right):
      yield y
  elif isinstance(exp, UnaryBoolExpression):
    for x in find_call_in_expression(exp.expr):
      yield x
  elif isinstance(exp, CompareExpression):
    for x in find_call_in_expression(exp.left):
      yield x
    for y in find_call_in_expression(exp.right):
      yield y
  elif isinstance(exp, BoolExpression):
    for x in find_call_in_expression(exp.expr):
      yield x
  elif isinstance(exp, Expression):
    for x in find_call_in_expression(exp.entity):
      yield x


class _ActionContext:
  action: Union[Assignment, Call]

  def __init__(self, fsm = None):
    self.fsm = fsm
    self.queue = []
    self.delay_queue = []
    self.state_stack = []
    self.stack = []
    self.action = None
    self.input = None


class _ActionActionDelegate(ActionActionDelegate):

  def shift(self, ctx, l):
    ctx.state_stack.append(ctx.fsm.state)
    ctx.stack.append(l)

  def syntax_error(self, ctx):
    print("syntax error in action syntaxer")
    print("current state: %d" % ctx.fsm.state)
    print("stack: %s" % ctx.stack)
    print("state stack: %s" % ctx.state_stack)
    print("input: %s" % ctx.input)

  def quit(self, ctx):
    exit(1)

  def reduce_to_action(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.action = ctx.stack.pop()

  def reduce_1_to_fun(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    id = ctx.stack.pop()
    ctx.queue.append(Fun(id))

  def enqueue(self, ctx, e):
    ctx.delay_queue.append(e)

  def reduce_5_to_assignment(self, ctx, c):
    ctx.fsm.state = ctx.state_stack.pop()
    call = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    type = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    id = ctx.stack.pop()
    ctx.queue.append(Assignment(id, type, call))

  def reduce_3_to_assignment(self, ctx, c):
    ctx.fsm.state = ctx.state_stack.pop()
    call = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    id = ctx.stack.pop()
    ctx.queue.append(Assignment(id, None, call))

  def reduce_2_to_fun(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    id = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    fun = ctx.stack.pop()
    fun.names.append(id)
    ctx.queue.append(fun)

  def reduce_1_to_call(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    fun = ctx.stack.pop()
    ctx.queue.append(Call(fun, []))

  def reduce_1_to_operands(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    operand = ctx.stack.pop()
    ctx.queue.append([operand])

  def reduce_3_to_call(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    fun = ctx.stack.pop()
    ctx.queue.append(Call(fun, []))

  def reduce_4_to_call(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    operands = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    fun = ctx.stack.pop()
    ctx.queue.append(Call(fun, operands))

  def reduce_2_to_operands(self, ctx):
    ctx.fsm.state = ctx.state_stack.pop()
    operand1 = ctx.stack.pop()
    ctx.fsm.state = ctx.state_stack.pop()
    operand2 = ctx.stack.pop()
    ctx.queue.append(operand2 + operand1)


class ActionSyntaxer:

  def __init__(self):
    self._fsm = ActionStateMachine(_ActionActionDelegate(), None, None)
    self._ctx = _ActionContext(self._fsm)

  def identifier(self, id):
    self._consume_queue()
    self._ctx.input = id
    self._fsm.identifier(self._ctx, id)
    self._consume_queue()

  def literal(self, l):
    self._consume_queue()
    self._ctx.input = l
    self._fsm.literal(self._ctx, l)
    self._consume_queue()

  def delimiter(self, d):
    self._consume_queue()
    self._ctx.input = d
    self._fsm.delimiter(self._ctx, d)
    self._consume_queue()

  def eof(self):
    self._consume_queue()
    self._ctx.input = 'eof'
    self._fsm.eof(self._ctx, 0)
    self._consume_queue()

  def result(self):
    return self._ctx.action

  def _consume_queue(self):
    while len(self._ctx.queue) > 0:
      n = self._ctx.queue[0]
      self._ctx.queue = self._ctx.queue[1:]
      self._ctx.input = n
      self._feed(n)
    while len(self._ctx.delay_queue) > 0:
      while len(self._ctx.queue) > 0:
        n = self._ctx.queue[0]
        self._ctx.queue = self._ctx.queue[1:]
        self._ctx.input = n
        self._feed(n)
      d = self._ctx.delay_queue[0]
      self._ctx.delay_queue = self._ctx.delay_queue[1:]
      self._ctx.input = d
      self._feed(d)

  def _feed(self, n):
    if isinstance(n, Assignment):
      self._fsm.assignment(self._ctx, n)
    elif isinstance(n, Call):
      self._fsm.call(self._ctx, n)
    elif isinstance(n, Fun):
      self._fsm.fun(self._ctx, n)
    elif isinstance(n, Identifier):
      self._fsm.identifier(self._ctx, n)
    elif isinstance(n, Literal):
      self._fsm.literal(self._ctx, n)
    elif isinstance(n, Delimiter):
      self._fsm.delimiter(self._ctx, n)
    elif isinstance(n, list):
      self._fsm.operands(self._ctx, n)
    elif isinstance(n, int):
      self._fsm.eof(self._ctx, n)


class ActionLexerAdapter:

  def __init__(self, syntaxer: ActionSyntaxer):
    self._syntaxer = syntaxer

  def on_call(self, token):
    if isinstance(token, Identifier):
      self._syntaxer.identifier(token)
    elif isinstance(token, Literal):
      self._syntaxer.literal(token)
    elif isinstance(token, Delimiter):
      self._syntaxer.delimiter(token)
    else:
      print('Unknown token in parameter lexer adapter: %s' % (repr(token)))
      exit(1)
