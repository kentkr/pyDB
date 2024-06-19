
from collections import defaultdict
import logging
import pdb
import re
import os
from typing import Any, Dict, List, Union
from .tokenizer import Token, Tokenizer

logger = logging.getLogger(__name__)

class Command:
    def __init__(self, raw_command) -> None:
        self.raw_command = raw_command

    def execute(self) -> None:
        pass
            
class CreateTableCommand(Command):
    def __init__(self, raw_command: str, tokens: List[Token]) -> None:
        super().__init__(raw_command)
        self.tokens = tokens

    def _parse_tokens(self) -> Dict:
        table_info = {}
        table_info['columns'] = []
        table_info['data'] = [[]]
        delim_counter = defaultdict(int)
        if len(self.tokens) < 1 or self.tokens[1].value != 'table':
            raise Exception(f'Expected keyword table!r after create. Instead got {self.tokens[1].value!r}')
        for token in self.tokens[2:]:
            print(token.token_type, token.value)
            # if delim count, skip parentheses
            if token.token_type == 'DELIMITER':
                delim_counter[token.value] += 1
                if token.value in ['(']:
                    continue
            # if column section (first parentheses)
            if delim_counter['('] == 1:
                if token.value == ',':
                    continue
                table_info['columns'].append(token.value)
                if delim_counter[')'] == 1:
                    continue
            # if rows (rest of parentheses)
            if delim_counter['('] > 1:
                if token.token_type == 'DELIMITER':
                             #pdb.set_trace()
                    if token.value == ',':
                        continue
                    elif token.value == ')':
                        table_info['data'].append([])
                if token.token_type == 'DELIMITER':
                    continue
                elif token.token_type in ['IDENTIFIER', 'NUMBER']:
                    table_info['data'][len(table_info['data'])-1].append(token.value)
                else:
                    raise Exception(f'Unexpected {token.token_type} of {token.value}')
        table_info['data'].pop()
        return table_info

    def execute(self) -> None:
        print(self._parse_tokens())
        pass

        
class SelectCommand(Command):
    def execute(self) -> None:
        print('select command!')
        pass

class CommandExecutor:
    def __init__(self, raw_command: str) -> None:
        self.raw_command = raw_command
        self.tokens = Tokenizer(raw_command).tokenize()
        self.command = self._get_command_executor()

    def _get_command_executor(self) -> Command:
        if self.tokens[0].value == 'create':
            return CreateTableCommand(self.raw_command, self.tokens)
        if self.tokens[0].value == 'select':
            return SelectCommand(self.raw_command)
        raise Exception('Invalid command. Must be one of create table or select')

    def execute(self) -> None:
        self.command.execute()


