#! /usr/bin/python3

def normalize(string):
    if len(string) > 0 and string[0].isdigit():
        string = "number_" + string
    return string.replace(' == ', '_EQUALS_').replace(' != ', '_NOT_EQUALS_').replace(':=', '_ASSIGN_TO_').replace(' = ', '_EQUALS_').replace('=', '_EQUALS_').replace(' + ', '_PLUS_').replace('+', '_PLUS_').replace(' - ', '_MINUS_').replace('-', '_').replace(' > ', '_GREATER_THAN_').replace('>', 'GREATER_THAN').replace(' < ', '_LESS_THAN_').replace('<', 'LESS_THAN').replace(': ', '_COLON_').replace(':', '_COLON_').replace(', ', '_COMMA_').replace(',', '_COMMA_').replace('"', '_QUOTATION_').replace('.', '_DOT_').replace('?', '_QUESTION_').replace(' ', '_').replace('\n', '_NEWLINE_').upper()

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
        events.append(prefix + "_" + normalize(cell) + "_EVENT")
    slides = wx.col(0)
    for i in range(1, len(slides)):
        cell = slides[i].value
        states.append(prefix + "_" + normalize(cell) + "_STATE")
    for i in range(1, wx.nrows):
        transformings.append([])
        for j in range(1, wx.ncols):
            cell = wx.cell(i, j).value
            if len(cell) > 0:
                [action, state] = normalize(cell).split("\\")
                if action:
                    action = prefix + "_" + action + "_ACTION"
                    actions[action] = 0
                transformings[i - 1].append((action, prefix + "_" + state + "_STATE"))
            else:
                transformings[i - 1].append((None, None))
    return states, events, actions.keys(), transformings

def state(prefix, states):
    output = "enum %s_STATE {\n" % prefix.upper()
    for s in states:
        output += " " * 2 + s + ",\n"
    output += "};\n"
    return output

def event(prefix, events):
    output = "enum %s_EVENT {\n" % prefix.upper()
    for e in events:
        output += " " * 2 + e + ",\n"
    output += "};\n"
    return output

def action(prefix, actions):
    output = "enum %s_ACTION {\n" % prefix.upper()
    for a in actions:
        output += " " * 2 + a + ",\n"
    output += "};\n"
    return output

def transforming(prefix, states, events, transformings):
    output = "enum %s_STATE %s_state_transform(enum %s_STATE state, enum %s_EVENT event, void * data) {\n" % (prefix, prefix.lower(), prefix, prefix)
    output += ' ' * 2 + 'switch (event) {\n'
    for i in range(len(events)):
        output += ' ' * 2 + 'case ' + events[i] + ': {\n'
        output += ' ' * 4 + 'switch (state) {\n'
        for j in range(len(states)):
            (action, state) = transformings[j][i]
            if state:
                if action:
                    output += ' ' * 4 + 'case ' + states[j] + ': {\n'
                    output += ' ' * 6 + '%s_do_action(%s, data);\n' % (prefix.lower(), action)
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

def main(src, output, prefix, defination, implementation):
    (states, events, actions, transformings) = load_model(prefix, src)
    if implementation:
        output.write(transforming(prefix, states, events, transformings))
        output.write("\n");
    else:
        output.write(state(prefix, states))
        output.write("\n");
        output.write(event(prefix, events))
        output.write("\n");
        output.write(action(prefix, actions))
        output.write("\n");
        output.write("enum %s_STATE %s_state_transform(enum %s_STATE state, enum %s_EVENT event, void * data);\n" % (prefix, prefix.lower(), prefix, prefix))

if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="the defination of state machine in xlsx")
    parser.add_argument("-o", "--output", default=sys.stdout, type=argparse.FileType('w'), help="Save output to the file")
    parser.add_argument("-p", "--prefix", default="", help="The prefix of generated structures and functions")
    parser.add_argument("--defination", default=True, action="store_true", help="Output definations")
    parser.add_argument("--implementation", default=False, action="store_true", help="Output implementation")
    args = parser.parse_args()
    main(args.src, args.output, normalize(args.prefix), args.defination, args.implementation)