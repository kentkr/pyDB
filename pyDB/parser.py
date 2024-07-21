from typing import List

from pyDB.exceptions import UnexpectedToken
from pyDB.tokenizer import Token
from pyDB.ast_definitions import Column, Relation, SelectStatement, Row, CreateTableStatement

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def walk(self) -> None:
        self.position += 1
        self.current_token = self.tokens[self.position]

    def expect(self, *token_type: str) -> Token:
        if self.current_token.token_type in token_type:
            token = self.current_token
            self.walk()
            return token
        else:
            raise UnexpectedToken(token_type, self.current_token)


class SelectParser(Parser):
    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def parse_column(self) -> Column:
        token = self.expect('IDENTIFIER')
        return Column(token.value)

    def parse_column_list(self) -> List[Column]:
        cols = [self.parse_column()]
        while self.position < len(self.tokens) and self.current_token.token_type == 'DELIMITER':
            self.expect('DELIMITER')
            cols.append(self.parse_column())
        return cols

    def parse_relation(self) -> Relation:
        db = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        schema = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        table = self.expect('IDENTIFIER').value
        return Relation(db, schema, table)

    def parse_select_statement(self) -> SelectStatement:
        # select
        self.expect('KEYWORD')
        col_list = self.parse_column_list()
        # from
        self.expect('KEYWORD')
        relation = self.parse_relation()
        return SelectStatement(col_list, relation)

class CreateTableParser(Parser):
    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def parse_relation(self) -> Relation:
        self.expect('KEYWORD') # create
        self.expect('IDENTIFIER') # table
        db = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        schema = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        table = self.expect('IDENTIFIER').value
        return Relation(db, schema, table)

    def parse_column_list(self) -> List[Column]:
        self.expect('ENCLOSURE')
        column_list = []
        column_list.append(Column(self.expect('IDENTIFIER').value))
        while self.current_token.token_type == 'DELIMITER':
            self.expect('DELIMITER')
            column_list.append(Column(self.expect('IDENTIFIER').value))
        self.expect('ENCLOSURE')
        return column_list

    def parse_row(self) -> Row:
        self.expect('ENCLOSURE')
        row = []
        row.append(self.expect('STRING', 'NUMBER').value)
        while self.current_token.token_type == 'DELIMITER':
            self.expect('DELIMITER')
            row.append(self.expect('STRING', 'NUMBER').value)
        self.expect('ENCLOSURE')
        return Row(row)

    def parse_create_table(self) -> CreateTableStatement:
        relation = self.parse_relation()
        column_list = self.parse_column_list()
        rows = []
        while self.current_token.token_type != 'EOF' and self.current_token.token_type == 'ENCLOSURE':
            rows.append(self.parse_row())
        return CreateTableStatement(relation, column_list, rows)

