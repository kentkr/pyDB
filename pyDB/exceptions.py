
from typing import Tuple
from pyDB.tokenizer import Token

class RelationNotFound(Exception):
    pass

class UnexpectedToken(Exception):
    def __init__(self, expected_token_type: Tuple, token: Token) -> None:
        self.expected_token_type = expected_token_type
        self.token= token

    def __str__(self) -> str:
        expected = ', '.join(self.expected_token_type)
        return f'Expected value of type {expected} but got {self.token}'

class ColumnNotFound(Exception):
    pass

class InvalidCommand(Exception):
    pass
