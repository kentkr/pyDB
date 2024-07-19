from typing import List
from tokenizer import Token, Tokenizer
from ast_definitions import Column, Relation, SelectStatement
from code import interact

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def walk(self) -> None:
        self.position += 1
        self.current_token = self.tokens[self.position]

    def expect(self, token_type: str) -> Token:
        if self.current_token.token_type == token_type:
            token = self.current_token
            self.walk()
            return token
        else:
            raise Exception(f'Expected {token_type} got {self.current_token.token_type} of {self.current_token.value}')


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

class CreateParser(Parser):
    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def parse_relation(self) -> Relation:
        self.expect('KEYWORD')
        self.expect('IDENTIFIER')
        print(self.current_token)
        db = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        print(self.current_token)
        schema = self.expect('IDENTIFIER').value
        self.expect('DELIMITER')
        table = self.expect('IDENTIFIER').value
        return Relation(db, schema, table)

query = 'create table db.schema.table (a, b)(1, 2)'
p = CreateParser(Tokenizer(query).tokenize())
r = p.parse_relation()

interact(local=locals())


