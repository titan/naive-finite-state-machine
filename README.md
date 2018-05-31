# finite-state-machine

A simple finite state machine generator which genrate source code from
Excel to C language.

A typical finite state machine is consist of tuple(Action, Event,
State). When an event occurred, the finite state machine should do the
action first, then transform to the new state. This is how the finite
state machine works.

## Requirement

1. Python3

2. xrld

## Usage

1. Define the finite state machine in an Excel file. The first colume
must be states, and the first row must be events. The (0, 0) cell is
useless could be anything. The rest cells descript combinations of
actions and new states in format of "action\state". If there is no
action to execute, the content of action could keep empty. If the
state does not change, keep state part empty as current state.

2. Run fsm-generator.py to generate defination header file and source
code like this:

    fsm-geneator.py --prefix xxx fsm.xlsx --defination yyy-fsm.h --implementation zzz-fsm.c

in where prefix is useful when there are more than 1 finite state
machine to use. --defination and --implementation indicate generated
header and source code file names. If these two parameters are
missing, then generated files will follow the pattern as the Excel
file.

3. Include the generated header files in your source code, then
implements xxx_do_action function to do actions according to the
current state and the occurred event. xxx_do_action has prototype
like:

   enum XXX_STATE do_action(enum XXX_STATE state, enum XXX_EVENT event, void * data);

in where XXX_STATE and XXX_EVENT are defined in defination header
file. The void pointer data argument is data passed by events and will
be transferred to the called action.

4. Emit the event in your source code according to IO, timer... Then
call state transformer function to run the finite state machine.
