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
    instr1 = re.compile(
        r'^(?P<instr>\w+)\s+(?P<op1>[^,;\s]+)' +
        COMMENT_SUFFIX
    )
    instr2 = re.compile(
        r'^(?P<instr>\w+)\s+(?P<op1>[^,;\s]+),\s+(?P<op2>[^;\s]+)' +
        COMMENT_SUFFIX
    )


class CodeLine(namedtuple(
    'CodeLine',
    ('syntax', 'groups', 'line_no'),
)):

    def __repr__(self):
        return f'CodeLine[{self.line_no}]({self.syntax.name}, {self.groups!r})'


def parse_code(text):
    for i, line in enumerate(text.splitlines()):
        line = line.strip()
        if not line:
            continue
        for syntax in Syntax:
            match = syntax.value.match(line)
            if match:
                yield CodeLine(
                    syntax=syntax,
                    groups=match.groupdict(),
                    line_no=i + 1,
                )
                break
        else:
            raise ParserError(f'failed to parse: {line}')


def get_sections(text):
    sections = {'_global': []}
    current = '_global'
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
