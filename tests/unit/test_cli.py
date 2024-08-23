
import pytest
from pyDB.cli import Input
from unittest.mock import patch, MagicMock

def test_load_history() -> None:
    # patch readline and see if it's called
    with patch('readline.read_history_file') as mock_read_history_file:
        input_instance = Input()
        mock_read_history_file.assert_called_with('history.txt')

def test_save_history() -> None:
    with patch('readline.write_history_file') as mock_write_history_file:
        input_instance = Input()
        input_instance.save_history()
        mock_write_history_file.assert_called_with('history.txt')

