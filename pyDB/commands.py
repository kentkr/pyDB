
import logging
import os
from typing import Iterable, List

from pyDB.ast_definitions import Column, Relation
from .tokenizer import Token, Tokenizer
from .parser import SelectParser, CreateTableParser

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
        self.create_table_statement = CreateTableParser(tokens).parse_create_table()

    def _get_table_path(self) -> str:
        relation = self.create_table_statement.relation
        return os.path.join('/Users/kylekent/Desktop/pyDB/data', relation.db, relation.schema, relation.table)

    def execute(self) -> None:
        path = self._get_table_path()
        columns = self.create_table_statement.column_list
        rows = self.create_table_statement.rows
        with open(path, 'w') as file:
            for i, col in enumerate(columns):
                file.write(col.name)
                if i < len(columns)-1:
                    file.write('|')
            file.write('\n')
            for row in rows:
                for i, value in enumerate(row.values):
                    file.write(str(value))
                    if i < len(row.values)-1:
                        file.write('|')
                file.write('\n')

class SelectCommand(Command):
    def __init__(self, raw_command: str, tokens: List[Token]) -> None:
        super().__init__(raw_command)
        self.tokens = tokens
        self.selected_statement = SelectParser(tokens).parse_select_statement()

    @staticmethod
    def _read_data(relation: Relation, columns: List[Column]) -> List:
        path = os.path.join(os.getcwd(), 'data', relation.db, relation.schema, relation.table)
        column_names = [col.name for col in columns]
        data = [column_names]
        with open(path, 'r') as file:
            lines = file.readlines()
            data_columns = lines[0].strip().split('|')
            for col in column_names:
                if col not in data_columns:
                    raise Exception(f'Column {col} not found in data')
            col_indices = [i for i, col in enumerate(data_columns) if col in column_names]
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
        relation = self.selected_statement.relation
        columns = self.selected_statement.columns
        data = self._read_data(relation, columns)
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


