import pdb
from typing import Any, Dict, List
from tokenizer import Tokenizer, Token
from code import interact

class Tokens(Tokenizer):
    def __init__(self, command: str) -> None:
        super().__init__(command)
        self.tokens = self.tokenize()
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def walk(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos]

class ASTNode:
    def __str__(self) -> str:
        # get class name
        s = f'{type(self).__name__}('
        # formatting to represent key values as repr
        f = '{k}: {v!r}'
        c = 0 # count iterations for commas
        for k, v in self.__dict__.items():
            s += f.format(k=k, v=v)
            c += 1
            if c < len(self.__dict__.items()):
                s += ', '
        s += ')'
        return s

    def __repr__(self) -> str:
        # get class name
        s = f'{type(self).__name__}('
        # formatting to represent key values as repr
        f = '{k}: {v!r}'
        c = 0 # count iterations for commas
        for k, v in self.__dict__.items():
            s += f.format(k=k, v=v)
            c += 1
            if c < len(self.__dict__.items()):
                s += ', '
        s += ')'
        return s

class Column(ASTNode):
    def __init__(self, name):
        self.name = name

class Relation(ASTNode):
    def __init__(self, db, schema, table):
        self.db = db
        self.schema = schema
        self.table = table

class SelectStatement(ASTNode):
    def __init__(self, columns: List[Column], relation: Relation) -> None:
        super().__init__()
        self.columns = columns
        self.relation = relation


class Parser:
    def __init__(self, tokens: Tokens) -> None:
        self.tokens = tokens

    def expect(self, token_type: str) -> Token:
        if self.tokens.current_token.token_type == token_type:
            token = self.tokens.current_token
            self.tokens.walk()
            return token
        else:
            raise Exception(f'Expected {token_type} got {self.tokens.current_token.token_type}')

    def parse_column(self) -> Column:
        token = self.expect('IDENTIFIER')
        return Column(token.value)

    def parse_column_list(self) -> List[Column]:
        cols = [self.parse_column()]
        print(self.tokens.pos)
        while self.tokens.pos < len(self.tokens.tokens) and self.tokens.current_token.token_type == 'DELIMITER':
            print(self.tokens.pos)
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


query = 'select col1, col2 from db.table.schema;'

t = Tokens(query)
p = Parser(t)
print(p.parse_select_statement())

interact(local=locals())


# bro break out the fucking white board and work
# through an example. Keep it simple you can figure it out
