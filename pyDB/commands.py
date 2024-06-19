
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

    def _get_table_info(self) -> Dict:
        table_info = {}
        table_info['columns'] = []
        table_info['rows'] = []
        # verify create table command
        if len(self.tokens) < 1 or self.tokens[1].value != 'table':
            raise Exception(f'Expected keyword table!r after create. Instead got {self.tokens[1].value!r}')
        # get relation 
        for i, token in enumerate(self.tokens[2:7]):
            if i == 0:
                table_info['db'] = token.value
            if i == 2:
                table_info['schema'] = token.value
            if i == 4:
                table_info['table'] = token.value
        table_info['path'] = os.path.join(os.getcwd(), 'data', table_info['db'], table_info['schema'], table_info['table'])
        # get cols and data
        row_count = 0
        col_count = 0
        new_data = []
        for token in self.tokens[7:]:
            #pdb.set_trace()
            if token.value == '(':
                row_count += 1
                continue
            elif token.value == ',':
                col_count += 1
                continue
            elif token.value == ')':
                if row_count == 1:
                    table_info['columns'] = new_data
                    new_data = []
                elif row_count > 1:
                    table_info['rows'].append(new_data)
                    new_data = []
                continue
            new_data.append(token.value)
        return table_info

    def execute(self) -> None:
        table_info = self._get_table_info()
        with open(table_info['path'], 'w') as file:
            for i, col in enumerate(table_info['columns']):
                file.write(col)
                if i < len(table_info['columns'])-1:
                    file.write('|')
            file.write('\n')
            for row in table_info['rows']:
                for i, value in enumerate(row):
                    file.write(str(value))
                    if i < len(row)-1:
                        file.write('|')
                file.write('\n')

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


