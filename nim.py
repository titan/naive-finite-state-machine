def preprocess(cell, as_key = False):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if as_key:
        if cell[0].isdigit():
            cell = "NUMBER_" + cell
    return cell

def state(prefix, states):
    output = ' ' * 2 + 'State* = enum\n'
    output += ' ' * 4 + ', '.join(['%s = %d' % (x, states.index(x) + 1) for x in states])
    output += '\n'
    return output

def action(prefix, actions):
    output = ' ' * 2 + 'StateMachineDelegate*[T] = object of RootObj\n'
    for action in actions:
        output += ' ' * 4 + '%s*: proc (ctx: var T)\n' % (action.lower())
    return output

def code_transforming(prefix, states, events, transformings, debug):
    output = ' ' * 2 + 'StateMachine*[T] = object of RootObj\n'
    output += ' ' * 4 + 'state*: State\n'
    output += ' ' * 4 + 'delegate: StateMachineDelegate[T]\n\n'
    output += 'proc initStateMachine*[T](state: State, delegate: StateMachineDelegate[T]): StateMachine[T] =\n'
    output += ' ' * 2 + 'result = StateMachine[T](state: state, delegate: delegate)\n\n' % (states[0])
    output += 'proc initStateMachine*[T](delegate: StateMachineDelegate[T]): StateMachine[T] =\n'
    output += ' ' * 2 + 'result = StateMachine[T](state: State.%s, delegate: delegate)\n\n' % (states[0])
    for ei in range(len(events)):
        output += 'proc %s*[T](fsm: var StateMachine[T], ctx: var T) =\n' % (preprocess(events[ei], as_key = True).lower())
        output += ' ' * 2 + 'case fsm.state:\n'
        count = 0
        for si in range(len(states)):
            (actions, state) = transformings[si][ei]
            if state:
                count += 1
                output += ' ' * 4 + 'of State.%s:\n' % (states[si])
                if len(actions) > 0:
                    if debug:
                        output += ' ' * 6 + 'echo("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], ' |> '.join([preprocess(x).upper() for x in actions]), state)
                    for action in actions:
                        output += ' ' * 6 + 'fsm.delegate.%s(ctx)\n' % (action.lower())
                else:
                    if debug:
                        output += ' ' * 6 + 'echo("(%s, %s) => (N/A, %s)");\n' % (events[ei], states[si], preprocess(state))
                if state != states[si]:
                    output += ' ' * 6 + 'fsm.state = State.%s\n' % (preprocess(state))
            elif len(actions) > 0:
                count += 1
                output += ' ' * 4 + 'of State.%s:\n' % (states[si])
                if debug:
                    output += ' ' * 6 + 'echo("(%s, %s) => (%s, N/A)")\n' % (events[ei], states[si], ' |> '.join([preprocess(x).upper() for x in actions]))
                for action in actions:
                    output += ' ' * 6 + 'fsm.delegate.%s(ctx)\n' % (action.lower())
            else:
                pass
        if count != len(states):
            output += ' ' * 4 + 'else:\n'
            output += ' ' * 6 + 'discard\n'
        output += '\n'
    return output

def table_transforming(prefix, states, events, actions, transformings, debug):
    output = ' ' * 2 + 'StateMachine*[T] = object of RootObj\n'
    output += ' ' * 4 + 'state*: int\n'
    output += ' ' * 4 + 'delegate: StateMachineDelegate[T]\n'
    output += ' ' * 4 + 'transform_actions: array[0..%d, proc (delegate: StateMachineDelegate[T], ctx: var T)]\n\n' % ((len(states) + 1)* len(events) - 1)
    if debug:
        output += 'const state_strings: array[0..%d, string] = [%s]\n' % (len(states), ', '.join(['""'] + ['"%s"' % state for state in states]))
        actions_table = ['%s' % ', '.join(['"N/A"'] * len(events))]
        for si in range(len(states)):
            actions = []
            for ei in range(len(events)):
                (_actions, state) = transformings[si][ei]
                if len(_actions) > 0:
                    actions.append('"{0}"'.format(' |> '.join([x.upper() for x in _actions])))
                else:
                    actions.append('"N/A"')
            actions_table.append("%s" % ', '.join(actions))
        output += 'const action_strings: array[0..%d, string] = [%s]\n' % ((len(states) + 1) * len(events) - 1, ', '.join(actions_table))
    transforming_states_table = ['%s' % ', '.join(['0'] * len(events))]
    for si in range(len(states)):
        transforming_states = []
        for ei in range(len(events)):
            (_, state) = transformings[si][ei]
            if state:
                transforming_states.append(states.index(state) - si)
            else:
                transforming_states.append(0)
        transforming_states_table.append('%s' % ', '.join(['%d' % x for x in transforming_states]))
    output += 'const transform_states: array[0..%d, int] = [%s];\n\n' % ((len(states) + 1) * len(events) - 1, ', '.join(transforming_states_table))
    actionid = 1
    inner_actions = {}
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (actions, state) = transformings[si][ei]
            if len(actions) > 0:
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
    output += 'proc initStateMachine*[T](state: int, delegate: StateMachineDelegate[T]): StateMachine[T] =\n\n'
    output += ' ' * 2 + 'proc noop[T](delegate: StateMachineDelegate[T], ctx: var T) {.closure.} =\n'
    output += ' ' * 4 + 'discard\n\n'
    for (actionid, actions) in inner_actions.values():
        output += ' ' * 2 + 'proc action_%d[T](delegate: StateMachineDelegate[T], ctx: var T) {.closure, noSideEffect, gcsafe, locks: 0.} =\n' % actionid
        for action in actions:
            output += ' ' * 4 + 'delegate.%s(ctx)\n' % action
        output += '\n'
    output += ' ' * 2 + 'let actions: array[0..%d, proc (delegate: StateMachineDelegate[T], ctx: var T)] = [%s]\n' % ((len(states) + 1) * len(events) - 1, ', '.join(['%s' % ', '.join(['noop[T]'] * len(events))] + ['%s' % ', '.join(['noop[T]' if y is None else 'action_%d[T]' % y for y in x]) for x in transforming_actions_table]))
    output += ' ' * 2 + 'result = StateMachine[T](state: state, delegate: delegate, transform_actions: actions)\n\n'
    output += 'proc initStateMachine*[T](delegate: StateMachineDelegate[T]): StateMachine[T] =\n'
    output += ' ' * 2 + 'result = initStateMachine[T](ord(State.%s), delegate)\n\n' % (states[0])
    for evt in events:
        event = preprocess(evt, as_key = True)
        output += 'proc %s*[T](fsm: var StateMachine[T], ctx: var T) =\n' % (event.lower())
        output += ' ' * 2 + 'let idx = fsm.state * %d + %d\n' % (len(events), events.index(evt))
        if debug:
            output += ' ' * 2 + 'echo("(%s, " & state_strings[fsm.state] & ") => (" & action_strings[idx] & ", " & state_strings[fsm.state + transform_states[idx]] & ")")\n' % (preprocess(evt).upper())
        output += ' ' * 2 + 'fsm.transform_actions[idx](fsm.delegate, ctx)\n'
        output += ' ' * 2 + 'fsm.state += transform_states[idx]\n\n'
    return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings):
    import os.path
    states = [preprocess(state) for state in states]
    events = [preprocess(event) for event in events]
    actions = [preprocess(action) for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    dest = os.path.join(directory, root.replace('-', '_') + '.nim')
    with open(dest, 'w') as output:
        output.write('type\n')
        output.write(state(prefix, states))
        output.write('\n')
        output.write(action(prefix, actions))
        output.write('\n')
        if style == 'code':
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug))
