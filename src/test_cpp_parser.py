"""
    Tests for CppParser
"""
import unittest
import sly
from lang_cpp import CppLexer, CppParser
from lang_parsers_utils import comment_remover_cpp


class TestCppParser(unittest.TestCase):
    def parse_file(self, filename):
        lexer = CppLexer()
        parser = CppParser()
        data_file = filename

        with open(data_file) as f:
            data = f.read()
            data = comment_remover_cpp(data)
            tokens = lexer.tokenize(data)
            outputs = parser.parse(tokens)

    def ztest_parse_array_prog(self):
        print('##### Array #####')
        data_file = '../data/cpp/array_file_main.cpp'
        self.parse_file(data_file)

    def ztest_parse_chaos_prog(self):
        print('##### chaos #####')
        data_file = '../data/cpp/chaos_main.cpp'
        self.parse_file(data_file)

    def ztest_parse_cout(self):
        print('##### Simple Cout test #####')
        data_file = '../data/cpp/cout_test.cpp'
        self.parse_file(data_file)

    def test_parse_game(self):
        print('##### Pokemon Game test #####')
        data_file = '../data/cpp/game_main.cpp'
        self.parse_file(data_file)

    def ztest_parse_simple_prog(self):
        print('##### Simple Prog #####')
        data_file = '../data/cpp/main_test.cpp'
        self.parse_file(data_file)

    def ztest_parse_sdl_prog(self):
        print('##### SDL prog #####')
        data_file = '../data/cpp/sdl_hello_world_main.cpp'
        self.parse_file(data_file)









if __name__ == '__main__':
    unittest.main()