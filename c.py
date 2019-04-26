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
    i = 1
    output = "enum %s_STATE_MACHINE_STATE {\n" % prefix.upper()
    for s in states:
        output += " " * 2 + '{prefix}_STATE_MACHINE_STATE_{state} = {index},\n'.format(prefix = prefix.upper(), state = preprocess(s).upper(), index = i)
        i += 1
    output += "};\n"
    return output

def event_fun_declare(prefix, events):
    return '\n'.join(['void {0}_state_machine_event_{1}(struct {0}_state_machine * fsm);'.format(prefix, evt.lower()) for evt in events]) + '\n'

def code_transforming(prefix, states, events, transformings, debug):
    output = ''
    output += 'void {prefix}_state_machine_init(struct {prefix}_state_machine * fsm, struct {prefix}_state_machine_context * ctx) {{\n'.format(prefix = prefix)
    output += ' ' * 2 + 'fsm->ctx = ctx;\n'
    output += ' ' * 2 + 'fsm->state = {0}_STATE_MACHINE_STATE_{1};\n'.format(prefix.upper(), states[0].upper())
    output += '}\n\n'
    for ei in range(len(events)):
        event = preprocess(events[ei]).lower()
        output += 'void {prefix}_state_machine_event_{event}(struct {prefix}_state_machine * fsm) {{\n'.format(prefix = prefix, event = event)
        output += ' ' * 2 + 'switch (fsm->state) {\n'
        count = 0
        for si in range(len(states)):
            (actions, state) = transformings[si][ei]
            if state:
                count += 1
                state = preprocess(state)
                output += ' ' * 4 + 'case {0}_STATE_MACHINE_STATE_{1}:\n'.format(prefix.upper(), preprocess(states[si]).upper())
                if len(actions) > 0:
                    if debug:
                        output += ' ' * 6 + 'printf("(%s, %s) => (%s, %s)\\n");\n' % (preprocess(events[ei]), preprocess(states[si]), ' |> '.join([x.upper() for x in actions]), preprocess(state))
                    for action in actions:
                        output += ' ' * 6 + '{0}_state_machine_action_{1}(fsm->ctx);\n'.format(prefix, preprocess(action).lower())
                else:
                    if debug:
                        output += ' ' * 6 + 'printf("(%s, %s) => (N/A, %s)\\n");\n' % (preprocess(events[ei]), preprocess(states[si]), preprocess(state))
                if state != states[si]:
                    output += ' ' * 6 + 'fsm->state = {0}_STATE_MACHINE_STATE_{1};\n'.format(prefix.upper(), preprocess(state).upper())
                output += ' ' * 6 + 'break;\n'
            elif len(actions) > 0:
                count += 1
                output += ' ' * 4 + 'case {0}_STATE_MACHINE_STATE_{1}:\n'.format(prefix.upper(), preprocess(states[si]).upper())
                if debug:
                    output += ' ' * 6 + 'printf("(%s, %s) => (%s, N/A)\\n");\n' % (preprocess(events[ei]), preprocess(states[si]), ' |> '.join([x.upper() for x in actions]))
                for action in actions:
                    output += ' ' * 6 + '{0}_state_machine_action_{1}(fsm->ctx);\n'.format(prefix, preprocess(action).lower())
            else:
                pass
        if count != len(states):
            output += ' ' * 4 + 'default: break;\n'
        output += ' ' * 2 + '}\n'
        output += '}\n\n'
    return output

def table_transforming(prefix, states, events, transformings, debug):

    # calculate state type
    if len(states) > 256 and len(states) <= 65536:
        state_type = 'short'
    elif len(states) > 65535:
        state_type = 'int'
    else:
        state_type = 'char'

    output = ""

    if debug:
        output += "static char * %s_state_strings[%d] = {\n%s\n};\n\n" % (prefix, len(states) + 1, ',\n'.join(['  ""'] + ['  "%s"' % s for s in states]))

        actions_table = ['  { %s }' % ', '.join(['"N/A"'] * len(events))]
        for si in range(len(states)):
            actions = []
            for ei in range(len(events)):
                (_actions, state) = transformings[si][ei]
                if len(_actions) > 0:
                    actions.append('"{0}"'.format(' |> '.join([str(x).upper() for x in _actions])))
                else:
                    actions.append('"N/A"')
            actions_table.append('  { %s }' % (', '.join(actions)))
        output += "static char * %s_action_strings[%d][%d] = {\n%s\n};\n\n" % (prefix, len(states) + 1, len(events), ',\n'.join(actions_table))

    transforming_states_table = ['  { %s }' % ', '.join(['0'] * len(events))]
    for si in range(len(states)):
        transforming_states = []
        for ei in range(len(events)):
            (_, state) = transformings[si][ei]
            if state:
                transforming_states.append(states.index(state) - si)
            else:
                transforming_states.append(0)
        transforming_states_table.append('  { %s }' % ', '.join(['%d' % x for x in transforming_states]))

    output += "static " + state_type + " %s_transform_states[%d][%d] = {\n%s\n};\n\n" % (prefix, len(states) + 1, len(events), ',\n'.join(transforming_states_table))

    actionid = 1
    inner_actions = {}
    transforming_actions_table = []
    for si in range(len(states)):
        transforming_actions = []
        for ei in range(len(events)):
            (actions, state) = transformings[si][ei]
            if len(actions) == 1:
                transforming_actions.append(preprocess(str(actions[0])).lower())
            elif len(actions) > 0:
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

    output += 'static void {0}_state_machine_inner_action_noop(struct {0}_state_machine_context * ctx) {{\n  (void)ctx;\n}}\n\n'.format(prefix)
    for (aid, actions) in inner_actions.values():
        output += 'static void {0}_state_machine_inner_action_{1}(struct {0}_state_machine_context * ctx) {{\n'.format(prefix, aid)
        for action in actions:
            output += ' ' * 2 + '{0}_state_machine_action_{1}(ctx);\n'.format(prefix, action)
        output += '}\n\n'

    output += 'static {0}_state_machine_action_fn {0}_transform_actions[{1}][{2}] = {{\n{3}\n}};\n\n'.format(prefix, len(states) + 1, len(events), ',\n'.join(['  {{ {0} }}'.format(', '.join(['{0}_state_machine_inner_action_noop'.format(prefix) if y is None else ('{0}_state_machine_action_{1}'.format(prefix, y) if isinstance(y, str) else '{0}_state_machine_inner_action_{1}'.format(prefix, y)) for y in x])) for x in ([[None] * len(events)] + transforming_actions_table)]))


    output += "void {prefix}_state_machine_init(struct {prefix}_state_machine * fsm, struct {prefix}_state_machine_context * ctx) {{\n".format(prefix=prefix)
    output += ' ' * 2 + 'fsm->ctx = ctx;\n'
    output += ' ' * 2 + 'fsm->state = {prefix}_STATE_MACHINE_STATE_{state};\n'.format(prefix = prefix.upper(), state = preprocess(states[0]).upper())
    output += "}\n\n"
    for evt in events:
        ei = events.index(evt)
        event = preprocess(evt).lower()
        output += "void {prefix}_state_machine_event_{event}(struct {prefix}_state_machine * fsm) {{\n".format(prefix=prefix, event = event)
        if debug:
            output += ' ' * 2 + 'printf("(%s, ");\n' % (event.upper())
            output += ' ' * 2 + 'printf(%s_state_strings[fsm->state]);\n' % prefix
            output += ' ' * 2 + 'printf(") => (");\n'
            output += ' ' * 2 + 'printf(%s_action_strings[fsm->state][%d]);\n' % (prefix, ei)
            output += ' ' * 2 + 'printf(", ");\n'
            output += ' ' * 2 + 'printf({prefix}_state_strings[fsm->state + {prefix}_transform_states[fsm->state][{ei}]]);\n'.format(prefix = prefix, ei = ei)
            output += ' ' * 2 + 'printf(")\\n");\n'
        output += ' ' * 2 + '{prefix}_transform_actions[fsm->state][{ei}](fsm->ctx);\n'.format(prefix = prefix, ei = ei)
        output += ' ' * 2 + "fsm->state += {prefix}_transform_states[fsm->state][{ei}];\n".format(prefix = prefix, ei = ei)
        output += "}\n\n"
    return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings):
    import os.path
    prefix = prefix.lower()
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    header = root + ".h"
    defination = os.path.join(directory, header)
    implementation = os.path.join(directory, root + ".c")
    action_header = root + '-actions.h'
    action_defination = os.path.join(directory, action_header)
    with open(action_defination, 'w') as output:
        output.write('#ifndef __%s\n' % (action_header.replace('-', '_').replace('.', '_').upper()))
        output.write('#define __%s\n' % (action_header.replace('-', '_').replace('.', '_').upper()))
        output.write("struct %s_state_machine_context;\n" % (prefix))
        for action in actions:
            output.write('void {prefix}_state_machine_action_{action}(struct {prefix}_state_machine_context * ctx);\n'.format(prefix=prefix, action=preprocess(action).lower()))
        output.write("#endif\n")
    with open(defination, 'w') as output:
        output.write('#ifndef __%s\n' % (header.replace('-', '_').replace('.', '_').upper()))
        output.write('#define __%s\n' % (header.replace('-', '_').replace('.', '_').upper()))
        output.write(state(prefix, states))
        output.write("\n")
        output.write("struct %s_state_machine_context;\n" % (prefix))
        output.write("struct %s_state_machine {\n" % (prefix))
        output.write(' ' * 2 + "enum %s_STATE_MACHINE_STATE state;\n" % (prefix.upper()))
        output.write(' ' * 2 + "struct %s_state_machine_context * ctx;\n" % (prefix))
        output.write("};\n")
        output.write("typedef void (* {0}_state_machine_action_fn)(struct {0}_state_machine_context * ctx);\n".format(prefix))
        output.write("void {prefix}_state_machine_init(struct {prefix}_state_machine * fsm, struct {prefix}_state_machine_context * ctx);\n".format(prefix = prefix))
        output.write(event_fun_declare(prefix, events))
        output.write("#endif\n")
    with open(implementation, 'w') as output:
        if debug:
            output.write('#include <stdio.h>\n')
        output.write('#include <stdlib.h>\n')
        output.write('#include "%s"\n' % header)
        output.write('#include "%s"\n' % action_header)
        output.write('\n')
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, transformings, debug))
