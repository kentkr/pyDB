from pyDB.ast_definitions import Column, CreateTableStatement, Relation, Row, SelectStatement
import pytest

def test_column():
    col = Column(name='col')
    assert col.name == 'col'

def test_rows():
    row = Row([0, 1, 2])
    assert hasattr(row, 'values')

def test_relation():
    rel = Relation('db', 'schema', 'table')
    assert all([rel.db == 'db', rel.schema == 'schema', rel.table == 'table'])

class TestSelectStatement:
    @pytest.fixture(autouse=True)
    def init(self):
        # This method will run before each test method.
        self.statement = SelectStatement([Column('a'), Column('b')], Relation('db', 'schema', 'table'))

    def test_columns(self):
        assert hasattr(self.statement, 'columns')

    def test_relation(self):
        assert hasattr(self.statement, 'relation')

class TestCreateTableStatement:
    @pytest.fixture(autouse=True)
    def init(self):
        # This method will run before each test method.
        col = [Column('a'), Column('b')]
        rel = Relation('db', 'schema', 'table')
        rows = [Row([0, 1])]
        self.statement = CreateTableStatement(rel, col, rows)

    def test_attrs(self):
        has_rel = hasattr(self.statement, 'relation')
        has_col = hasattr(self.statement, 'column_list')
        has_rows = hasattr(self.statement, 'rows')
        assert all([has_rel, has_col, has_rows])

