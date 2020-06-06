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
              LPAREN, RPAREN, LBRACE, RBRACE, LSQBRACE, RSQBRACE,
              LT, LTE, GT, GTE, NOTEQ, NOT,
              SCOPE, ARROW, OUTSTREAM, INSTREAM,
              RETURN, IF, ELSE, FOR, WHILE, SWITCH, DO,
              STATIC, CONST, PUBLIC, PRIVATE, PROTECTED, VIRTUAL,
              QUOTED, CHARLIT}

    literals = ['.', '"', ',', ':', ';']

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
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LSQBRACE = r'\['
    RSQBRACE = r'\]'

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

    @_('statements statement',
       'statement')
    def statements(self, p):
        # print('statements')
        pass

    @_('comment',
       'include',
       'using',
       'funcdec',
       'forloop',
       'whileloop',
       'ifstatement',
       'expr ";"',
       'returnstatement')
    def statement(self, p):
        print('statement')
        pass

    @_('COMMENT')
    def comment(self, p):
        # print('comment')
        pass

    @_('INCLUDE')
    def include(self, p):
        # print('stmt include:', p.INCLUDE)
        pass

    @_('USING ID ";"')
    def using(self, p):
        # print('stmt using:', p.ID)
        pass

    @_('')
    def empty(self, p):
        pass

    @_('RETURN val_expr ";"')
    def returnstatement(self, p):
        #print("return statement")
        pass

    @_('IF LPAREN val_expr RPAREN block')
    def ifstatement(self, p):
        print("if statement block")
        pass

    # @_('IF LPAREN cond_expr RPAREN statement')
    # def ifstatement(self, p):
    #     print("if statement not bracket {BAD}")
    #     pass
    #
    # @_('IF LPAREN cond_expr RPAREN block ELSE block')
    # def ifstatement(self, p):
    #     print("if-else statement blocks")
    #     pass
    #
    # @_('IF LPAREN cond_expr RPAREN block ELSE ifstatement')
    # def ifstatement(self, p):
    #     print("if-else-if statement")
    #     pass

    @_('ID ID LPAREN paramlist RPAREN block')
    def funcdec(self, p):
        print('func declaration', p.ID1)
        pass

    @_('LBRACE statements RBRACE')
    def block(self, p):
        # print("block")
        pass

    @_('LBRACE RBRACE')
    def block(self, p):
        # print("empty block")
        pass

    @_('params',
       'empty')
    def paramlist(self, p):
        pass

    @_('ID ID')
    def param(self, p):
        # print("Parameter: type=", p.ID0, "name=", p.ID1)
        pass

    @_('ID REF ID')
    def param(self, p):
        # print("Parameter: type=", p.ID0, "name=", p.ID1)
        pass

    @_('ID ID LSQBRACE RSQBRACE')
    def param(self, p):
        # print("Parameter: type=", p.ID0, "name=", p.ID1)
        pass

    @_('params "," param',
       'param')
    def params(self, p):
        pass

    @_('WHILE LPAREN val_expr RPAREN block')
    def whileloop(self, p):
        pass

    @_('FOR LPAREN declare ";" val_expr ";" val_expr RPAREN block')
    def forloop(self, p):
        print('for loop')
        pass

    @_('ID ID')
    def declare(self, p):
        # print('declaration', "type: %s, name: %s" % (p.ID0, p.ID1))
        pass

    @_('ID ID LSQBRACE NUMBER RSQBRACE')
    def declare(self, p):
        # print('declaration', "type: %s array, name: %s[%s]" % (p.ID0, p.ID1, p.NUMBER))
        pass

    @_('decassign')
    def declare(self, p):
        # print('declaration', p.decassign)
        pass

    @_('ID ID ASSIGN val_expr')
    def decassign(self, p):
        print('declaration and assignment', "type: %s, name: %s" % (p.ID0, p.ID1))
        return "type: %s, name: %s" % (p.ID0, p.ID1)

    @_('assignment',
       'declare',
       'streamexpr',
       'empty',
       'val_expr')
    def expr(self, p):
        # print("expr", p)
        pass

    @_('lit_expr')
    def val_expr(self, p):
        pass

    @_('add_expr')
    def val_expr(self, p):
        pass

    @_('cond_expr')
    def val_expr(self, p):
        print('val_expr', p.cond_expr)
        return 'val_expr', p.cond_expr

    @_('CHARLIT')
    def lit_expr(self, p):
        pass

    @_('QUOTED')
    def lit_expr(self, p):
        pass

    @_('add_expr PLUS mult_expr')
    def add_expr(self, p):
        pass

    @_('add_expr MINUS mult_expr')
    def add_expr(self, p):
        pass

    @_('mult_expr')
    def add_expr(self, p):
        print('mult_expr', p.mult_expr)
        return 'mult_expr', p.mult_expr

    @_('mult_expr TIMES prime_expr')
    def mult_expr(self, p):
        print('mult_expr *', p.mult_expr, p.prime_expr)
        return 'mult_expr *', p.mult_expr, p.prime_expr

    @_('mult_expr DIVIDE prime_expr')
    def mult_expr(self, p):
        pass

    @_('mult_expr MOD prime_expr')
    def mult_expr(self, p):
        pass

    @_('prime_expr')
    def mult_expr(self, p):
        print('mult primary', p.prime_expr)
        return 'mult_primary', p.prime_expr

    # @_('LPAREN add_expr RPAREN')
    # def prime_expr(self, p):
    #     print('primary')
    #     return 'primary ()', p.add_expr

    # @_('functioncall')
    # def prime_expr(self, p):
    #     pass

    @_('NUMBER')
    def prime_expr(self, p):
        return 'Number', p.NUMBER

    @_('FLOAT')
    def prime_expr(self, p):
        return 'Float', p.FLOAT

    @_('name_expr')
    def prime_expr(self, p):
        print('prime_expr', p.name_expr)
        return 'prime_expr', p.name_expr

    @_('name_expr "." id_expr')
    def name_expr(self, p):
        print('name_expr .', p.name_expr, p.id_expr)
        return 'name_expr .', p.name_expr, p.id_expr

    @_('name_expr SCOPE id_expr')
    def name_expr(self, p):
        print('name_exp ::', p.id_expr)
        return 'name_exp ::', p.id_expr

    @_('name_expr ARROW id_expr')
    def name_expr(self, p):
        print('name_exp ->', p.id_expr)
        return 'name_exp ->', p.id_expr

    @_('PLUS PLUS name_expr')
    def name_expr(self, p):
        print('++name', p.name)
        return '++name', p.name

    @_('name_expr PLUS PLUS')
    def name_expr(self, p):
        print('name++', p.name)
        return 'name++', p.name

    @_('MINUS MINUS name_expr')
    def name_expr(self, p):
        print('name', p.name)
        pass

    @_('name_expr MINUS MINUS')
    def name_expr(self, p):
        print('name', p.name)
        pass

    @_('id_expr')
    def name_expr(self, p):
        print('name_exp', p.id_expr)
        return 'name_exp', p.id_expr

    @_('ID')
    def id_expr(self, p):
        print('id_expr', p.ID)
        return 'id_expr', p.ID

    @_('id_expr LSQBRACE val_expr RSQBRACE')
    def id_expr(self, p):
        print("id_expr array access", p.id_expr, p.val_expr)
        return "id_expr array access", p.id_expr, p.val_expr

    @_('id_expr LPAREN arglist RPAREN')
    def id_expr(self, p):
        print("id_expr function call", p.id_expr, p.arglist)
        return "id_expr function call", p.id_expr, p.arglist

    # @_('name')
    # def id_expr(self, p):
    #     print('id_expr', p.name)
    #     return 'id_expr', p.name

    @_('logic_expr')
    def cond_expr(self, p):
        print('cond_expr', p.logic_expr)
        return 'cond_expr', p.logic_expr

    @_('logic_expr AND logic_expr')
    def logic_expr(self, p):
        print('logic_expr AND', p.logic_expr, p.logic_expr)
        return 'logic_expr AND', p.logic_expr, p.logic_expr

    @_('logic_expr OR logic_expr')
    def logic_expr(self, p):
        print('logic_expr OR', p.logic_expr, p.logic_expr)
        return 'logic_expr OR', p.logic_expr, p.logic_expr

    @_('NOT logic_expr')
    def logic_expr(self, p):
        print('logic_expr NOT', p.logic_expr)
        return 'logic_expr NOT', p.logic_expr

    @_('LPAREN logic_expr RPAREN')
    def logic_expr(self, p):
        print('logic_expr ()', p.logic_expr)
        return 'logic_expr ()', p.logic_expr

    @_('rel_expr')
    def logic_expr(self, p):
        pass

    @_('id_expr')
    def logic_expr(self, p):
        pass

    @_('val_expr relop val_expr')
    def rel_expr(self, p):
        pass

    @_('GT', 'GTE',
       'LT', 'LTE',
       'EQ',
       'NOTEQ')
    def relop(self, p):
        pass


    # Names etc.
    # @_('ID')
    # def name(self, p):
    #     # print("name")
    #     return p.ID

    # @_('ID SCOPE ID')
    # def name(self, p):
    #     pass
    #     return "".join([p.ID0, p.SCOPE, p.ID1])
    #
    # @_('ID "." ID')
    # def name(self, p):
    #     pass
    #     return "".join([p.ID0, ".", p.ID1])

    # @_('name LSQBRACE val_expr RSQBRACE')
    # def name(self, p):
    #     pass
    #     return "%s[expr]" % p.name
    #
    # @_('name LPAREN arglist RPAREN')
    # def functioncall(self, p):
    #     # print("function call", p.name)
    #     pass

    @_('empty',
       'args')
    def arglist(self, p):
        pass

    @_('args "," arg',
       'arg')
    def args(self, p):
        pass

    @_('val_expr')
    def arg(self, p):
        pass

    @_('val_expr OUTSTREAM expr',
       'val_expr INSTREAM expr')
    def streamexpr(self, p):
        # print("stream expr: ")
        pass


    @_('name_expr ASSIGN val_expr')
    def assignment(self, p):
        print('assignment')
        pass

    @_('name_expr PLUSEQ val_expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name_expr MINUSEQ val_expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name_expr TIMESEQ val_expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name_expr DIVEQ val_expr')
    def assignment(self, p):
        # print('assignment')
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
