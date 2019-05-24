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
    output = ' ' * 2 + 'StateMachineDelegate*[T] = ref object of RootObj\n'
    for action in actions:
        output += ' ' * 4 + '%s*: proc (ctx: T): T\n' % (action.lower())
    output += '\n'
    output += ' ' * 2 + 'AsyncStateMachineDelegate*[T] = ref object of RootObj\n'
    for action in actions:
        output += ' ' * 4 + '%s*: proc (ctx: T): Future[T]\n' % (action.lower())
    return output

def code_state_machine(states, events, asynced):
    if asynced:
        asyncprefix = "Async"
    else:
        asyncprefix = ""
    output = ' ' * 2 + '{asyncprefix}StateMachine*[T] = ref object of RootObj\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 4 + 'state*: int\n'
    output += ' ' * 4 + 'delegate*: {asyncprefix}StateMachineDelegate[T]\n\n'.format(asyncprefix = asyncprefix)
    return output

def table_state_machine(states, events, asynced):
    if asynced:
        asyncprefix = "Async"
        asyncreturn = ": Future[T]"
    else:
        asyncprefix = ""
        asyncreturn = ": T"
    output = ' ' * 2 + '{asyncprefix}StateMachine*[T] = ref object of RootObj\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 4 + 'state*: int\n'
    output += ' ' * 4 + 'delegate*: {asyncprefix}StateMachineDelegate[T]\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 4 + 'transform_actions: array[0..{len}, proc (delegate: {asyncprefix}StateMachineDelegate[T], ctx: T){asyncreturn}]\n\n'.format(asyncprefix = asyncprefix, len = ((len(states) + 1)* len(events) - 1), asyncreturn = asyncreturn)
    return output

def transforming_states(states, events, transformings):
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
    return 'const transform_states: array[0..%d, int] = [%s];\n\n' % ((len(states) + 1) * len(events) - 1, ', '.join(transforming_states_table))

def table_debug_string(states, events, transformings, debug):
    output = ""
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
    return output

def async_action_generator(indent, fun, actions):
    output = ' ' * indent + 'var retfut = newFuture[T]("{0}")\n'.format(fun)
    output += ' ' * indent + 'iterator {0}_iter(): FutureBase {{.closure.}} =\n'.format(fun)
    idx = 1
    for action in actions:
        output += ' ' * (indent + 2) + 'var ctx{idx}fut = delegate.{action}(ctx{previdx})\n'.format(action = action, idx = idx, previdx = idx - 1)
        output += ' ' * (indent + 2) + 'yield ctx{idx}fut\n'.format(idx = idx)
        output += ' ' * (indent + 2) + 'let ctx{idx} = ctx{idx}fut.read\n'.format(idx = idx)
        idx += 1
    output += ' ' * (indent + 2) + 'complete(retfut, ctx{previdx})\n'.format(previdx = idx - 1)
    output += ' ' * indent + 'var name_iter = {0}_iter\n'.format(fun)
    output += ' ' * indent + 'proc {0}_continue() {{.closure.}} =\n'.format(fun)
    output += ' ' * (indent + 2) + 'try:\n'
    output += ' ' * (indent + 4) + 'if not name_iter.finished:\n'
    output += ' ' * (indent + 6) + 'var next = name_iter()\n'
    output += ' ' * (indent + 6) + 'while (not next.isNil) and next.finished:\n'
    output += ' ' * (indent + 8) + 'next = name_iter()\n'
    output += ' ' * (indent + 8) + 'if name_iter.finished:\n'
    output += ' ' * (indent + 10) + 'break\n'
    output += ' ' * (indent + 6) + 'if next == nil:\n'
    output += ' ' * (indent + 8) + 'if not retfut.finished:\n'
    output += ' ' * (indent + 10) + 'let msg = "Async procedure ($1) yield `nil`, are you wait\'ing a " & "`nil` Future?"\n'
    output += ' ' * (indent + 10) + 'raise newException(AssertionError, msg % "{0}")\n'.format(fun)
    output += ' ' * (indent + 6) + 'else:\n'
    output += ' ' * (indent + 8) + '{.gcsafe.}:\n'
    output += ' ' * (indent + 10) + '{.push, hint[ConvFromXtoItselfNotNeeded]: off.}\n'
    output += ' ' * (indent + 10) + 'next.callback = (proc () {{.closure, gcsafe.}})({0}_continue)\n'.format(fun)
    output += ' ' * (indent + 10) + '{.pop.}\n'
    output += ' ' * (indent + 2) + 'except:\n'
    output += ' ' * (indent + 4) + 'if retfut.finished:\n'
    output += ' ' * (indent + 6) + 'raise\n'
    output += ' ' * (indent + 4) + 'else:\n'
    output += ' ' * (indent + 6) + 'retfut.fail(getCurrentException())\n'
    output += ' ' * indent + '{0}_continue()\n'.format(fun)
    output += ' ' * indent + 'result = retfut\n'
    return output

def code_transforming(prefix, states, events, transformings, debug, asynced):
    if asynced:
        asyncprefix = "Async"
        asyncpragma = ""
        awaitprefix = "await "
        asyncreturn = ": Future[T]"
    else:
        asyncprefix = ""
        asyncpragma = ""
        awaitprefix = ""
        asyncreturn = ": T"
    output = ''
    output += 'proc new{asyncprefix}StateMachine*[T](state: int, delegate: {asyncprefix}StateMachineDelegate[T]): {asyncprefix}StateMachine[T] =\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result = new({asyncprefix}StateMachine[T])\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result.state = state\n'
    output += ' ' * 2 + 'result.delegate = delegate\n\n'
    output += 'proc new{asyncprefix}StateMachine*[T](delegate: {asyncprefix}StateMachineDelegate[T]): {asyncprefix}StateMachine[T] =\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result = new({asyncprefix}StateMachine[T])\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result.state = ord(State.{state})\n'.format(state = states[0])
    output += ' ' * 2 + 'result.delegate = delegate\n\n'
    for ei in range(len(events)):
        output += 'proc {event}*[T](fsm: var {asyncprefix}StateMachine[T], ctx0: T){asyncreturn} {asyncpragma}=\n'.format(event = preprocess(events[ei], as_key = True).lower(), asyncprefix = asyncprefix, asyncreturn = asyncreturn, asyncpragma = asyncpragma)
        output += ' ' * 2 + 'let delegate = fsm.delegate\n'
        output += ' ' * 2 + 'let state = State(fsm.state)\n'
        output += ' ' * 2 + 'case state:\n'
        count = 0
        for si in range(len(states)):
            (actions, state) = transformings[si][ei]
            if state:
                count += 1
                output += ' ' * 4 + 'of State.%s:\n' % (states[si])
                if len(actions) > 0:
                    if debug:
                        output += ' ' * 6 + 'echo("(%s, %s) => (%s, %s)")\n' % (events[ei], states[si], ' |> '.join([preprocess(x).upper() for x in actions]), state)
                    if not asynced:
                        idx = 0
                        for action in actions:
                            if idx == len(actions) - 1:
                                output += ' ' * 6 + 'result = delegate.{action}(ctx{idx})\n'.format(action = action.lower(), idx = idx)
                            else:
                                output += ' ' * 6 + 'let ctx{nextidx} = delegate.{action}(ctx{idx})\n'.format(action = action.lower(), idx = idx, nextidx = idx + 1)
                            idx += 1
                    else:
                        output += async_action_generator(6, preprocess(events[ei], as_key = True).lower(), actions)
                else:
                    if debug:
                        output += ' ' * 6 + 'echo("(%s, %s) => (N/A, %s)");\n' % (events[ei], states[si], preprocess(state))
                    if asynced:
                        output += ' ' * 6 + 'result = newFuture[T]("{0}")\n'.format(preprocess(events[ei], as_key = True).lower())
                        output += ' ' * 6 + 'result.complete(ctx0)\n'
                    else:
                        output += ' ' * 6 + 'result = ctx0\n'
                if state != states[si]:
                    output += ' ' * 6 + 'fsm.state = ord(State.%s)\n' % (preprocess(state))
            elif len(actions) > 0:
                count += 1
                output += ' ' * 4 + 'of State.%s:\n' % (states[si])
                if debug:
                    output += ' ' * 6 + 'echo("(%s, %s) => (%s, N/A)")\n' % (events[ei], states[si], ' |> '.join([preprocess(x).upper() for x in actions]))
                if not asynced:
                    idx = 0
                    for action in actions:
                        if idx == len(actions) - 1:
                            output += ' ' * 6 + 'result = delegate.{action}(ctx{idx})\n'.format(action = action.lower(), idx = idx)
                        else:
                            output += ' ' * 6 + 'let ctx{nextidx} = delegate.{action}(ctx{idx})\n'.format(action = action.lower(), idx = idx, nextidx = idx + 1)
                        idx += 1
                else:
                    output += async_action_generator(6, preprocess(events[ei], as_key = True).lower(), actions)
            else:
                pass
        if count != len(states):
            output += ' ' * 4 + 'else:\n'
            if asynced:
                output += ' ' * 6 + 'result = newFuture[T]("{0}")\n'.format(preprocess(events[ei], as_key = True).lower())
                output += ' ' * 6 + 'result.complete(ctx0)\n'
            else:
                output += ' ' * 6 + 'result = ctx0\n'
        output += '\n'
    return output

def table_transforming(prefix, states, events, actions, transformings, debug, asynced):
    if asynced:
        asyncprefix = "Async"
        asyncpragma = "{.async.}"
        awaitprefix = "await "
        innerpragma = ", async"
        asyncreturn = ": Future[T]"
        nosideffect = ""
    else:
        asyncprefix = ""
        asyncpragma = ""
        awaitprefix = ""
        innerpragma = ""
        asyncreturn = ": T"
        nosideffect = ", noSideEffect"
    output = ''
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
    output += 'proc new{asyncprefix}StateMachine*[T](state: int, delegate: {asyncprefix}StateMachineDelegate[T]): {asyncprefix}StateMachine[T] =\n\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'proc noop[T](delegate: {asyncprefix}StateMachineDelegate[T], ctx: T){asyncreturn} {{.closure{innerpragma}.}} =\n'.format(asyncprefix = asyncprefix, innerpragma = innerpragma, asyncreturn = asyncreturn)
    output += ' ' * 4 + 'result = ctx\n\n'
    for (actionid, actions) in inner_actions.values():
        output += ' ' * 2 + 'proc action_{actionid}[T](delegate: {asyncprefix}StateMachineDelegate[T], ctx0: T){asyncreturn} {{.closure{nosideffect}, gcsafe, locks: 0.}} =\n'.format(actionid = actionid, asyncprefix = asyncprefix, asyncreturn = asyncreturn, innerpragma = innerpragma, nosideffect = nosideffect)
        if not asynced:
            idx = 0
            for action in actions:
                if idx == len(actions) - 1:
                    output += ' ' * 4 + 'result = delegate.{action}(ctx{idx})\n'.format(action = action, idx = idx)
                else:
                    output += ' ' * 4 + 'let ctx{nextidx} = {awaitprefix}delegate.{action}(ctx{idx})\n'.format(action = action, awaitprefix = awaitprefix, idx = idx, nextidx = idx + 1)
                idx += 1
            output += '\n'
        else:
            output += async_action_generator(4, "action_{0}".format(actionid), actions)
            output += '\n'
    output += ' ' * 2 + 'let actions: array[0..{len}, proc (delegate: {asyncprefix}StateMachineDelegate[T], ctx: T){asyncreturn}] = [{actions}]\n'.format(len = (len(states) + 1) * len(events) - 1, actions = ', '.join(['%s' % ', '.join(['noop[T]'] * len(events))] + ['%s' % ', '.join(['noop[T]' if y is None else 'action_%d[T]' % y for y in x]) for x in transforming_actions_table]), asyncprefix = asyncprefix, asyncreturn = asyncreturn)
    output += ' ' * 2 + 'result = new({asyncprefix}StateMachine[T])\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result.state = state\n'
    output += ' ' * 2 + 'result.delegate = delegate\n'
    output += ' ' * 2 + 'result.transform_actions = actions\n\n'
    output += 'proc new{asyncprefix}StateMachine*[T](delegate: {asyncprefix}StateMachineDelegate[T]): {asyncprefix}StateMachine[T] =\n'.format(asyncprefix = asyncprefix)
    output += ' ' * 2 + 'result = new{asyncprefix}StateMachine[T](ord(State.{state}), delegate)\n\n'.format(asyncprefix = asyncprefix, state = states[0])
    for evt in events:
        event = preprocess(evt, as_key = True)
        output += 'proc {event}*[T](fsm: var {asyncprefix}StateMachine[T], ctx: T){asyncreturn} =\n'.format(event = event.lower(), asyncprefix = asyncprefix, asyncreturn = asyncreturn)
        output += ' ' * 2 + 'let idx = fsm.state * %d + %d\n' % (len(events), events.index(evt))
        if debug:
            output += ' ' * 2 + 'echo("(%s, " & state_strings[fsm.state] & ") => (" & action_strings[idx] & ", " & state_strings[fsm.state + transform_states[idx]] & ")")\n' % (preprocess(evt).upper())
        output += ' ' * 2 + 'result = fsm.transform_actions[idx](fsm.delegate, ctx)\n'.format(awaitprefix = awaitprefix)
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
        output.write('import asyncdispatch\n')
        output.write('type\n')
        output.write(state(prefix, states))
        output.write('\n')
        output.write(action(prefix, actions))
        output.write('\n')
        if style == 'code':
            output.write(code_state_machine(states, events, False))
            output.write(code_state_machine(states, events, True))
            output.write(code_transforming(prefix, states, events, transformings, debug, False))
            output.write(code_transforming(prefix, states, events, transformings, debug, True))
        else:
            output.write(table_state_machine(states, events, False))
            output.write(table_state_machine(states, events, True))
            output.write(transforming_states(states, events, transformings))
            if debug:
                output.write(table_debug_string(states, events, transformings, debug))
            output.write(table_transforming(prefix, states, events, actions, transformings, debug, False))
            output.write(table_transforming(prefix, states, events, actions, transformings, debug, True))
