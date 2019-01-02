def preprocess(prefix, cell, postfix = None):
    if postfix:
        return ("%s_%s_%s" % (prefix, cell, postfix)).replace('__', '_')
    else:
        return ("%s_%s" % (prefix, cell)).replace('__', '_')

def state(prefix, states):
    i = 0
    output = "enum %s_STATE {\n" % prefix.upper()
    for s in states:
        output += " " * 2 + s + " = %d,\n" % i
        i += 1
    output += "};\n"
    return output

def event(prefix, events):
    i = 0
    output = "enum %s_EVENT {\n" % prefix.upper()
    for e in events:
        output += " " * 2 + e + " = %d,\n" % i
        i += 1
    output += "};\n"
    return output

def action(prefix, actions):
    i = 1
    output = "enum %s_ACTION {\n" % prefix.upper()
    for a in actions:
        output += " " * 2 + a + " = %d,\n" % i
        i += 1
    output += "};\n"
    return output

def code_transforming(prefix, states, events, transformings, debug, function):
    if not function:
        output = "enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data) {\n" % (prefix, prefix.lower(), prefix, prefix)
        output += ' ' * 2 + 'switch (event) {\n'
        for i in range(len(events)):
            output += ' ' * 2 + 'case ' + events[i] + ': {\n'
            output += ' ' * 4 + 'switch (state) {\n'
            for j in range(len(states)):
                (action, state) = transformings[j][i]
                if state:
                    state = preprocess(prefix, state, "STATE")
                    if action:
                        action = preprocess(prefix, action, "ACTION")
                        output += ' ' * 4 + 'case ' + states[j] + ': {\n'
                        if debug:
                            output += ' ' * 6 + 'printf("(%s, %s) => (%s, %s)\\n");\n' % (events[i], states[j], action, state)
                        output += ' ' * 6 + '%s_do_action(%s, data);\n' % (prefix.lower(), action)
                        output += ' ' * 6 + 'return %s;\n' % state
                        output += ' ' * 4 + '}\n'
                    else:
                        if debug:
                            output += ' ' * 4 + 'case %s: {\n' % states[j]
                            output += ' ' * 6 + 'printf("(%s, %s) => (N/A, %s)\\n");\n' % (events[i], states[j], state)
                            output += ' ' * 6 + 'return %s;\n' % state
                            output += ' ' * 4 + '}\n'
                        else:
                            output += ' ' * 4 + 'case %s: return %s;\n' % (states[j], state)
            output += ' ' * 4 + 'default: return state;\n'
            output += ' ' * 4 + '}\n'
            output += ' ' * 4 + 'break;\n'
            output += ' ' * 2 + '}\n'
        output += ' ' * 2 + 'default: return state;\n'
        output += ' ' * 2 + '}\n'
        output += "}\n"
    else:
        output = ''
        actions = {}
        for si in range(len(states)):
            for ei in range(len(events)):
                (action, state) = transformings[si][ei]
                if action:
                    actions[action.lower()] = 1
        for action in actions.keys():
            output += 'extern void %s(struct %s_context * ctx, enum %s_STATE state, enum %s_EVENT event);\n' % (preprocess(prefix, action).lower(), prefix.lower(), prefix, prefix)
        output += 'void %s_init_state_machine(struct %s_state_machine * fsm, struct %s_context * ctx) {\n' % (prefix.lower(), prefix.lower(), prefix.lower())
        output += ' ' * 2 + 'fsm->ctx = ctx;\n'
        output += ' ' * 2 + 'fsm->state = %s;\n' % (states[0])
        output += '}\n'
        output += 'void %s_process(struct %s_state_machine * fsm, enum %s_EVENT event) {\n' % (prefix.lower(), prefix.lower(), prefix)
        output += ' ' * 2 + 'switch (event) {\n'
        for ei in range(len(events)):
            output += ' ' * 4 + 'case ' + events[ei] + ': {\n'
            output += ' ' * 6 + 'switch (fsm->state) {\n'
            for si in range(len(states)):
                (action, state) = transformings[si][ei]
                if state:
                    state = preprocess(prefix, state, 'STATE')
                    output += ' ' * 8 + 'case ' + states[si] + ':\n'
                    if action:
                        if debug:
                            output += ' ' * 10 + 'printf("(%s, %s) => (%s, %s)\\n");\n' % (events[ei], states[si], action, state)
                        output += ' ' * 10 + '%s(fsm->ctx, fsm->state, event);\n' % (preprocess(prefix, action).lower())
                    else:
                        if debug:
                            output += ' ' * 10 + 'printf("(%s, %s) => (N/A, %s)\\n");\n' % (events[ei], states[si], state)
                    if state != states[si]:
                        output += ' ' * 10 + 'fsm->state = %s;\n' % (state)
                    output += ' ' * 10 + 'break;\n'
            output += ' ' * 8 + 'default: break;\n'
            output += ' ' * 6 + '}\n'
            output += ' ' * 4 + '}\n'
        output += ' ' * 4 + 'default: break;\n'
        output += ' ' * 2 + '}\n'
        output += '}\n'
    return output

def table_transforming(prefix, states, events, actions, transformings, debug, function):
    # calculate action type
    if len(actions) > 256 and len(actions) <= 65536:
        action_type = 'unsigned short'
    elif len(actions) > 65536:
        action_type = 'unsigned int'
    else:
        action_type = 'unsigned char'

    # calculate state type
    if len(states) > 256 and len(states) <= 65536:
        state_type = 'unsigned short'
    elif len(actions) > 65535:
        state_type = 'unsigned int'
    else:
        state_type = 'unsigned char'

    output = ""

    if debug:

        output += "static char * %s_state_strings[%d] = {\n" % (prefix.lower(), len(states))
        for s in states:
            output += ' ' * 2 + '"%s",\n' % s
        output += "};\n"

        output += "static char * %s_event_strings[%d] = {\n" % (prefix.lower(), len(events))
        for e in events:
            output += ' ' * 2 + '"%s",\n' % e
        output += "};\n"

        if not function:
            output += "static char * %s_action_strings[%d] = {\n" % (prefix.lower(), len(actions) + 1)
            output += ' ' * 2 + '"N/A",\n'
            for a in actions:
                output += ' ' * 2 + '"%s",\n' % a
            output += "};\n"
        else:
            output += "static char * %s_action_strings[%d][%d] = {\n" % (prefix.lower(), len(states), len(events))
            for si in range(len(states)):
                output += ' ' * 2 + '{'
                for ei in range(len(events)):
                    (action, state) = transformings[si][ei]
                    if action:
                        output += ' "' + str(action) + '",'
                    else:
                        output += ' "N/A",'
                output = output[0:-1]
                output += ' },\n'
            output += "};\n"

    output += "static " + state_type + " %s_transform_states[%d][%d] = {\n" % (prefix.lower(), len(states), len(events))
    for i in range(len(states)):
        output += ' ' * 2 + '{'
        for j in range(len(events)):
            (action, state) = transformings[i][j]
            if state:
                state = preprocess(prefix, state, "STATE")
                output += ' ' + str(state) + ','
            else:
                output += ' ' + str(states[i]) + ','
        output = output[0:-1]
        output += ' ' + '},\n'
    output += "};\n"
    if not function:
        output += "static " + action_type + " %s_transform_actions[%d][%d] = {\n" % (prefix.lower(), len(states), len(events))
        for i in range(len(states)):
            output += ' ' * 2 + '{'
            for j in range(len(events)):
                (action, state) = transformings[i][j]
                if action:
                    action = preprocess(prefix, action, "ACTION")
                    output += ' ' + str(action) + ','
                else:
                    output += ' 0,'
            output = output[0:-1]
            output += ' ' + '},\n'
        output += "};\n"
        output += "enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data) {\n" % (prefix, prefix.lower(), prefix, prefix)
        if debug:
            output += ' ' * 2 + 'printf("(");\n'
            output += ' ' * 2 + 'printf(%s_event_strings[event]);\n' % prefix.lower()
            output += ' ' * 2 + 'printf(", ");\n'
            output += ' ' * 2 + 'printf(%s_state_strings[state]);\n' % prefix.lower()
            output += ' ' * 2 + 'printf(") => (");\n'
            output += ' ' * 2 + 'printf(%s_action_strings[%s_transform_actions[state][event]]);\n' % (prefix.lower(), prefix.lower())
            output += ' ' * 2 + 'printf(", ");\n'
            output += ' ' * 2 + 'printf(%s_state_strings[%s_transform_states[state][event]]);\n' % (prefix.lower(), prefix.lower())
            output += ' ' * 2 + 'printf(")\\n");\n'
        output += ' ' * 2 + '%s_do_action(%s_transform_actions[state][event], data);\n' % (prefix.lower(), prefix.lower())
        output += ' ' * 2 + 'return %s_transform_states[state][event];\n' % (prefix.lower())
        output += "}\n"
    else:
        actions = {}
        tmp = "static %s_state_machine_action_fn %s_transform_actions[%d][%d] = {\n" % (prefix.lower(), prefix.lower(), len(states), len(events))
        for si in range(len(states)):
            tmp += ' ' * 2 + '{'
            for ei in range(len(events)):
                (action, state) = transformings[si][ei]
                if action:
                    actions[action.lower()] = 1
                    tmp += preprocess(prefix, action).lower() + ', '
                else:
                    tmp += 'NULL, '
            tmp = tmp[0:-2]
            tmp += '},\n'
        tmp += "};\n"
        for action in actions.keys():
            output += 'extern void %s(struct %s_context * ctx, enum %s_STATE state, enum %s_EVENT event);\n' % (preprocess(prefix, action).lower(), prefix.lower(), prefix, prefix)
        output += tmp;
        output += "void %s_init_state_machine(struct %s_state_machine * fsm, struct %s_context * ctx) {\n" % (prefix.lower(), prefix.lower(), prefix.lower())
        output += ' ' * 2 + 'fsm->ctx = ctx;\n'
        output += ' ' * 2 + 'fsm->state = %s;\n' % (states[0])
        output += "}\n"
        output += "void %s_process(struct %s_state_machine * fsm, enum %s_EVENT event) {\n" % (prefix.lower(), prefix.lower(), prefix)
        if debug:
            output += ' ' * 2 + 'printf("(");\n'
            output += ' ' * 2 + 'printf(%s_event_strings[event]);\n' % prefix.lower()
            output += ' ' * 2 + 'printf(", ");\n'
            output += ' ' * 2 + 'printf(%s_state_strings[fsm->state]);\n' % prefix.lower()
            output += ' ' * 2 + 'printf(") => (");\n'
            output += ' ' * 2 + 'printf(%s_action_strings[fsm->state][event]);\n' % (prefix.lower())
            output += ' ' * 2 + 'printf(", ");\n'
            output += ' ' * 2 + 'printf(%s_state_strings[%s_transform_states[fsm->state][event]]);\n' % (prefix.lower(), prefix.lower())
            output += ' ' * 2 + 'printf(")\\n");\n'
        output += ' ' * 2 + 'if (%s_transform_actions[fsm->state][event]) {\n' % (prefix.lower())
        output += ' ' * 4 + '%s_transform_actions[fsm->state][event](fsm->ctx, fsm->state, event);\n' % (prefix.lower())
        output += ' ' * 2 + "};\n"
        output += ' ' * 2 + "fsm->state = %s_transform_states[fsm->state][event];\n" % (prefix.lower())
        output += "};\n"
    return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings, function):
    import os.path
    states = [preprocess(prefix, state, "STATE") for state in states]
    events = [preprocess(prefix, event, "EVENT") for event in events]
    actions = [preprocess(prefix, action, "ACTION") for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    header = root + ".h"
    defination = os.path.join(directory, header)
    implementation = os.path.join(directory, root + ".c")
    with open(defination, 'w') as output:
        output.write('#ifndef __%s\n' % (header.replace('-', '_').replace('.', '_').upper()))
        output.write('#define __%s\n' % (header.replace('-', '_').replace('.', '_').upper()))
        output.write(state(prefix, states))
        output.write("\n")
        output.write(event(prefix, events))
        output.write("\n")
        if not function:
            output.write(action(prefix, actions))
            output.write("\n")
            output.write("enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data);\n" % (prefix, prefix.lower(), prefix, prefix))
            output.write("void %s_do_action(enum %s_ACTION action, void * data);\n" % (prefix.lower(), prefix))
        else:
            output.write("struct %s_context;\n" % (prefix.lower()))
            output.write("struct %s_state_machine {\n" % (prefix.lower()))
            output.write(' ' * 2 + "enum %s_STATE state;\n" % (prefix))
            output.write(' ' * 2 + "struct %s_context * ctx;\n" % (prefix.lower()))
            output.write("};\n")
            output.write("typedef void (* %s_state_machine_action_fn)(struct %s_context * ctx, enum %s_STATE state, enum %s_EVENT event);\n" % (prefix.lower(), prefix.lower(), prefix, prefix))
            output.write("void %s_init_state_machine(struct %s_state_machine * fsm, struct %s_context * ctx);\n" % (prefix.lower(), prefix.lower(), prefix.lower()))
            output.write("void %s_process(struct %s_state_machine * fsm, enum %s_EVENT event);\n" % (prefix.lower(), prefix.lower(), prefix))
        output.write("#endif\n")
    with open(implementation, 'w') as output:
        if debug:
            output.write('#include <stdio.h>\n')
        output.write('#include <stdlib.h>\n')
        output.write('#include "%s"\n' % header)
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug, function))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug, function))
        output.write("\n");
