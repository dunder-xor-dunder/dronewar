import re
from enum import Enum
from collections import namedtuple


class ParserError(ValueError):
    pass


COMMENT_SUFFIX = r'(?:\s*;(?P<comment>.*))?$'


class Syntax(Enum):
    comment = re.compile(
        r'^;(?P<comment>.*)$'
    )
    label = re.compile(
        r'^(?P<label>\w+):' +
        COMMENT_SUFFIX
    )
    section = re.compile(
        r'^\.(?P<name>\w+)' +
        COMMENT_SUFFIX
    )
    var_def = re.compile(
        r'^%(?P<id>\w+)\s+(?P<val>\S+)' +
        COMMENT_SUFFIX
    )
    instr = re.compile(
        r'^(?P<instr>\w+)\s*(?P<rest>[^;]*)' +
        COMMENT_SUFFIX
    )


class InstrDef:
    __slots__ = ('name', 'num_ops')

    def __init__(self, name, num_ops):
        self.name = name
        self.num_ops = num_ops


class InstrType(Enum):
    """
    reference: https://www.cs.virginia.edu/~evans/cs216/guides/x86.html
    """
    INT = InstrDef('int', 1)
    MOV = InstrDef('mov', 2)
    PUSH = InstrDef('push', 1)
    POP = InstrDef('pop', 1)
    LEA = InstrDef('lea', 2)
    ADD = InstrDef('add', 2)
    SUB = InstrDef('sub', 2)
    INC = InstrDef('inc', 1)
    DEC = InstrDef('dec', 1)
    MUL = InstrDef('mul', 2)
    DIV = InstrDef('div', 2)
    AND = InstrDef('and', 2)
    OR = InstrDef('or', 2)
    XOR = InstrDef('xor', 2)
    NOT = InstrDef('not', 1)
    SHL = InstrDef('shl', 2)
    SHR = InstrDef('shr', 2)
    CMP = InstrDef('cmp', 1)
    JMP = InstrDef('jmp', 1)
    JE = InstrDef('je', 1)
    JNE = InstrDef('jne', 1)
    JZ = InstrDef('jz', 1)
    JG = InstrDef('jg', 1)
    JGE = InstrDef('jge', 1)
    JL = InstrDef('jl', 1)
    JLE = InstrDef('jle', 1)
    CALL = InstrDef('call', 1)
    RET = InstrDef('ret', 1)
    SWP = InstrDef('swp', 2)

    @classmethod
    def get(cls, reg):
        try:
            return cls[reg.upper()]
        except KeyError:
            return None

    def __str__(self):
        return self.name


class Instr(namedtuple(
    'Instr',
    ('instr', 'type', 'ops'),
)):

    def __str__(self):
        return f'{self.instr} {", ".join(self.ops)}'

    def __repr__(self):
        return f'Instr[{self.instr}]({", ".join(self.ops)})'

    @classmethod
    def parse(cls, name, rest):
        name = name.lower()
        instr_type = InstrType.get(name)
        if instr_type is None:
            raise ParserError(f'{name} is not a valid instruction')
        csv = [
            x.strip()
            for x in rest.split(',')
        ]
        ops = csv
        return cls(
            instr=name,
            type=instr_type,
            ops=ops,
        )


class CodeLine(namedtuple(
    'CodeLine',
    ('syntax', 'groups', 'line_no', 'instr'),
)):

    def __repr__(self):
        return (
            f'CodeLine[{self.line_no}]('
            f'type={self.syntax.name}, '
            f'groups={self.groups!r}, '
            f'instr={self.instr!r}'
            ')'
        )

    @classmethod
    def parse_instr(cls, *, syntax, groups, line_no):
        instr = Instr.parse(groups['instr'], groups['rest'])
        return cls(
            syntax=syntax,
            groups=groups,
            line_no=line_no,
            instr=instr,
        )


def parse_code(text):
    for i, line in enumerate(text.splitlines()):
        line = line.strip()
        if not line:
            continue
        for syntax in Syntax:
            match = syntax.value.match(line)
            if match:
                if syntax is Syntax.instr:
                    yield CodeLine.parse_instr(
                        syntax=syntax,
                        groups=match.groupdict(),
                        line_no=i + 1,
                    )
                else:
                    yield CodeLine(
                        syntax=syntax,
                        groups=match.groupdict(),
                        line_no=i + 1,
                        instr=None,
                    )
                break
        else:
            raise ParserError(f'failed to parse: {line}')


def get_sections(text):
    sections = {'_GLOBAL': []}
    current = '_GLOBAL'
    for code in parse_code(text):
        if code.syntax is Syntax.section:
            current = code.groups['name']
            sections[current] = []
            continue
        sections[current].append(code)
    for name, section in sections.items():
        print(f'SECTION {name}')
        for codeline in section:
            print(f'  {codeline!r}')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    with open(args.path) as f:
        code = f.read()
    get_sections(code)


if __name__ == '__main__':
    main()
