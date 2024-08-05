
from pyDB.tokenizer import Token, Tokenizer
import pytest

token_list = [
    ('IDENTIFIER', 'hi'), 
    ('NUMBER', 9),
]
@pytest.mark.parametrize('token_type,value', token_list)
def test_Token(token_type, value) -> None:
    token = Token(token_type=token_type, value=value)
    assert hasattr(token, 'token_type')
    assert hasattr(token, 'value')

# not testing NEWLINE or SKIP since they aren't supported yet
token_matches = [
    ('9', 'NUMBER'),
    ('"hi"', 'STRING'),
    ('bazinga', 'IDENTIFIER'),
    ('from', 'KEYWORD'),
    (',', 'DELIMITER'),
    ('(', 'ENCLOSURE'),
    #('\n', 'NEWLINE'),
    #('\t', 'SKIP'),
    (';', 'EOF'),
]
@pytest.mark.parametrize('input,token_type', token_matches)
def test_token_matches(input, token_type) -> None:
    tokens = Tokenizer(input).tokenize()
    assert tokens
    assert tokens[0].token_type == token_type


token_lens = [
    ('select a from a.b.c;', 9),
    ('select 1', 2),
]
@pytest.mark.parametrize('input,length', token_lens)
def test_token_len(input, length) -> None:
    tokens = Tokenizer(input).tokenize()
    assert len(tokens) == length

