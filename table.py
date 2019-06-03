from table_fsm import Delegate as TableDelegate, StateMachine

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
        self.cellwidths = []
        self.cellwidth = 0
        self.cellindex = 0

class MyTableDelegate(TableDelegate):
    def error(self, ctx, state = 0, event = 0):
        print("Invalid table format at col %d in line %d" % (ctx.col, ctx.line))
        exit(-1)
    def reset_cell_index(self, ctx):
        ctx.cellindex = 0
    def append_width(self, ctx):
        ctx.cellwidths.append(ctx.cellwidth)
    def reset_width(self, ctx):
        ctx.cellwidth = 0
    def incr_width(self, ctx):
        ctx.cellwidth += 1
    def append(self, ctx, state = 0, event = 0):
        ctx.buf += ctx.ch
    def cell(self, ctx, state = 0, event = 0):
        ctx.cells.append(ctx.buf.strip())
        ctx.buf = ''
    def incr_cell_index(self, ctx):
        ctx.cellindex += 1
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
        for cell in cells:
            if len(cell) > 0:
                content = '\n'.join(cell)
                if content.startswith('----') or content.startswith('===='):
                    content = '\n' + content
                if content.endswith('----') or content.endswith('===='):
                    content += '\n'
                row.append(content)
            else:
                row.append(None)
        row = []
        for c in cells:
            row.append('\n'.join(c))
        ctx.rows.append(row)
        ctx.lines = []
    def clear_widths(self, ctx):
        ctx.cellwidths = []

def reader(src):
    ctx = TableContext()
    fsm = StateMachine(MyTableDelegate())
    for ch in src:
        ctx.ch = ch
        if ch == '\n':
            ctx.line += 1
            ctx.col = 1
            fsm.lf(ctx)
        elif ch == '+':
            fsm.plus(ctx)
            ctx.col += 1
        elif ch == '-':
            fsm.minus(ctx)
            ctx.col += 1
        elif ch == '|':
            splitors = [1]
            for cellwidth in ctx.cellwidths:
                splitors.append(splitors[-1] + cellwidth + 1)
            if ctx.col in splitors:
                fsm.pipe(ctx)
            else:
                fsm.pipe_in_cell(ctx)
            ctx.col += 1
        else:
            fsm.others(ctx)
            ctx.col += 1
    return ctx.rows
