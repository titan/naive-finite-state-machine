def preprocess(cell):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if cell[0].isdigit():
      cell = 'NUMBER_' + cell
    return cell

def state(prefix, states):
    output = ' ' * 2 + 'State* = enum\n'
    output += ' ' * 4 + ', '.join(states)
    return output

def event(prefix, events):
    output = ' ' * 2 + 'Event* = enum\n'
    output += ' ' * 4 + ', '.join(events)
    return output

def action(prefix, actions):
    output = ' ' * 2 + 'StateMachineDelegate*[T] = object of RootObj\n'
    for action in actions:
        output += ' ' * 4 + '%s*: proc (ctx: T, state: State, event: Event)\n' % (action.lower())
    return output

def code_transforming(prefix, states, events, transformings, debug):
    output = ' ' * 2 + 'StateMachine*[T] = object of RootObj\n'
    output += ' ' * 4 + 'state: State\n'
    output += ' ' * 4 + 'delegate: StateMachineDelegate[T]\n'
    output += 'proc initStateMachine*[T](delegate: StateMachineDelegate[T]): StateMachine[T] =\n'
    output += ' ' * 2 + 'result = StateMachine[T](state: State.%s, delegate: delegate)\n' % (states[0])
    output += 'proc process*[T](fsm: var StateMachine[T], ctx: T, event: Event) =\n'
    output += ' ' * 2 + 'case event:\n'
    for ei in range(len(events)):
        output += ' ' * 4 + 'of Event.%s:\n' % (events[ei])
        output += ' ' * 6 + 'case fsm.state:\n'
        count = 0
        for si in range(len(states)):
            (action, state) = transformings[si][ei]
            if state:
                count += 1
                output += ' ' * 8 + 'of State.%s:\n' % (states[si])
                if action:
                    if debug:
                        output += ' ' * 10 + 'echo("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], action, state)
                    output += ' ' * 10 + 'fsm.delegate.%s(ctx, fsm.state, event)\n' % (action.lower())
                else:
                    if debug:
                        output += ' ' * 10 + 'echo("(%s, %s) => (N/A, %s)");\n' % (events[ei], states[si], state)
                if state != states[si]:
                    output += ' ' * 10 + 'fsm.state = State.%s\n' % (state)
        if count != len(states):
            output += ' ' * 8 + 'else:\n'
            output += ' ' * 10 + 'discard\n'
    return output

def table_transforming(prefix, states, events, actions, transformings, debug):
    output = ' ' * 2 + 'StateMachine*[T] = object of RootObj\n'
    output += ' ' * 4 + 'state: State\n'
    output += ' ' * 4 + 'transform_actions: array[0..%d, proc (ctx: T, state: State, event: Event)]\n' % (len(states) * len(events) - 1)
    if debug:
        output += 'const state_strings: array[0..%d, string] = [%s]\n' % (len(states) - 1, ', '.join(['"%s"' % state for state in states]))
        output += 'const event_strings: array[0..%d, string] = [%s]\n' % (len(events) - 1, ', '.join(['"%s"' % event for event in events]))
        actions_table = []
        for si in range(len(states)):
            actions = []
            for ei in range(len(events)):
                (action, state) = transformings[si][ei]
                if action:
                    actions.append('"%s"' % preprocess(action))
                else:
                    actions.append('"N/A"')
            actions_table.append(', '.join(actions))
        output += 'const action_strings: array[0..%d, string] = [%s]\n' % (len(states) * len(events) - 1, ', '.join(actions_table))
    transforming_states_table = []
    for si in range(len(states)):
        transforming_states = []
        for ei in range(len(events)):
            (action, state) = transformings[si][ei]
            if state:
                transforming_states.append('State.' + preprocess(state))
            else:
                transforming_states.append('State.' + states[si])
        transforming_states_table.append(', '.join(transforming_states))
    output += 'const transform_states: array[0..%d, State] = [%s];\n' % (len(states) * len(events) - 1, ', '.join(transforming_states_table))
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (action, state) = transformings[si][ei]
            if action:
                transforming_actions.append('delegate.' + preprocess(action).lower())
            else:
                transforming_actions.append('nil')
        transforming_actions_table.append(', '.join(transforming_actions))
    output += 'proc initStateMachine*[T](delegate: StateMachineDelegate[T]): StateMachine[T] =\n'
    output += ' ' * 2 + 'let actions: array[0..%d, proc (ctx: T, state: State, event: Event)] = [%s]\n' % (len(states) * len(events) - 1, ', '.join(transforming_actions_table))
    output += ' ' * 2 + 'result = StateMachine[T](state: State.%s, transform_actions: actions)\n' % (states[0])
    output += 'proc process*[T](fsm: var StateMachine[T], ctx: T, event: Event) =\n'
    output += ' ' * 2 + 'let idx = ord(fsm.state) * %d + ord(event)\n' % len(events)
    if debug:
        output += ' ' * 2 + 'echo("(" & event_strings[ord(event)] & ", " & state_strings[ord(fsm.state)] & ") => (" & action_strings[idx] & ", " & state_strings[ord(transform_states[idx])] & ")")\n'
    output += ' ' * 2 + 'if fsm.transform_actions[idx] != nil:\n'
    output += ' ' * 4 + 'fsm.transform_actions[idx](ctx, fsm.state, event)\n'
    output += ' ' * 2 + 'fsm.state = transform_states[idx]\n'
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
        output.write(event(prefix, events))
        output.write('\n')
        output.write(action(prefix, actions))
        output.write('\n')
        if style == 'code':
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug))
        output.write('\n')
