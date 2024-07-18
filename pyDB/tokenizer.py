
from code import interact
import re
from typing import List, Tuple, Union
from dataclasses import dataclass

KEYWORDS = {'select', 'from'}
DELIMITERS = {',', '.'}
EOF = ';'
ENCLOSURES = {'(', ')', '\'', '\"'}

_token_specification = [
        ('NUMBER',    r'\d+(\.\d*)?'),
        ('IDENTIFIER', r'[A-Za-z_]\w*'),
        ('DELIMITER', r'|'.join(re.escape(delim) for delim in DELIMITERS)),
        ('ENCLOSURE', r'|'.join(re.escape(e) for e in ENCLOSURES)),
        ('NEWLINE',   r'\n'),           # Line endings
        ('SKIP',      r'[ \t]+'),       # Skip over spaces and tabs
        ('EOF',  EOF),
        ('MISMATCH',  r'.'),
        ]

_token_regex = r'|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in _token_specification)
_compiled_regex = re.compile(_token_regex)

@dataclass
class Token:
    token_type: Union[str, None]
    value: Union[str, int, float]

class Tokenizer:
    def __init__(self, command: str) -> None:
        self.command = command

    def tokenize(self) -> List[Token]:
        line_num = 1
        #line_start = 0
        tokens = []
        for matched_objects in _compiled_regex.finditer(self.command):
            token_type = matched_objects.lastgroup
            #value = matched_objects.group(token_type)
            value = matched_objects.group()
            if token_type == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif token_type == 'IDENTIFIER' and value in KEYWORDS:
                token_type = 'KEYWORD'
            elif token_type == 'NEWLINE':
                #line_start = matched_objects.end()
                line_num += 1
                continue
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            tokens.append(Token(token_type=token_type, value=value))
        return tokens


