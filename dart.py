def preprocess(cell):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if cell[0].isdigit():
      cell = 'NUMBER_' + cell
    return cell

def state(prefix, states):
    output = 'enum State {\n'
    for s in states:
        output += ' ' * 2 + s + ',\n'
    output += '}\n'
    return output

def event(prefix, events):
    output = 'enum Event {\n'
    for e in events:
        output += ' ' * 2 + e + ',\n'
    output += '}\n'
    return output

def action(prefix, actions):
    output = 'abstract class StateMachineDelegate<C> {\n'
    for action in actions:
        output += ' ' * 2 + 'void %s(C ctx, State state, Event event);\n' % (action.lower())
    output += '}\n'
    return output

def code_transforming(prefix, states, events, transformings, debug):
    output = 'class StateMachine<C> {\n'
    output += ' ' * 2 + 'State state;\n'
    output += ' ' * 2 + 'StateMachineDelegate<C> delegate;\n'
    output += ' ' * 2 + 'StateMachine(StateMachineDelegate<C> delegate) {\n'
    output += ' ' * 4 + 'this.delegate = delegate;\n'
    output += ' ' * 4 + 'this.state = State.%s;\n' % states[0]
    output += ' ' * 2 + '}\n'
    output += ' ' * 2 + 'void process(C ctx, Event event) {\n'
    output += ' ' * 4 + 'switch (event) {\n'
    for ei in range(len(events)):
        output += ' ' * 6 + 'case Event.%s: {\n' % (events[ei])
        output += ' ' * 8 + 'switch (state) {\n'
        for si in range(len(states)):
            (action, state) = transformings[si][ei]
            if state:
                output += ' ' * 10 + 'case State.%s:\n' % (states[si])
                if action:
                    if debug:
                        output += " " * 12 + 'print("(%s, %s) => (%s, %s)");\n' % (events[ei], states[si], action, state)
                    output += ' ' * 12 + 'this.delegate.%s(ctx, this.state, event);\n' % (action.lower())
                else:
                    if debug:
                        output += " " * 12 + 'print("(%s, %s) => (N/A, %s)");\n' % (events[ei], states[si], state)
                if state != states[si]:
                    output += ' ' * 12 + 'this.state = State.%s;\n' % (state)
                output += ' ' * 12 + 'break;\n'
        output += ' ' * 10 + 'default:\n'
        output += ' ' * 12 + 'break;\n'
        output += ' ' * 8 + '}\n'
        output += ' ' * 8 + 'break;\n'
        output += ' ' * 6 + '}\n'
    output += ' ' * 6 + 'default:\n'
    output += ' ' * 8 + 'break;\n'
    output += ' ' * 4 + '}\n'
    output += ' ' * 2 + '}\n'
    output += '}\n'
    return output

def table_transforming(prefix, states, events, actions, transformings, debug):
    output = ''
    if debug:
        output += 'List<String> state_strings = const <String>[%s];\n' % (', '.join(['"%s"' % state for state in states]))
        output += 'List<String> event_strings = const <String>[%s];\n' % (', '.join(['"%s"' % event for event in events]))
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
        output += 'List<String> action_strings = const <String>[%s];\n' % (', '.join(actions_table))
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
    output += 'List<State> transform_states = <State>[%s];\n' % (', '.join(transforming_states_table))
    output += 'class StateMachine<C> {\n'
    output += ' ' * 2 + 'State state;\n'
    output += ' ' * 2 + 'StateMachineDelegate<C> delegate;\n'
    output += ' ' * 2 + 'List<void Function(C ctx, State state, Event event)> transform_actions;\n'
    output += ' ' * 2 + 'StateMachine(StateMachineDelegate<C> delegate) {\n'
    output += ' ' * 4 + 'this.delegate = delegate;\n'
    output += ' ' * 4 + 'this.state = State.%s;\n' % states[0]
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (action, state) = transformings[si][ei]
            if action:
                transforming_actions.append('this.delegate.' + preprocess(action).lower())
            else:
                transforming_actions.append('null')
        transforming_actions_table.append(', '.join(transforming_actions))
    output += ' ' * 4 + 'this.transform_actions = <void Function(C ctx, State state, Event event)>[%s];\n' % (', '.join(transforming_actions_table))
    output += ' ' * 2 + '}\n'
    output += ' ' * 2 + 'void process(C ctx, Event event) {\n'
    output += ' ' * 4 + 'int idx = this.state.index * %d + event.index;\n' % len(events)
    if debug:
        output += ' ' * 4 + 'print("(${event_strings[event.index]}, ${state_strings[this.state.index]}) => (${action_strings[idx]}, ${state_strings[transform_states[idx].index]})");\n'
    output += ' ' * 4 + 'if (this.transform_actions[idx] != null) {\n'
    output += ' ' * 6 + 'this.transform_actions[idx](ctx, this.state, event);\n'
    output += ' ' * 4 + '}\n'
    output += ' ' * 4 + 'this.state = transform_states[idx];\n'
    output += ' ' * 2 + '}\n'
    output += '}\n'
    return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings):
    import os.path
    states = [preprocess(state) for state in states]
    events = [preprocess(event) for event in events]
    actions = [preprocess(action) for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    dest = os.path.join(directory, root.replace("-", "_") + ".dart")
    with open(dest, 'w') as output:
        output.write(state(prefix, states))
        output.write("\n");
        output.write(event(prefix, events))
        output.write("\n");
        output.write(action(prefix, actions))
        output.write("\n");
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug))
        output.write("\n");
