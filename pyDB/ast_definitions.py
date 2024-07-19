

from typing import List

class ASTNode:
    def __str__(self) -> str:
        # get class name
        output = f'{type(self).__name__}('
        # formatting to represent key values as repr
        key_value_formatter = '{key}: {value!r}'
        count = 0 # count iterations for commas
        for key, value in self.__dict__.items():
            output += key_value_formatter.format(key=key, value=value)
            count += 1
            if count < len(self.__dict__.items()):
                output += ', '
        output += ')'
        return output

    def __repr__(self) -> str:
        return self.__str__()

class Column(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

class Relation(ASTNode):
    def __init__(self, db: str, schema: str, table: str) -> None:
        self.db = db
        self.schema = schema
        self.table = table

class SelectStatement(ASTNode):
    def __init__(self, columns: List[Column], relation: Relation) -> None:
        super().__init__()
        self.columns = columns
        self.relation = relation

