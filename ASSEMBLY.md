Assembly Language
=================

The dronewars assembly language is comprised of several basic instructions that
you might be familiar with if you know x86 or similar instruction sets.

Built-In Static Variables
-------------------------

Variables that are capitalized and begin with an underscore like `_GLOBAL` are
built-in static variables.

`_GLOBAL`: this is the global default section, code above where any section is
defined like `.hardware`.

Data Movement Instructions
--------------------------

`mov`: copies one data item in the first operand into the second. The instruction
can move a register into a register, a literal value (number) into a register,
a literal value or register into a section of memory pointed at by a register or
literal (some v
