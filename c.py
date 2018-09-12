def preprocess(prefix, postfix, cell):
    return ("%s_%s_%s" % (prefix, cell, postfix)).replace('__', '_')

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

def code_transforming(prefix, states, events, transformings, debug):
    output = "enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data) {\n" % (prefix, prefix.lower(), prefix, prefix)
    output += ' ' * 2 + 'switch (event) {\n'
    for i in range(len(events)):
        output += ' ' * 2 + 'case ' + events[i] + ': {\n'
        output += ' ' * 4 + 'switch (state) {\n'
        for j in range(len(states)):
            (action, state) = transformings[j][i]

            if state:
                state = preprocess(prefix, "STATE", state)
                if action:
                    action = preprocess(prefix, "ACTION", action)
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
    return output

def table_transforming(prefix, states, events, actions, transformings, debug):
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

        output += "char * %s_state_strings[%d] = {\n" % (prefix.lower(), len(states))
        for s in states:
            output += ' ' * 2 + '"%s",\n' % s
        output += "};\n"

        output += "char * %s_event_strings[%d] = {\n" % (prefix.lower(), len(events))
        for e in events:
            output += ' ' * 2 + '"%s",\n' % e
        output += "};\n"

        output += "char * %s_action_strings[%d] = {\n" % (prefix.lower(), len(actions) + 1)
        output += ' ' * 2 + '"N/A",\n'
        for a in actions:
            output += ' ' * 2 + '"%s",\n' % a
        output += "};\n"

    output += state_type + " %s_transform_states[%d][%d] = {\n" % (prefix.lower(), len(states), len(events))
    for i in range(len(states)):
        output += ' ' * 2 + '{'
        for j in range(len(events)):
            (action, state) = transformings[i][j]
            if state:
                state = preprocess(prefix, "STATE", state)
                output += ' ' + str(state) + ','
            else:
                output += ' ' + str(states[i]) + ','
        output = output[0:-1]
        output += ' ' + '},\n'
    output += "};\n"
    output += action_type + " %s_transform_actions[%d][%d] = {\n" % (prefix.lower(), len(states), len(events))
    for i in range(len(states)):
        output += ' ' * 2 + '{'
        for j in range(len(events)):
            (action, state) = transformings[i][j]
            if action:
                action = preprocess(prefix, "ACTION", action)
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
    return output

def process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings):
    import os.path
    states = [preprocess(prefix, "STATE", state) for state in states]
    events = [preprocess(prefix, "EVENT", event) for event in events]
    actions = [preprocess(prefix, "ACTION", action) for action in actions]
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    if defination == None:
        header = root + ".h"
        defination = os.path.join(directory, header)
    else:
        (root, ext) = os.path.splitext(os.path.basename(defination))
        header = root + ".h"
    if implementation == None:
        header = root + ".h"
        implementation = os.path.join(directory, root + ".c")
    with open(defination, 'w') as output:
        output.write(state(prefix, states))
        output.write("\n");
        output.write(event(prefix, events))
        output.write("\n");
        output.write(action(prefix, actions))
        output.write("\n");
        output.write("enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data);\n" % (prefix, prefix.lower(), prefix, prefix))
        output.write("void %s_do_action(enum %s_ACTION action, void * data);\n" % (prefix.lower(), prefix))
    with open(implementation, 'w') as output:
        if debug:
            output.write('#include <stdio.h>\n')
        output.write('#include "%s"\n' % header)
        if style == "code":
            output.write(code_transforming(prefix, states, events, transformings, debug))
        else:
            output.write(table_transforming(prefix, states, events, actions, transformings, debug))
        output.write("\n");
