
from pyDB.parser import Parser, SelectParser, CreateTableParser
from pyDB.tokenizer import Tokenizer
import pytest

class TestBaseParser:
    @pytest.fixture(autouse=True)
    def init(self) -> None:
        self.input = 'select a from db.schema.table'
        self.tokens = Tokenizer(self.input).tokenize()
        self.parser = Parser(self.tokens)

    def test_init(self) -> None:
        assert all([self.parser.position == 0, self.parser.current_token.value == 'select'])

    def test_walk(self) -> None:
        self.parser.walk()
        assert all([self.parser.position == 1, self.parser.current_token.value == 'a'])

    def test_valid_expect(self) -> None:
        self.parser.expect('KEYWORD')
        assert all([self.parser.position == 1, self.parser.current_token.value == 'a'])


class TestSelectParser:
    @pytest.fixture(autouse=True)
    def init(self) -> None:
        self.input = 'select a from db.schema.table;'
        self.tokens = Tokenizer(self.input).tokenize()
        self.parser = SelectParser(self.tokens)

    def test_parse_column(self) -> None:
        self.parser.expect('KEYWORD')
        column = self.parser.parse_column()
        assert type(column).__name__ == 'Column'
        assert hasattr(column, 'name')
        assert column.name == 'a'

    def test_parse_column_list(self) -> None:
        self.parser.expect('KEYWORD')
        columns = self.parser.parse_column_list()
        assert type(columns).__name__ == 'list'

    def test_parse_relation(self) -> None:
        self.parser.expect('KEYWORD')
        columns = self.parser.parse_column_list()
        self.parser.expect('KEYWORD')
        print(self.parser.__dict__)
        relation = self.parser.parse_relation()
        assert type(relation).__name__ == 'Relation'
        assert relation.db == 'db'
        assert relation.schema == 'schema'
        assert relation.table == 'table'

class TestCreateTableParser:
    @pytest.fixture(autouse=True)
    def init(self) -> None:
        self.input = 'create table db.schema.table (a, b)(1,2)("hi", "there");'
        self.tokens = Tokenizer(self.input).tokenize()
        self.parser = CreateTableParser(self.tokens)

    def test_parse_relation(self) -> None:
        relation = self.parser.parse_relation()
        assert type(relation).__name__ == 'Relation'
        assert relation.db == 'db'
        assert relation.schema == 'schema'
        assert relation.table == 'table'

    def test_parse_column_list(self) -> None:
        relation = self.parser.parse_relation()
        column_list = self.parser.parse_column_list()
        assert type(column_list).__name__ == 'list'
        assert len(column_list) == 2
        assert type(column_list[0]).__name__ == 'Column'
        assert column_list[0].name == 'a'

    def test_parse_row(self) -> None:
        relation = self.parser.parse_relation()
        column_list = self.parser.parse_column_list()
        row = self.parser.parse_row()
        assert type(row).__name__ == 'Row'
        assert len(row.values) == 2

    def test_parse_create_table(self) -> None:
        create_table = self.parser.parse_create_table()
        assert type(create_table).__name__ == 'CreateTableStatement'
