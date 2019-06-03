def _python_normalize(string: str) -> str:
    keywords = [ "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield" ]
    if string in keywords:
        return 'my_' + string
    else:
        return string

def preprocess(cell, as_key = False):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if as_key:
        if cell[0].isdigit():
            cell = "NUMBER_" + cell
        cell = _python_normalize(cell)
    return cell

def state(prefix, states):
    i = 1
    output = "class State:\n"
    for s in states:
        output += " " * 4 + s + " = %d\n" % i
        i += 1
    return output

def action(prefix, actions):
    output = 'class Delegate(ABC):\n\n'
    for action in actions:
        output += ' ' * 4 + '@abstractmethod\n'
        output += ' ' * 4 + 'def %s(self, ctx):\n' % (action.lower())
        output += ' ' * 8 + "return NotImplemented\n\n"
    return output

def code_transforming(prefix, states, events, transformings, debug):
    output = "class StateMachine:\n\n"
    output += " " * 4 + "def __init__(self, delegate):\n"
    output += " " * 8 + "self.delegate = delegate\n"
    output += " " * 8 + "self.state = State.%s\n\n" % states[0]
    for ei in range(len(events)):
        evt = events[ei]
        output += " " * 4 + "def %s(self, ctx):\n" % preprocess(evt, as_key = True).lower()
        first_state = True
        stmt = 0
        for si in range(len(states)):
            st = states[si]
            (actions, state) = transformings[si][ei]
            if len(actions) == 0 and state == None and not debug:
                continue
            stmt += 1
            if first_state:
                first_state = False
                output += " " * 8 + "if self.state == State.%s:\n" % preprocess(st)
            else:
                output += " " * 8 + "elif self.state == State.%s:\n" % preprocess(st)
            if len(actions) > 1:
                if debug:
                    actionstr = '{0}'.format(' |> '.join([x.upper() for x in actions]))
                    output += " " * 12 + 'print("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], actionstr, preprocess(state) if state else 'N/A')
                for action in actions:
                    output += " " * 12 + "self.delegate.%s(ctx)\n" % action.lower()
            elif len(actions) == 1:
                action = preprocess(actions[0])
                if debug:
                    output += " " * 12 + 'print("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], action.upper(), preprocess(state) if state else 'N/A')
                output += " " * 12 + "self.delegate.%s(ctx)\n" % action.lower()
            else:
                if debug:
                    output += " " * 12 + 'print("(%s, %s) => (N/A, %s)")\n' % (events[ei], states[si], preprocess(state) if state else 'N/A')
            if state:
                output += " " * 12 + "self.state = State.%s\n" % preprocess(state)
        if stmt == 0:
            output += " " * 8 + "pass\n\n"
        else:
            output += "\n"
    return output

def table_transforming(prefix, states, events, actions, transformings, debug):
    output = ''
    if debug:
        output += "_state_strings = [%s]\n" % (", ".join(['""'] + ["\"%s\"" % state for state in states]))
        actions_table = ['[%s]' % ', '.join(['"N/A"'] * len(events))]
        for si in range(len(states)):
            actions = []
            for ei in range(len(events)):
                (_actions, state) = transformings[si][ei]
                if len(_actions) > 0:
                    actions.append('"{0}"'.format(' |> '.join([x.upper() for x in _actions])))
                else:
                    actions.append('"N/A"')
            actions_table.append("[%s]" % ", ".join(actions))
        output += "_action_strings = [%s]\n" % (", ".join(actions_table))
    transforming_states_table = ['[%s]' % ', '.join(['0'] * len(events))]
    for si in range(len(states)):
        transforming_states = []
        for ei in range(len(events)):
            (_, state) = transformings[si][ei]
            if state:
                transforming_states.append(states.index(state) - si)
            else:
                transforming_states.append(0)
        transforming_states_table.append("[%s]" % ", ".join(['%d' % x for x in transforming_states]))
    output += "_transform_states = [%s]\n" % (", ".join(transforming_states_table))
    output += '\n'
    output += "class StateMachine:\n\n"
    output += " " * 4 + "def __init__(self, delegate):\n"
    output += " " * 8 + "self.state = State.%s\n" % states[0]
    output += " " * 8 + "self.delegate = delegate\n"
    actionid = 1
    inner_actions = {}
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (actions, state) = transformings[si][ei]
            if len(actions) == 1:
                transforming_actions.append(preprocess(str(actions[0])).lower())
            elif len(actions) > 1:
                key = "".join([str(a) for a in actions])
                if key not in inner_actions:
                    transforming_actions.append(actionid)
                    inner_actions[key] = (actionid, actions)
                    actionid += 1
                else:
                    (aid, _) = inner_actions[key]
                    transforming_actions.append(aid)
            else:
                transforming_actions.append(None)
        transforming_actions_table.append(transforming_actions)
    output += " " * 8 + "self._transform_actions = [%s]\n\n" % (", ".join(['[%s]' % ', '.join(['self._noop'] * len(events))] + ["[%s]" % ", ".join([('self._noop' if y is None else ('self.delegate.' + y if isinstance(y, str) else 'self._action_%d' % y)) for y in x]) for x in transforming_actions_table]))
    output += " " * 4 + "def _noop(self, ctx):\n"
    output += " " * 8 + "pass\n\n"
    for evt in events:
        ei = events.index(evt)
        event = preprocess(evt, as_key = True)
        output += " " * 4 + "def %s(self, ctx):\n" % (event.lower())
        output += " " * 8 + "global _transform_states\n"
        if debug:
            output += " " * 8 + "global _state_strings, _event_strings, _action_strings\n"
            output += " " * 8 + 'print("({1}, %s) => (%s, %s)" % (_state_strings[self.state], _action_strings[self.state][{0}], _state_strings[self.state +_transform_states[self.state][{0}]]))\n'.format(ei, preprocess(evt).upper());
        output += " " * 8 + "self._transform_actions[self.state][%d](ctx)\n" % ei
        output += " " * 8 + "self.state += _transform_states[self.state][%d]\n\n" % ei
    for (actionid, actions) in inner_actions.values():
        output += ' ' * 4 + 'def _action_%d(self, ctx):\n' % actionid
        for action in actions:
            output += ' ' * 8 + 'self.delegate.%s(ctx)\n' % action
        output += '\n'
    return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings):
    import os.path
    states = [preprocess(state, as_key = True) for state in states]
    events = [preprocess(event) for event in events]
    actions = [preprocess(action, as_key = True) for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    dest = os.path.join(directory, root.replace("-", "_") + ".py")
    with open(dest, 'w') as output:
        output.write('from abc import ABC, abstractmethod\n\n')
        output.write(state(prefix, states))
        output.write("\n");
        output.write(action(prefix, actions))
        output.write("\n");
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug))
        output.write("\n");
