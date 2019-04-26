from typing import List, NewType, Union

class Delimiter:
  name: str

  def __init__(self, name: str = None):
    self.name = name

  def __str__(self):
    return self.name

  def __repr__(self):
    return 'Delimiter(%s)' % self.name


class Identifier:
  name: str

  def __init__(self, name: str = None):
    self.name = name

  def __str__(self):
    return self.name

  def __repr__(self):
    return 'Identifier(%s)' % self.name


class Literal():
  name: str
  type: str

  def __init__(self, name: str = None, type: str = None):
    self.name = name
    self.type = type

  def __str__(self):
    if self.type == 'char':
      if self.name == "'":
        return "'\\''"
      elif self.name == "\\":
        return "'\\\\'"
      else:
        return "'%s'" % self.name
    elif self.type == 'string':
      return '"%s"' % (self.name.replace('"', '\\"'))
    else:
      return str(self.name)

  def __repr__(self):
    return 'Literal(%s: %s)' % (self.name, self.type)


class Call():
  operator: Identifier
  operands: List[Union[Identifier, Literal]]
  type: Identifier

  def __init__(self, operator: Identifier = None, operands: List[Union[Identifier, Literal]] = [], type: Identifier = None):
    self.operator = operator
    self.operands = operands
    self.type = type

  def __str__(self):
    return '%s(%s)' % (str(self.operator), ', '.join([str(x) for x in self.operands]))

  def __repr__(self):
    return 'Call(%s: %s -> %s)' % (self.operator, self.operands, self.type)


class Expression:
  entity: Union[Identifier, Literal, Call]

  def __init__(self, entity: Union[Identifier, Literal, Call] = None):
    self.entity = entity

  def __str__(self):
    return str(self.entity)

  def __repr__(self):
    return 'Expression(%s)' % self.entity


class BoolExpression(Expression):
  expr: Expression

  def __init__(self, expr: Expression = None):
    self.expr = expr

  def __str__(self):
    return '%s' % (str(self.expr))

  def __repr__(self):
    return 'BoolExpression(%s)' % self.expr


class UnaryBoolExpression(BoolExpression):
  expr: BoolExpression
  op: Identifier

  def __init__(self, op: Identifier = None, expr: BoolExpression = None):
    self.op = op
    self.expr = expr

  def __str__(self):
    return '%s %s' % (str(self.op), str(self.expr))

  def __repr__(self):
    return 'UnaryBoolExpression(%s, %s)' % (self.op, self.exp)


class BinaryBoolExpression(BoolExpression):
  left: BoolExpression
  right: BoolExpression
  op: Identifier

  def __init__(self, left: BoolExpression = None, op: Identifier = None, right: BoolExpression = None):
    self.left = left
    self.op = op
    self.right = right

  def __str__(self):
    if isinstance(self.left, BinaryBoolExpression) or isinstance(self.left, UnaryBoolExpression):
      left = '(%s)' % str(self.left)
    else:
      left = str(self.left)
    if isinstance(self.right, BinaryBoolExpression) or isinstance(self.right, UnaryBoolExpression):
      right = '(%s)' % str(self.right)
    else:
      right = str(self.right)
    return '%s %s %s' % (left, str(self.op), right)

  def __repr__(self):
    return 'BinaryExpression(%s, %s, %s)' % (self.left, self.op, self.right)


class CompareExpression(Expression):
  left: Expression
  right: Expression
  op: Delimiter

  def __init__(self, left: Expression = None, op: Delimiter = None, right: Expression = None):
    self.left = left
    self.op = op
    self.right = right

  def __str__(self):
    return '%s %s %s' % (str(self.left), str(self.op), str(self.right))

  def __repr__(self):
    return 'CompareExpression(%s, %s, %s)' % (self.left, self.op, self.right)


class Accessor():
  accessors: List[Identifier]

  def __init__(self, accessors: List[Identifier] = []):
    self.accessors = accessors

  def __str__(self):
    return '%s' % ('.'.join([str(x) for x in self.accessors]))

  def __repr__(self):
    return 'Accessor(%s)' % (self.accessors)


class Assignment:
  target: Identifier
  type: Identifier
  expression: Expression

  def __init__(self, target: Identifier = None, type: Identifier = None, expression: Expression = None):
    self.target = target
    self.type = type
    self.expression = expression

  def __str__(self):
    if self.type:
      return '%s : %s = %s' % (str(self.target), str(self.type), str(self.expression))
    else:
      return '%s = %s' % (str(self.target), str(self.expression))

  def __repr__(self):
    if self.type:
      return 'Assignment(%s: %s = %s)' % (self.target, self.type, self.expression)
    else:
      return 'Assignment(%s = %s)' % (self.target, self.expression)


class Fun:
  names: List[Union[Identifier, Literal]]

  def __init__(self, name: Union[Identifier, Literal]):
    self.names = [name]

  def __str__(self):
    return ' '.join([str(x) for x in self.names])


class Var:
  name: Identifier

  def __init__(self, name: Identifier = None):
    self.name = name

  def __str__(self):
    return str(self.name)


class Type:
  kind: int

  def __init__(self, kind: int = 0, type = None):
    self.kind = kind
    self.type = type

  def __str__(self):
    return str(self.type)


class UnionType():
  kind: int
  types: List[Type]

  def __init__(self):
    self.kind = 1
    self.types = []

  def __str__(self):
    return ' | '.join([str(x) for x in self.types])


class ListType():
  kind: int
  type: Type

  def __init__(self, type: Type = None):
    self.kind = 2
    self.type = type

  def __str__(self):
    return '[%s]' % str(self.type)


class MapType(Type):
  kind: int
  keytype: Type
  valtype: Type

  def __init__(self, keytype: Type = None, valtype: Type = None):
    self.kind = 3
    self.keytype = keytype
    self.valtype = valtype

  def __str__(self):
    return '{%s: %s}' % (str(self.keytype), str(self.valtype))
