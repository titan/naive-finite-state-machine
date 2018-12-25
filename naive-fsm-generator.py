#! /usr/bin/python3

def normalize(string):
    #if len(string) > 0 and string[0].isdigit():
    #    string = "number_" + string
    mappings = {}
    mappings['_'] = '_UNDERLINE_'
    mappings['!='] = '_NOT_EQUALS_'
    mappings[':='] = '_ASSIGN_TO_'
    mappings['=='] = '_EQUALS_'
    mappings['='] = '_EQUALS_'
    mappings['+'] = '_PLUS_'
    mappings['-'] = '_MINUS_'
    mappings['>'] = '_GREATER_THAN_'
    mappings['<'] = '_LESS_THAN_'
    mappings['('] = '_OPEN_PARENTHESIS_'
    mappings[')'] = '_CLOSE_PARENTHESIS_'
    mappings['['] = '_OPEN_BRACKET_'
    mappings[']'] = '_CLOSE_BRACKET_'
    mappings['{'] = '_OPEN_BRACE_'
    mappings['}'] = '_CLOSE_BRACE_'
    mappings[':'] = '_COLON_'
    mappings[','] = '_COMMA_'
    mappings[';'] = '_SEMI_COLON_'
    mappings['"'] = '_DOUBLE_QUOTES_'
    mappings["'"] = '_APOSTROPHE_'
    mappings['.'] = '_DOT_'
    mappings['?'] = '_QUESTION_'
    mappings['%'] = '_PERCENT_'
    mappings[' '] = '_'
    mappings['\n'] = '_NEWLINE_'
    mappings['#'] = '_SHARP_'
    mappings['*'] = '_ASTERISK_'
    mappings['\\'] = '_BACKSLASH_'
    mappings['|'] = '_PIPE_'
    mappings['!'] = '_EXCLAM_'
    mappings['/'] = '_SLASH_'
    for (k, v) in mappings.items():
        string = string.replace(k, v)
    return string.replace(' ', '_').replace('__', '_').replace('__', '_').upper()

def load_model_from_excel(filename):
    import xlrd
    model = []
    wb = xlrd.open_workbook(filename)
    wx = wb.sheet_by_index(0)
    for i in range(0, wx.nrows):
        row = []
        for j in range(0, wx.ncols):
            row.append(wx.cell(i, j).value)
        model.append(row)
    return model

def load_model_from_csv(filename):
    import csv
    model = []
    with open(filename, 'r') as line:
        reader = csv.reader(line, dialect='excel')
        for row in reader:
            line = []
            for col in row:
                line.append(col)
            model.append(line)
    return model

class TableContext:
    def __init__(self):
        self.buf = ""
        self.tmp = ""
        self.ch = None
        self.line = 1
        self.col = 1
        self.cells = []
        self.lines = []
        self.rows = []

class TableDelegate:
    def error(self, ctx, state = 0, event = 0):
        print("Invalid table format at col %d in line %d" % (ctx.col, ctx.line))
        exit(-1)
    def append(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.ch
    def cell(self, ctx, state = 0, event = 0):
        ctx.cells.append(ctx.buf.strip())
        ctx.buf = ''
    def line(self, ctx, state = 0, event = 0):
        ctx.lines.append(ctx.cells)
        ctx.cells = []
    def row(self, ctx, state = 0, event = 0):
        cells = []
        for i in range(len(ctx.lines[0])):
            cells.append([])
        for row in range(len(ctx.lines)):
            for col in range(len(ctx.lines[row])):
                if len(ctx.lines[row][col]) > 0:
                    cells[col].append(ctx.lines[row][col])
        row = []
        for c in cells:
            row.append('\n'.join(c))
        ctx.rows.append(row)
        ctx.lines = []

def load_model_from_table(src):
    from table_fsm import Event, StateMachine
    ctx = TableContext()
    fsm = StateMachine(TableDelegate())
    with open(src, 'r') as input:
        content = input.read(-1)
        for ch in content:
            ctx.ch = ch
            if ch == '\n':
                ctx.line += 1
                ctx.col = 1
                fsm.process(ctx, Event.LF)
            elif ch == '+':
                fsm.process(ctx, Event.PLUS)
                ctx.col += 1
            elif ch == '-':
                fsm.process(ctx, Event.MINUS)
                ctx.col += 1
            elif ch == '|':
                fsm.process(ctx, Event.PIPE)
                ctx.col += 1
            else:
                fsm.process(ctx, Event.OTHERS)
                ctx.col += 1
    return ctx.rows

class CellContext:
    def __init__(self):
        self.buf = ""
        self.tmp = ""
        self.ch = None
        self.action = None
        self.state = None

class CellDelegate:
    def append_tmp(self, ctx, state = 0, event = 0):
        ctx.tmp += ctx.ch
    def comment_error(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.ch
        print("Invalid comment: %s" % ctx.buf)
        exit(-1)
    def append(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.ch
    def combine_tmp_comma_append(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.tmp
        ctx.tmp = ""
        ctx.buf += ctx.ch
    def combine_tmp_comma_action(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.tmp
        ctx.tmp = ""
        ctx.action = ctx.buf
        ctx.buf = ""
    def action(self, ctx, state = 0, event = 0):
        ctx.action = ctx.buf
        ctx.buf = ""
    def state_error(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.ch
        print("Invalid state: %s" % ctx.buf)
        exit(-1)
    def state(self, ctx, state = 0, event = 0):
        ctx.state = ctx.buf
        ctx.buf = ""

def extract_model(model):
    from cell_fsm import Event, StateMachine
    states = []
    events = []
    actions = {}
    transformings = []
    headers = model[0]
    for i in range(1, len(headers)):
        cell = headers[i]
        events.append(normalize(str(cell)).replace('__', '_'))
    for i in range(1, len(model)):
        cell = model[i][0]
        states.append(normalize(str(cell)).replace('__', '_'))
    for i in range(1, len(model)):
        transformings.append([])
        for j in range(1, len(model[i])):
            cell = model[i][j]
            if len(cell) > 0:
                ctx = CellContext()
                fsm = StateMachine(CellDelegate())
                for ch in str(cell):
                    ctx.ch = ch
                    if ch == '\n':
                        fsm.process(ctx, Event.LF)
                    elif ch == '-':
                        fsm.process(ctx, Event.MINUS)
                    elif ch == '\\':
                        fsm.process(ctx, Event.BACKSLASH)
                    elif ch == '(':
                        fsm.process(ctx, Event.OPEN_PARENTHESIS)
                    elif ch == ')':
                        fsm.process(ctx, Event.CLOSE_PARENTHESIS)
                    else:
                        fsm.process(ctx, Event.OTHERS)
                fsm.process(ctx, Event.EOI)
                if ctx.action:
                    ctx.action = normalize(ctx.action).replace('__', '_')
                    actions[ctx.action] = 0
                if not ctx.state or ctx.state == "":
                    ctx.state = str(model[i][0])
                transformings[i - 1].append((ctx.action, normalize(ctx.state).replace('__', '_')))
            else:
                transformings[i - 1].append((None, None))
    return states, events, actions.keys(), transformings

def main(src, prefix, directory, defination, implementation, debug, style, target, function):
    model = None
    if src.endswith("csv"):
        model = load_model_from_csv(src)
    elif src.endswith("xls"):
        model = load_model_from_excel(src)
    elif src.endswith("xlsx"):
        model = load_model_from_excel(src)
    else:
        model = load_model_from_table(src)
    if model == None:
        print("Cannot load model from %s" % src)
        exit(-1)
    (states, events, actions, transformings) = extract_model(model)
    if target == "c":
        import c
        c.process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings, function)
    elif target == "python":
        import python
        python.process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings, function)
    elif target == 'dart':
        import dart
        dart.process(src, prefix, directory, defination, implementation, debug, style, states, events, actions, transformings, function)

if __name__ == '__main__':
    import argparse
    import sys
    from os.path import basename
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="The defination of state machine in xlsx or csv")
    parser.add_argument("-p", "--prefix", default="", help="The prefix of generated structures and functions")
    parser.add_argument("-d", "--directory", help="The directory of generated files")
    parser.add_argument("--defination", help="The filename of definations header")
    parser.add_argument("--implementation", help="The filename of implementation")
    parser.add_argument("--debug", action='store_true', help="Output debug info in console")
    parser.add_argument("--style", default="table", help="The style of fsm: code(code directly) or table(table driven)")
    parser.add_argument("--target", default="c", help="The target language of fsm: c, dart or python")
    args = parser.parse_args()
    main(args.src, args.prefix.replace('-', '_').upper(), args.directory, args.defination, args.implementation, args.debug, args.style, args.target, True if basename(sys.argv[0]) == 'naive-fsm-generator.py' else False)
