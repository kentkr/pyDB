
class Parser:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokens = tokenizer.tokenize()
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
            raise Exception(f'Expected {token_type} got {self.current_token.token_type}')

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


query = 'select col1, col2 from db.table.schema;'

t = Tokenizer(query)
p = Parser(t)
print(p.parse_select_statement())

interact(local=locals())


# bro break out the fucking white board and work
# through an example. Keep it simple you can figure it out
