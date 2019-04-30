def preprocess(cell, as_key = False):
    if cell.startswith('_'):
        cell = cell[1:]
    if cell.endswith('_'):
        cell = cell[:-1]
    if as_key:
        if cell[0].isdigit():
            cell = "NUMBER_" + cell
    return cell

def transforming(states, events, transformings):
  ssmapping = []
  for si in range(len(states)):
    tmp = [[] for x in range(len(states))]
    ssmapping.append(tmp)
    for ei in range(len(events)):
      (actions, state) = transformings[si][ei]
      if state:
        if len(actions) > 0:
          tmp[states.index(state)].append((events[ei].lower().replace('_', '-'), '\\n'.join(actions).replace('_', '-')))
        else:
          tmp[states.index(state)].append((events[ei].lower().replace('_', '-'), None))
      else:
        if len(actions) > 0:
          tmp[si].append((events[ei].lower(), '\\n'.join(actions).replace('_', '-')))
  output = '@startuml\n'
  output += '\n'.join(['state "{0}" as {1}'.format(state, preprocess(state).lower()) for state in states]) + '\n'
  output += '[*] --> {0}\n'.format(preprocess(states[0]).lower())
  for i in range(len(states)):
    for j in range(len(states)):
      label = []
      for (event, action) in ssmapping[i][j]:
        if action:
          label.append('%s\\n----\\n%s' % (event, action))
        else:
          label.append(event)
      if len(label) > 0:
        output += '%s --> %s : %s\n' % (preprocess(states[i]).lower(), preprocess(states[j]).lower(), "\\n\\n".join(label))
  output += '@enduml\n'
  return output

def process(src, prefix, directory, debug, style, states, events, actions, transformings):
  import os.path
  if directory == None:
    directory = os.path.dirname(src)
  (root, ext) = os.path.splitext(os.path.basename(src))
  dest = os.path.join(directory, root + '.uml')
  with open(dest, 'w') as output:
    output.write(transforming(states, events, transformings))
