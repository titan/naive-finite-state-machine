def transforming(states, events, transformings):
  ssmapping = []
  for si in range(len(states)):
    tmp = [[] for x in range(len(states))]
    ssmapping.append(tmp)
    for ei in range(len(events)):
      (action, state) = transformings[si][ei]
      if state:
        if action:
          tmp[states.index(state)].append((events[ei], action))
        else:
          tmp[states.index(state)].append((events[ei], None))
      else:
        if action:
          tmp[si].append((events[ei], action))
  output = 'digraph fsm {\n'
  output += ' ' * 8 + 'node [shape="box"];\n'
  output += ' ' * 8 + 'edge [decorate=true];\n'
  output += ' ' * 8 + 'graph [ranksep=2, nodesep=.5]\n'
  output += ' ' * 8 + 'concentrate = false;\n'
  for i in range(len(states)):
    for j in range(len(states)):
      label = []
      for (event, action) in ssmapping[i][j]:
        if action:
          label.append('%s: %s' % (event, action))
        else:
          label.append(event)
      if len(label) > 0:
        output += ' ' * 8 + '%s -> %s [label="%s", weight=%d];\n' % (states[i], states[j], "\\n".join(label), len(label))
  output += '}\n'
  return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings, function):
  import os.path
  if directory == None:
    directory = os.path.dirname(src)
  (root, ext) = os.path.splitext(os.path.basename(src))
  dest = os.path.join(directory, root + '.dot')
  with open(dest, 'w') as output:
    output.write(transforming(states, events, transformings))
