
from unittest.mock import mock_open, patch
from pyDB.commands import CreateTableCommand
from pyDB.tokenizer import Tokenizer
import pytest
import os

class TestCreatetableCommand:
    @pytest.fixture(autouse=True)
    def init(self):
        self.raw_command = 'create table db.schema.table (a, b)(1,2)("hi", "there");'
        self.tokens = Tokenizer(self.raw_command).tokenize()
        self.command = CreateTableCommand(self.raw_command, self.tokens)

    def test__get_table_path(self) -> None:
        path = self.command._get_table_path()
        assert path == os.path.abspath(os.path.join(__file__, '..', '..', '..', 'data', 'db', 'schema', 'table'))

    @patch('builtins.open', new_callable=mock_open)
    def test_execute(self, mock_open):
        columns = self.command.create_table_statement.column_list
        rows = self.command.create_table_statement.rows
        self.command.execute()
        column_write_calls = len(columns) + (len(columns))
        row_write_calls = len(rows) * len(columns) + (len(rows) * (len(columns) - 1)) + len(rows)
        assert mock_open().write.call_count, column_write_calls+row_write_calls
        


