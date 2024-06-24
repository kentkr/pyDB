
from collections import defaultdict
import logging
import pdb
import re
import os
from typing import Any, Dict, Iterable, List, Union
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
        data_tokens = self.tokens[7:]
        for i, token in enumerate(data_tokens):
            #pdb.set_trace()
            # first token of new row, skip
            if token.value == '(':
                row_count += 1
                continue
            # row delim, skip
            elif token.value == ',':
                # first value null or last value null
                if data_tokens[i-1].value in ['(', ',']:
                    new_data.append(None)
                continue
            # end of row, create col or append rows, clear data
            elif token.value == ')':
                if row_count == 1:
                    table_info['columns'] = new_data
                    new_data = []
                elif row_count > 1:
                    if data_tokens[i-1].value == ',':
                        new_data.append(None)
                    table_info['rows'].append(new_data)
                    new_data = []
                continue
            # actual value, append to new data
            else:
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
    def __init__(self, raw_command: str, tokens: List) -> None:
        super().__init__(raw_command)
        self.tokens = tokens

    def _parse_command(self):
        columns = []
        relation = []
        current_keyword = 'select'
        for token in self.tokens[1:]:
            if token.token_type == 'DELIMITER':
                continue
            if token.token_type == 'KEYWORD':
                current_keyword = token.value
                continue
            if current_keyword == 'select':
                columns.append(token.value)
            if current_keyword == 'from':
                relation.append(token.value)
        return [relation, columns]

    @staticmethod
    def _read_data(relation: List[str], selected_columns: List[str]) -> List:
        path = os.path.join(os.getcwd(), 'data', relation[0], relation[1], relation[2])
        data = [selected_columns]
        with open(path, 'r') as file:
            lines = file.readlines()
            columns = lines[0].strip().split('|')
            col_indices = [i for i, col in enumerate(columns) if col in selected_columns]
            for line in lines[1:]:
                split_line = line.strip().split('|')
                data.append([split_line[i] for i in col_indices])
        return data

    def _pretty_print_result(self, data: List[List[object]]):
        col_widths = []
        # zip lists to traverse columns not rows
        for col in zip(*data):
            max_value = 0
            for item in col:
                max_value = max(max_value, len(str(item)))
            col_widths.append(max_value)
        
        # using widths create row with values
        def construct_row(items: Iterable):
            return '| ' + ' | '.join(f'{str(item).ljust(width)}' for item, width in zip(items, col_widths)) + ' |'

        # using widths create row '+' and '-'
        border = '+-' + '-+-'.join('-' * width for width in col_widths) + '-+'

        print(border)
        print(construct_row(data[0]))
        print(border)
        for row in data[1:]:
            print(construct_row(row))
        print(border)
        
    def execute(self) -> None:
        relation, selected_columns = self._parse_command()
        data = self._read_data(relation, selected_columns)
        self._pretty_print_result(data)


class CommandExecutor:
    def __init__(self, raw_command: str) -> None:
        self.raw_command = raw_command
        self.tokens = Tokenizer(raw_command).tokenize()
        self.command = self._get_command_executor()

    def _get_command_executor(self) -> Command:
        if self.tokens[0].value == 'create':
            return CreateTableCommand(self.raw_command, self.tokens)
        if self.tokens[0].value == 'select':
            return SelectCommand(self.raw_command, self.tokens)
        raise Exception('Invalid command. Must be one of create table or select')

    def execute(self) -> None:
        self.command.execute()


