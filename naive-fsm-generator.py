#! /usr/bin/python3

from semantic import Assignment, Call, Expression, Identifier
from analyzer import ActionSyntaxer, ActionLexerAdapter
from lexer import Lexer

def normalize(string):
    #if len(string) > 0 and string[0].isdigit():
    #    string = "number_" + string
    if not string:
        return None
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
    mappings['$'] = '_DOLLAR_'
    for (k, v) in mappings.items():
        string = string.replace(k, v)
    result = string.replace(' ', '_').replace('__', '_').replace('__', '_').upper()
    if result[0] == '_':
        result = result[1:]
    if result[-1] == '_':
        result = result[:-1]
    return result

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

def load_model_from_table(src):
    import table
    model = []
    with open(src, 'r') as input:
        content = input.read()
        model = table.reader(content)
    return model

def extract_model(model, normalizing = True):
    states = []
    events = []
    actionmap = {}
    transformings = []
    headers = model[0]
    for i in range(1, len(headers)):
        cell = headers[i]
        events.append(str(cell) if not normalizing else normalize(str(cell)))
    for i in range(1, len(model)):
        cell = model[i][0]
        states.append(str(cell) if not normalizing else normalize(str(cell)))
    for i in range(1, len(model)):
        transformings.append([])
        for j in range(1, len(model[i])):
            cell = model[i][j]
            if len(cell) > 0:
                state_line = False
                actions = []
                statelines = []
                for line in str(cell).split('\n'):
                    if line.startswith('----') or line.startswith('===='):
                        state_line = True
                        continue
                    if not state_line:
                        if len(line) == 0:
                            continue
                        syntaxer = ActionSyntaxer()
                        lexer = Lexer(ActionLexerAdapter(syntaxer))
                        for ch in line:
                            lexer.feed(ch)
                        lexer.eof()
                        syntaxer.eof()
                        if isinstance(syntaxer.result(), Call):
                            action = syntaxer.result()
                            actionkey = normalize(str(action).replace('()', '')).lower() if normalizing else str(action).replace('()', '')
                            actions.append(actionkey)
                            actionmap[actionkey] = None
                    else:
                        statelines.append(line)
                while statelines.count('') > 0:
                    statelines.remove('')
                if len(statelines) == 0:
                    state = None
                else:
                    state = '\n'.join(statelines)
                    if normalizing:
                        state = normalize(state)
                transformings[i - 1].append((actions, state))
            else:
                transformings[i - 1].append(([], None))
    return states, events, actionmap.keys(), transformings

def main(src, prefix, directory, debug, style, lang):
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
    if lang == "c":
        (states, events, actions, transformings) = extract_model(model)
        import c
        c.process(src, prefix, directory, debug, style, states, events, actions, transformings)
    elif lang == "python":
        (states, events, actions, transformings) = extract_model(model)
        import python
        python.process(src, prefix, directory, debug, style, states, events, actions, transformings)
    elif lang == 'nim':
        (states, events, actions, transformings) = extract_model(model)
        import nim
        nim.process(src, prefix, directory, debug, style, states, events, actions, transformings)
    elif lang == 'dot':
        (states, events, actions, transformings) = extract_model(model)
        import dot
        dot.process(src, prefix, directory, debug, style, states, events, actions, transformings)
    elif lang == 'plantuml':
        (states, events, actions, transformings) = extract_model(model, normalizing = False)
        import plantuml
        plantuml.process(src, prefix, directory, debug, style, states, events, actions, transformings)

if __name__ == '__main__':
    import argparse
    import sys
    from os.path import basename
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="The defination of state machine in xlsx or csv")
    parser.add_argument("-p", "--prefix", default="", help="The prefix of generated structures and functions")
    parser.add_argument("-d", "--directory", help="The directory of generated files")
    parser.add_argument("--debug", action='store_true', help="Output debug info in console")
    parser.add_argument("--style", default="table", help="The style of fsm: code(code directly) or table(table driven)")
    parser.add_argument("--lang", default="c", help="The target language of fsm: c, dot, nim, plantuml or python")
    args = parser.parse_args()
    main(args.src, args.prefix.replace('-', '_').upper(), args.directory, args.debug, args.style, args.lang)
