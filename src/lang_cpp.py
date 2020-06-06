"""
 A simple lexer for C++

 Good reference: free c++ spec, consulted but not followed closely
 http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4296.pdf
"""
from sly import Lexer, Parser


class CppLexer(Lexer):
    """
        A simple lexer for C++.
        Note: Cannot handle multi-line comments
        use the comment_remover_cpp from lang_parsers_utils.py
    """
    # Set of token names.   This is always required
    tokens = {COMMENT, INCLUDE, USING,
              ID, FLOAT, NUMBER,
              PLUS, MINUS, TIMES, DIVIDE, MOD, PLUSEQ, MINUSEQ, TIMESEQ, DIVEQ,
              EQ, ASSIGN, REF, AND, OR,
              LT, LTE, GT, GTE, NOTEQ, NOT,
              SCOPE, ARROW, OUTSTREAM, INSTREAM,
              RETURN, BREAK, CONTINUE,
              IF, ELSE, FOR, WHILE, SWITCH, DO,
              STATIC, CONST, PUBLIC, PRIVATE, PROTECTED, VIRTUAL,
              QUOTED, CHARLIT,
              CASE, DEFAULT}

    literals = ['.', '"', ',', ':', ';', '(', ')', '{', '}', '[', ']']

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Other ignored patterns
    # ignore_comment = r'//.*'
    ignore_newline = r'\n+'

    USING = r'using\s+namespace'
    #INCLUDE = r'(\#include\s+<\w+>)|(\#include\s+\"(.+?)\")'
    INCLUDE = r'(\#include\s+<(.+?)>)|(\#include\s+\"(.+?)\")'
    # INCLUDE = r'\#include\s+\"(.+?)\"'

    # Regular expression rules for tokens
    QUOTED = r'\"(.+?)\"'
    CHARLIT = r'\'(.+?)\''

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['return'] = RETURN
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['switch'] = SWITCH
    ID['do'] = DO
    ID['static'] = STATIC
    ID['const'] = CONST
    ID['public'] = PUBLIC
    ID['private'] = PRIVATE
    ID['protected'] = PROTECTED
    ID['virtual'] = VIRTUAL
    ID['case'] = CASE
    ID['default'] = DEFAULT


    # MULTCOMMENT = r'/*[^*]*[*]+(?:[^/*][^*]*[*]+)*/'
    # MULTCOMMENTSTART = r'/\*'
    # MULTCOMMENTEND = r'\*/'
    # LINES = '[^*\n]+'
    COMMENT = r'//(.+?)\n'

    FLOAT = r'\d+\.\d+'
    NUMBER = r'\d+'
    PLUSEQ = r'\+='
    PLUS = r'\+'
    MINUSEQ = r'-='
    MINUS = r'-'
    TIMESEQ = r'\*='
    TIMES = r'\*'
    DIVEQ = r'/='
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='

    OR = r'\|\|'
    AND = r'&&'
    REF = r'&'

    OUTSTREAM = '<<'
    INSTREAM = '>>'

    LT = r'<'
    LTE = r'<='

    GT = r'>'
    GTE = r'>='
    NOTEQ = r'!='
    NOT = r'!'

    SCOPE = r'::'

    MOD = r'%'

    ARROW = r'->'


class CppParser(Parser):
    debugfile = "parser.out"
    tokens = CppLexer.tokens

    # precedence = (
    #     ('left', PLUS, MINUS),
    #     ('left', TIMES, DIVIDE),
    #     ('left', AND, OR),
    # )

    @_('include_statement',
       'labeled_statement',
       'expression_statement',
       'compound_statement',
       'selection_statement',
       'iteration_statement',
       'jump_statement',
       'declaration_statement',
       'try_catch_statement')
    def statement(self, p):
        print('statement')
        return 'statement', p

    # ********** include_statement **********
    @_('INCLUDE')
    def include_statement(self, p):
        print('include', p)
        return 'include', p.INCLUDE

    # ********** labeled_statement **********
    @_('identifier ":" statement')
    def labeled_statement(self, p):
        pass

    @_('CASE constant_expr ":" statement')
    def labeled_statement(self, p):
        pass

    @_('DEFAULT ":" statement')
    def labeled_statement(self, p):
        pass

    # ********** expr_statement **********
    @_('expression ";"')
    def expression_statement(self, p):
        print('expression_statement', p.expr)
        return 'expression_statement', p.expr

    @_('empty ";"')
    def expression_statement(self, p):
        print('expression_statement', p.expr)
        return 'expression_statement', p.expr

    # ********** compound_statement **********
    @_('"{" statement_seq "}"')
    def compound_statement(self, p):
        print('compound statement (block)', p.statement_seq)
        return 'compound statement (block)', p.statement_seq

    # ********** statement_seq **********
    @_('statement')
    def statement_seq(self, p):
        pass

    @_('statement_seq statement')
    def statement_seq(self, p):
        pass

    # ********** selection_statement **********
    @_('IF "(" condition ")" statement ')
    def selection_statement
        print('selection_statement IF1', p.condition, p.statement)
        return 'selection_statement IF1', p.condition, p.statement

    @_('IF "(" condition ")" statement ELSE statement')
    def selection_statement
        print('selection_statement IF2', p.condition, p.statement0, p.statement1)
        return 'selection_statement IF2', p.condition, p.statement0, p.statement1

    @_('SWITCH "(" condition ")" statement')
    def selection_statement
        print('selection_statement IF2', p.condition, p.statement)
        return 'selection_statement IF2', p.condition, p.statement

    # ********** condition **********
    @_('expression')
    def condition(self, p):
        print('condition', p.expr)
        return 'condition', p.expr

    # ********** iteration_statement **********
    @_('WHILE "(" condition ")" statement ')
    def iteration_statement(self, p):
        print('iteration_statement WHILE', p.condition, p.statement)
        return 'iteration_statement WHILE', p.condition, p.statement

    @_('DO statement WHILE "(" expr ")" ";" ')
    def iteration_statement(self, p):
        print('iteration_statement DO WHILE', p.condition, p.statement)
        return 'iteration_statement DO WHILE', p.condition, p.statement

    @_('FOR "(" for_init_statement condition ";" expression ")" statement')
    def iteration_statement(self, p):
        print('iteration_statement FOR', p.condition, p.statement)
        return 'iteration_statement FOR', p.condition, p.statement

    @_('FOR "(" for_init_statement empty ";" empty ")" statement')
    def iteration_statement(self, p):
        print('iteration_statement FOR empty', p.statement)
        return 'iteration_statement FOR empty' p.statement

    # ********** for_init_statement **********
    @_('expression_statement')
    def for_init_statement(self, p):
        pass

    @_('simple_declaration')
    def for_init_statement(self, p):
        pass

    # ********** jump_statement **********
    @_('BREAK ";"')
    def jump_statement(self, p):
        print('break')
        return 'break'

    @_('CONTINUE ";"')
    def jump_statement(self, p):
        print('continue')
        return 'continue'

    @_('RETURN expression ";"')
    def jump_statement(self, p):
        print('RETURN', p.expression)
        return 'RETURN', p.expression

    @_('RETURN empty ";"')
    def jump_statement(self, p):
        print('RETURN')
        return 'RETURN'

    # ********** declaration_statement ***********
    @_('block_declaration')
    def declaration_statement(self, p):
        pass

    # TODO
    '''
    block_declaration
    
    try_catch_statement
    
    expression
    simple_declaration
    
    
    '''

    # ********** Empty production **********
    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        if p:
            print(">>>>>>>>>>")
            print("Syntax error at token:", p.value)
            print(p)
            print(p.type)
            print(p.index)
            print(p.value)
            print(p.lineno)
            # Just discard the token and tell the parser it's okay.
            for i in range(10):
                print(i, "NEXT TOK->", next(self.tokens, None))
            # input(">>:")
            print("<<<<<<<<<<")
            #self.errok()
        else:
            print("Syntax error at EOF")

        # raise for testing grammar
        raise RuntimeError
