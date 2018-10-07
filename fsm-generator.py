#! /usr/bin/python3

class ParsingContext:
    def __init__(self):
        self.buf = ""
        self.tmp = ""
        self.ch = None
        self.action = None
        self.state = None

def cell_do_action(action, ctx):
    import cell_fsm
    if action == cell_fsm.Action.APPEND_TMP:
        ctx.tmp += ctx.ch
    elif action == cell_fsm.Action.APPEND:
        ctx.buf += ctx.ch
    elif action == cell_fsm.Action.COMBINE_TMP_COMMA_APPEND:
        ctx.buf += ctx.tmp
        ctx.tmp = ""
        ctx.buf += ctx.ch
    elif action == cell_fsm.Action.COMBINE_TMP_COMMA_ACTION:
        ctx.buf += ctx.tmp
        ctx.tmp = ""
        ctx.action = ctx.buf
        ctx.buf = ""
    elif action == cell_fsm.Action.ACTION:
        ctx.action = ctx.buf
        ctx.buf = ""
    elif action == cell_fsm.Action.STATE:
        ctx.state = ctx.buf
        ctx.buf = ""
    elif action == cell_fsm.Action.STATE_ERROR:
        ctx.buf += ctx.ch
        print("Invalid state: %s" % ctx.buf)
        exit(-1)
    elif action == cell_fsm.Action.COMMENT_ERROR:
        ctx.buf += ctx.ch
        print("Invalid comment: %s" % ctx.buf)
        exit(-1)

def normalize(string):
    #if len(string) > 0 and string[0].isdigit():
    #    string = "number_" + string
    return string.replace('_', '_UNDERLINE_').replace('!=', '_NOT_EQUALS_').replace(':=', '_ASSIGN_TO_').replace('==', '_EQUALS_').replace('=', '_EQUALS_').replace('+', '_PLUS_').replace('-', '_MINUS_').replace('>', '_GREATER_THAN_').replace('<', '_LESS_THAN_').replace('(', '_OPEN_PARENTHESIS_').replace(')', '_CLOSE_PARENTHESIS_').replace('[', '_OPEN_BRACKET_').replace(']', '_CLOSE_BRACKET_').replace('{', '_OPEN_BRACE_').replace('}', '_CLOSE_BRACE_').replace(':', '_COLON_').replace(',', '_COMMA_').replace(';', '_SEMI_COLON_').replace('"', '_DOUBLE_QUOTES_').replace("'", '_QUOTES_').replace('.', '_DOT_').replace('?', '_QUESTION_').replace('%', '_PERCENT_').replace(' ', '_').replace('\n', '_NEWLINE_').replace('#', '_SHARP_').replace('*', '_ASTERISK_').replace('\\', '_BACKSLASH_').replace('__', '_').replace('__', '_').upper()

def load_model_from_excel(filename):
    import xlrd
    import cell_fsm
    states = []
    events = []
    actions = {}
    wb = xlrd.open_workbook(filename)
    wx = wb.sheet_by_index(0)
    transformings = []
    headers = wx.row(0)
    for i in range(1, len(headers)):
        cell = headers[i].value
        events.append(normalize(str(cell)).replace('__', '_'))
    slides = wx.col(0)
    for i in range(1, len(slides)):
        cell = slides[i].value
        states.append(normalize(str(cell)).replace('__', '_'))
    for i in range(1, wx.nrows):
        transformings.append([])
        for j in range(1, wx.ncols):
            cell = wx.cell(i, j).value
            if len(cell) > 0:
                ctx = ParsingContext()
                fsm = cell_fsm.FSM(cell_do_action)
                for ch in str(cell):
                    ctx.ch = ch
                    if ch == '\n':
                        fsm.process(cell_fsm.Event.LF, ctx)
                    elif ch == '-':
                        fsm.process(cell_fsm.Event.MINUS, ctx)
                    elif ch == '=':
                        fsm.process(cell_fsm.Event.EQUALS, ctx)
                    elif ch == '\\':
                        fsm.process(cell_fsm.Event.BACKSLASH, ctx)
                    elif ch == '(':
                        fsm.process(cell_fsm.Event.OPEN_PARENTHESIS, ctx)
                    elif ch == ')':
                        fsm.process(cell_fsm.Event.CLOSE_PARENTHESIS, ctx)
                    else:
                        fsm.process(cell_fsm.Event.OTHERS, ctx)
                fsm.process(cell_fsm.Event.EOI, ctx)
                if ctx.action:
                    ctx.action = normalize(ctx.action).replace('__', '_')
                    actions[ctx.action] = 0
                if not ctx.state or ctx.state == "":
                    ctx.state = str(wx.cell(i, 0).value)
                transformings[i - 1].append((ctx.action, normalize(ctx.state).replace('__', '_')))
            else:
                transformings[i - 1].append((None, None))
    return states, events, actions.keys(), transformings

def load_model_from_csv(filename):
    import csv
    import cell_fsm
    states = []
    events = []
    actions = {}
    transformings = []
    with open(filename, 'r') as line:
        reader = csv.reader(line, dialect='excel')
        first = True
        for row in reader:
            if first:
                first = False
                headers = row[1:]
                for event in headers:
                    events.append(normalize(str(event)).replace('__', '_'))
            else:
                transformings.append([])
                st = state = str(row[0])
                states.append(normalize(state).replace('__', '_'))
                for cell in row[1:]:
                    if len(cell) > 0:
                        ctx = ParsingContext()
                        fsm = cell_fsm.FSM(cell_do_action)
                        for ch in str(cell):
                            ctx.ch = ch
                            if ch == '\n':
                                fsm.process(cell_fsm.Event.LF, ctx)
                            elif ch == '-':
                                fsm.process(cell_fsm.Event.MINUS, ctx)
                            elif ch == '=':
                                fsm.process(cell_fsm.Event.EQUALS, ctx)
                            elif ch == '\\':
                                fsm.process(cell_fsm.Event.BACKSLASH, ctx)
                            elif ch == '(':
                                fsm.process(cell_fsm.Event.OPEN_PARENTHESIS, ctx)
                            elif ch == ')':
                                fsm.process(cell_fsm.Event.CLOSE_PARENTHESIS, ctx)
                            else:
                                fsm.process(cell_fsm.Event.OTHERS, ctx)
                        fsm.process(cell_fsm.Event.EOI, ctx)
                        if ctx.action:
                            ctx.action = normalize(ctx.action).replace('__', '_')
                            actions[ctx.action] = 0
                        if not ctx.state or ctx.state == "":
                            ctx.state = st
                        transformings[-1].append((ctx.action, normalize(ctx.state).replace('__', '_')))
                    else:
                        transformings[-1].append((None, None))
    return states, events, actions.keys(), transformings

def main(src, prefix, directory, defination, implementation, debug, style, target):
    if src.endswith("csv"):
        (states, events, actions, transformings) = load_model_from_csv(src)
    else:
        (states, events, actions, transformings) = load_model_from_excel(src)
    if target == "c":
        import c
        c.process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings)
    elif target == "python":
        import python
        python.process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings)

if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="The defination of state machine in xlsx or csv")
    parser.add_argument("-p", "--prefix", default="", help="The prefix of generated structures and functions")
    parser.add_argument("-d", "--directory", help="The directory of generated files")
    parser.add_argument("--defination", help="The filename of definations header")
    parser.add_argument("--implementation", help="The filename of implementation")
    parser.add_argument("--debug", action='store_true', help="Output debug info in console")
    parser.add_argument("--style", default="code", help="The style of fsm: code(code directly) or table(table driven)")
    parser.add_argument("--target", default="c", help="The target language of fsm: c or python")
    args = parser.parse_args()
    main(args.src, args.prefix.replace('-', '_').upper(), args.directory, args.defination, args.implementation, args.debug, args.style, args.target)
