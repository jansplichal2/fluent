import unittest
from fluent_ast import LetStmt, SimpleType, ListType
from parser import Parser


class TestParsedTypeAnnotations(unittest.TestCase):
    def parse_let_type(self, src: str):
        parser = Parser(src)
        stmt = parser.parse()[0]
        assert isinstance(stmt, LetStmt)
        return stmt.type_annotation

    def test_bool_type(self):
        typ = self.parse_let_type("let b: Bool = true")
        self.assertEqual(typ, SimpleType("Bool"))

    def test_list_of_int(self):
        typ = self.parse_let_type("let xs: List[Int] = [1, 2, 3]")
        self.assertEqual(typ, ListType(SimpleType("Int")))

    def test_nested_list(self):
        typ = self.parse_let_type("let tbl: List[List[String]] = []")
        self.assertEqual(
            typ,
            ListType(ListType(SimpleType("String")))
        )


if __name__ == "__main__":
    unittest.main()
