#! /usr/bin/python3

def normalize(string):
    #if len(string) > 0 and string[0].isdigit():
    #    string = "number_" + string
    return string.replace(' == ', '_EQUALS_').replace(' != ', '_NOT_EQUALS_').replace(':=', '_ASSIGN_TO_').replace(' = ', '_EQUALS_').replace('=', '_EQUALS_').replace(' + ', '_PLUS_').replace('+', '_PLUS_').replace(' - ', '_MINUS_').replace('-', '_').replace(' > ', '_GREATER_THAN_').replace('>', 'GREATER_THAN').replace(' < ', '_LESS_THAN_').replace('<', 'LESS_THAN').replace(': ', '_COLON_').replace(':', '_COLON_').replace(', ', '_COMMA_').replace(',', '_COMMA_').replace('"', '_QUOTATION_').replace('.', '_DOT_').replace('?', '_QUESTION_').replace(' ', '_').replace('\n', '_NEWLINE_').replace('#', 'SHARP').upper()

def load_model(prefix, filename):
    import xlrd
    states = []
    events = []
    actions = {}
    wb = xlrd.open_workbook(filename)
    wx = wb.sheet_by_index(0)
    transformings = []
    headers = wx.row(0)
    for i in range(1, len(headers)):
        cell = headers[i].value
        events.append(prefix + "_" + normalize(str(cell)) + "_EVENT")
    slides = wx.col(0)
    for i in range(1, len(slides)):
        cell = slides[i].value
        states.append(prefix + "_" + normalize(str(cell)) + "_STATE")
    for i in range(1, wx.nrows):
        transformings.append([])
        for j in range(1, wx.ncols):
            cell = wx.cell(i, j).value
            if len(cell) > 0:
                [action, state] = normalize(str(cell)).split("\\")
                if action:
                    action = prefix + "_" + action + "_ACTION"
                    actions[action] = 0
                if state == "":
                    state = normalize(str(wx.cell(i, 0).value))
                transformings[i - 1].append((action, prefix + "_" + state + "_STATE"))
            else:
                transformings[i - 1].append((None, None))
    return states, events, actions.keys(), transformings

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
                if action:
                    output += ' ' * 4 + 'case ' + states[j] + ': {\n'
                    if debug:
                        output += ' ' * 6 + 'puts("(%s, %s) => (%s, %s)\\n");\n' % (events[i], states[j], action, state)
                    output += ' ' * 6 + '%s_do_action(%s, data);\n' % (prefix.lower(), action)
                    output += ' ' * 6 + 'return %s;\n' % state
                    output += ' ' * 4 + '}\n'
                else:
                    if debug:
                        output += ' ' * 4 + 'case %s: {\n' % states[j]
                        output += ' ' * 6 + 'puts("(%s, %s) => (N/A, %s)\\n");\n' % (events[i], states[j], state)
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
                output += ' ' + str(action) + ','
            else:
                output += ' 0,'
        output = output[0:-1]
        output += ' ' + '},\n'
    output += "};\n"
    output += "enum %s_STATE %s_transform_state(enum %s_STATE state, enum %s_EVENT event, void * data) {\n" % (prefix, prefix.lower(), prefix, prefix)
    if debug:
        output += ' ' * 2 + 'puts("(");\n'
        output += ' ' * 2 + 'puts(%s_event_strings[event]);\n' % prefix.lower()
        output += ' ' * 2 + 'puts(", ");\n'
        output += ' ' * 2 + 'puts(%s_state_strings[state]);\n' % prefix.lower()
        output += ' ' * 2 + 'puts(") => (");\n'
        output += ' ' * 2 + 'puts(%s_action_strings[%s_transform_actions[state][event]]);\n' % (prefix.lower(), prefix.lower())
        output += ' ' * 2 + 'puts(", ");\n'
        output += ' ' * 2 + 'puts(%s_state_strings[%s_transform_states[state][event]]);\n' % (prefix.lower(), prefix.lower())
        output += ' ' * 2 + 'puts(")\\n");\n'
    output += ' ' * 2 + '%s_do_action(%s_transform_actions[state][event], data);\n' % (prefix.lower(), prefix.lower())
    output += ' ' * 2 + 'return %s_transform_states[state][event];\n' % (prefix.lower())
    output += "}\n"
    return output

def main(src, prefix, directory, defination, implementation, debug, style):
    (states, events, actions, transformings) = load_model(prefix, src)
    import os.path
    if directory == None:
        directory = os.path.dirname(src)
    (root, ext) = os.path.splitext(os.path.basename(src))
    header = root + ".h"
    if defination == None:
        defination = os.path.join(directory, header)
    if implementation == None:
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

if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="The defination of state machine in xlsx")
    parser.add_argument("-p", "--prefix", default="", help="The prefix of generated structures and functions")
    parser.add_argument("-d", "--directory", help="The directory of generated files")
    parser.add_argument("--defination", help="The filename of definations header")
    parser.add_argument("--implementation", help="The filename of implementation")
    parser.add_argument("--debug", action='store_true', help="Output debug info in console")
    parser.add_argument("--style", default="code", help="The style of fsm: code(code directly) or table(table driven)")
    args = parser.parse_args()
    main(args.src, normalize(args.prefix), args.directory, args.defination, args.implementation, args.debug, args.style)
