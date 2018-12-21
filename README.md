# naive-finite-state-machine

A simple finite state machine generator which genrate state machine
source code from table format files, like Excel or csv.

A typical naive finite state machine is consist of tuple(Action,
Event, State, NextState). When an event occurred, the naive finite
state machine should execute the action first according to the current
state of state machine, then transform to the next state. This is how
the naive finite state machine works.

## Requirement

1. Python3

2. xrld(For Excel files)

## Usage

1. Define the finite state machine in an table file. The first colume
must be states, and the first row must be events. The (0, 0) cell is
useless could be anything. The rest cells descript combinations of
actions and the next states with format as 'action\n----\n next
state'. If there is no action to execute, the content of action could
keep empty. And if the state does not change, keep state part empty as
current state.

2. Run naive-fsm-generator.py to generate source code like this:

    fsm-geneator.py --prefix xxx fsm.txt --style table --target c

in where prefix is useful when there are more than 1 finite state
machine to use.
