def preprocess(cell):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if cell[0].isdigit():
      cell = "NUMBER_" + cell
    return cell

def state(prefix, states):
    i = 0
    output = "class State:\n"
    for s in states:
        output += " " * 4 + s + " = %d\n" % i
        i += 1
    return output

def event(prefix, events):
    i = 0
    output = "class Event:\n"
    for e in events:
        output += " " * 4 + e + " = %d\n" % i
        i += 1
    return output

def action(prefix, actions):
    i = 1
    output = "class Action:\n"
    for a in actions:
        output += " " * 4 + a + " = %d\n" % i
        i += 1
    return output

def code_transforming(prefix, states, events, transformings, debug, function):
    output = "class StateMachine:\n"
    if not function:
        output += " " * 4 + "def __init__(self, delegate):\n"
        output += " " * 8 + "self.delegate = delegate\n"
        output += " " * 8 + "self.state = State.%s\n" % states[0]
        output += " " * 4 + "def process(self, event, data = None):\n"
    else:
        actions = {}
        for si in range(len(states)):
            for ei in range(len(events)):
                (action, state) = transformings[si][ei]
                if action:
                    realaction = preprocess(action).lower()
                    actions[realaction] = 1
        for action in actions.keys():
            output += " " * 4 + "def %s(self, ctx, state = 0, event = 0):\n" % (action)
            output += " " * 8 + "pass\n"
        output += " " * 4 + "def __init__(self, delegate):\n"
        for action in actions.keys():
            output += " " * 8 + "self.%s = delegate.%s\n" % (action, action)
        output += " " * 8 + "self.state = State.%s\n" % states[0]
        output += " " * 4 + "def process(self, ctx, event):\n"
    first_event = True
    ei = 0
    for e in events:
        if first_event:
            first_event = False
            output += " " * 8 + "if event == Event.%s:\n" % e
        else:
            output += " " * 8 + "elif event == Event.%s:\n" % e
        first_state = True
        si = 0
        stmt = 0
        for s in states:
            (action, state) = transformings[si][ei]
            if state:
                stmt += 1
                state = preprocess(state)
                if first_state:
                    first_state = False
                    output += " " * 12 + "if self.state == State.%s:\n" % preprocess(s)
                else:
                    output += " " * 12 + "elif self.state == State.%s:\n" % preprocess(s)
                if action:
                    action = preprocess(action)
                    if debug:
                        output += " " * 16 + 'print("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], action, state)
                    if function:
                        output += " " * 16 + "self.%s(ctx, self.state, event)\n" % action.lower()
                    else:
                        output += " " * 16 + "if self.delegate:\n"
                        output += " " * 20 + "self.delegate(Action.%s, data)\n" % action
                else:
                    if debug:
                        output += " " * 16 + 'print("(%s, %s) => (N/A, %s)")\n' % (events[ei], states[si], state)
                output += " " * 16 + "self.state = State.%s\n" % state
            si += 1
        if stmt == 0:
            output += " " * 12 + "pass\n"
        ei += 1
    return output

def table_transforming(prefix, states, events, actions, transformings, debug, function):
    output = "class StateMachine:\n"
    if not function:
        output += " " * 4 + "def __init__(self, delegate):\n"
        output += " " * 8 + "self.delegate = delegate\n"
    else:
        actions = {}
        for si in range(len(states)):
            for ei in range(len(events)):
                (action, state) = transformings[si][ei]
                if action:
                    realaction = preprocess(action).lower()
                    actions[realaction] = 1
        for action in actions.keys():
            output += " " * 4 + "def %s(self, ctx, state = 0, event = 0):\n" % (action)
            output += " " * 8 + "pass\n"
        output += " " * 4 + "def __init__(self, delegate):\n"
        for action in actions.keys():
            output += " " * 8 + "self.%s = delegate.%s\n" % (action, action)
    if debug:
        output += " " * 8 + "self.state_strings = [%s]\n" % (", ".join(["\"%s\"" % state for state in states]))
        output += " " * 8 + "self.event_strings = [%s]\n" % (", ".join(["\"%s\"" % event for event in events]))
        if not function:
            output += " " * 8 + "self.action_strings = [\"N/A\", %s]\n" % (", ".join(["\"%s\"" % action for action in actions]))
        else:
            actions_table = []
            for si in range(len(states)):
                actions = []
                for ei in range(len(events)):
                    (action, state) = transformings[si][ei]
                    if action:
                        actions.append('"%s"' % preprocess(action))
                    else:
                        actions.append('"N/A"')
                actions_table.append("[%s]" % ", ".join(actions))
            output += " " * 8 + "self.action_strings = [%s]\n" % (", ".join(actions_table))
    transforming_states_table = []
    for si in range(len(states)):
        transforming_states = []
        for ei in range(len(events)):
            (action, state) = transformings[si][ei]
            if state:
                transforming_states.append("State." + preprocess(state))
            else:
                transforming_states.append("State." + states[si])
        transforming_states_table.append("[%s]" % ", ".join(transforming_states))
    output += " " * 8 + "self.transform_states = [%s]\n" % (", ".join(transforming_states_table))
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (action, state) = transformings[si][ei]
            if function:
                if action:
                    transforming_actions.append("self." + preprocess(action).lower())
                else:
                    transforming_actions.append("None")
            else:
                if action:
                    transforming_actions.append("Action." + preprocess(action))
                else:
                    transforming_actions.append("0")
        transforming_actions_table.append("[%s]" % ", ".join(transforming_actions))
    output += " " * 8 + "self.transform_actions = [%s]\n" % (", ".join(transforming_actions_table))
    output += " " * 8 + "self.state = State.%s\n" % states[0]
    if not function:
        output += " " * 4 + "def process(self, event, data):\n"
        if debug:
            output += " " * 8 + 'print("(%s, %s) => (%s, %s)" % (self.event_strings[event], self.state_strings[self.state], self.action_strings[self.transform_states[self.state][event]], self.state_strings[self.transform_states[self.state][event]]))\n';
        output += " " * 8 + "if self.delegate:\n"
        output += " " * 12 + "self.delegate(self.transform_actions[self.state][event], data)\n"
    else:
        output += " " * 4 + "def process(self, ctx, event):\n"
        if debug:
            output += " " * 8 + 'print("(%s, %s) => (%s, %s)" % (self.event_strings[event], self.state_strings[self.state], self.action_strings[self.state][event], self.state_strings[self.transform_states[self.state][event]]))\n';
        output += " " * 8 + "if self.transform_actions[self.state][event]:\n"
        output += " " * 12 + "self.transform_actions[self.state][event](ctx, self.state, event)\n"
    output += " " * 8 + "self.state = self.transform_states[self.state][event]\n"
    return output

def process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings, function):
    import os.path
    states = [preprocess(state) for state in states]
    events = [preprocess(event) for event in events]
    actions = [preprocess(action) for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    dest = os.path.join(directory, root.replace("-", "_") + ".py")
    with open(dest, 'w') as output:
        output.write(state(prefix, states))
        output.write("\n");
        output.write(event(prefix, events))
        output.write("\n");
        if not function:
            output.write(action(prefix, actions))
            output.write("\n");
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug, function))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug, function))
        output.write("\n");
