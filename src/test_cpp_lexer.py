"""
    Tests for CppLexer
"""
import unittest
import sly
from lang_cpp import CppLexer
from lang_parsers_utils import comment_remover_cpp


class TestCppLexer(unittest.TestCase):
    def test_simple_lex(self):
        """
        Test that it can lex a simple program
        """
        lexer = CppLexer()
        data = """
        #include <iostream>
        int i = 0;
        """
        tokens = list(lexer.tokenize(data))
        # for token in tokens:
        #     print(token)
        self.assertEqual(len(tokens), 6)

    def test_simple_lex_error(self):
        """
        Test that it can fail on improper syntax
        """
        lexer = CppLexer()
        data = """
        #include <iostream!
        int i = 0;
        """
        with self.assertRaises(sly.lex.LexError):
            tokens = list(lexer.tokenize(data))

    def test_program_lex(self):
        """
        Test that it can lex a small simple program.
        """
        lexer = CppLexer()
        with open('../data/cpp/main_test.cpp') as f:
            data = f.read()

        data = comment_remover_cpp(data)
        tokens = list(lexer.tokenize(data))
        # for token in tokens:
        #     print(token)
        self.assertEqual(len(tokens), 38)

    def test_program_lex_fail(self):
        """
            test that the program fails on a program with an error.
        """
        lexer = CppLexer()
        with open('../data/cpp/main_test.cpp') as f:
            data = f.read()

        data = comment_remover_cpp(data)
        data = data.replace(';', '#')

        with self.assertRaises(sly.lex.LexError):
            tokens = list(lexer.tokenize(data))
            # for token in tokens:
            #     print(token)

    def test_sdl_prog_lex(self):
        lexer = CppLexer()
        with open('../data/cpp/sdl_hello_world_main.cpp') as f:
            data = f.read()
            data = comment_remover_cpp(data)
            tokens = list(lexer.tokenize(data))
            # for token in tokens:
            #     print(token)
            self.assertEqual(len(tokens), 157)


if __name__ == '__main__':
    unittest.main()
