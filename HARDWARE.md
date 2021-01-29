Hardware
========

These are the specifications for the type of hardware that can be defined in the
`.hardware` section of a drone file. The specifications in that file determine
what capabilities the drone will have, and its cost.

Format
======

The format of the hardware section can be seen in example drones in the
`./examples/` directory, but the section is defined as any section, a line
starting with (optional) whitespace, then the static string `.hardware`
Under it, variables are defined that have static names, such as `%CPU` and
`%tracks`. Some of those are required, like `%CPU` and `%MEM`, but others
are not.

Required Hardware
=================

A drone must specify the following variables in the `.hardware` section:

`%CPU`: defines which registers are available, instructions, and stack size.
`%MEM`: defines how large the drone's code can get (each line of code is four
bytes)
`%CHASSIS`: defines the size of the drone, how many weapons it can carry and max
size of certain other bits of hardware, like `%TRACKS`
`%TRACKS`: the tank treads, determining the max speed and acceleration of a
drone

CPU
=====

The variable name is `%CPU`. It can be one of `small`, `medium`, or `large`.
Each CPU gives access to different capabilities, such as more registers.
All CPU registers are 16-bit, regardless of CPU size.
16-bit registers allow these ranges of values:

```
signed (allows negative): −32,768 to 32,767
unsigned (positive only): 0 to 65,535
```

The CPUs might also have 32-bit floating point registers.
They allow these values (roughly, with floating point errors):

```
32-bit float: 
```

All CPUs share these registers:

```
sp: stack pointer
ip: instruction pointer (which instruction is running)
```


small
-----

The `small` CPU has 2 16-bit registers, `%ax` and `%cx`.
It has a stack size of 256 bytes.

medium
------

The `medium` CPU has 3 16-bit registers, `%ax`, `%cx` and `%dx`.
It has a stack size of 1024 bytes.

large
------

The `large` CPU has 4 16-bit registers, `%ax`, `%cx`, `%dx` and `%bx`.
It has a stack size of 4096 bytes.


CHASSIS
=======

The variable name is `%CHASSIS`. It can be one of `corvette`, `destroyer`,
`cruiser` and `battleship`.

corvette
--------

pass

TRACKS
======

The variable name is `%TRACKS`. It can be one of `fast` or `slow`.
