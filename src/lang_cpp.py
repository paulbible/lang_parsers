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
              SCOPE, OUTSTREAM, INSTREAM,
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


class CppParser(Parser):
    debugfile = "parser.out"
    tokens = CppLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', AND, OR),
    )

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
        # print('statement')
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

    @_('RETURN expr ";"')
    def returnstatement(self, p):
        #print("return statement")
        pass

    @_('IF LPAREN expr RPAREN block')
    def ifstatement(self, p):
        # print("if statement block")
        pass

    @_('IF LPAREN expr RPAREN expr')
    def ifstatement(self, p):
        # print("if statement not bracket {BAD}")
        pass

    @_('IF LPAREN expr RPAREN block ELSE block')
    def ifstatement(self, p):
        # print("if-else statement blocks")
        pass

    @_('IF LPAREN expr RPAREN block ELSE ifstatement')
    def ifstatement(self, p):
        # print("if-else-if statement")
        pass

    @_('ID ID LPAREN paramlist RPAREN block')
    def funcdec(self, p):
        # print('func declaration', p.ID1)
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

    @_('WHILE LPAREN expr RPAREN block')
    def whileloop(self, p):
        pass

    @_('FOR LPAREN declare ";" expr ";" expr RPAREN block')
    def forloop(self, p):
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

    @_('ID ID ASSIGN expr')
    def decassign(self, p):
        # print('declaration and assignment')
        pass
        return "type: %s, name: %s" % (p.ID0, p.ID1)

    @_('CHARLIT',
       'LPAREN expr RPAREN',
       'binaryexpr',
       'assignment',
       'declare',
       'streamexpr',
       'functioncall',
       'condition',
       'incexpr',
       'name',
       'QUOTED',
       'NUMBER',
       'FLOAT',
       'empty')
    def expr(self, p):
        # print("expr", p)
        pass

    @_('ID')
    def name(self, p):
        # print("name")
        pass
        return p.ID

    @_('ID SCOPE ID')
    def name(self, p):
        pass
        return "".join([p.ID0, p.SCOPE, p.ID1])

    @_('ID "." ID')
    def name(self, p):
        pass
        return "".join([p.ID0, ".", p.ID1])

    @_('name LSQBRACE expr RSQBRACE')
    def name(self, p):
        pass
        return "%s[expr]" % p.name

    @_('name LPAREN arglist RPAREN')
    def functioncall(self, p):
        # print("function call", p.name)
        pass

    @_('empty',
       'args')
    def arglist(self, p):
        pass

    @_('args "," arg',
       'arg')
    def args(self, p):
        pass

    @_('expr')
    def arg(self, p):
        pass

    @_('expr OUTSTREAM expr',
       'expr INSTREAM expr')
    def streamexpr(self, p):
        # print("stream expr: ")
        pass

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr AND expr',
       'expr OR expr',
       'expr MOD expr')
    def binaryexpr(self, p):
        # print("binary expr")
        pass

    @_('name ASSIGN expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name PLUSEQ expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name MINUSEQ expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name TIMESEQ expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('name DIVEQ expr')
    def assignment(self, p):
        # print('assignment')
        pass

    @_('PLUS PLUS ID',
       'ID PLUS PLUS')
    def incexpr(self, p):
        # print("inc expr", p.ID)
        pass

    @_('NOT expr',
       'expr relop expr')
    def condition(self, p):
        # print("condition")
        pass

    @_('GT', 'GTE',
       'LT', 'LTE',
       'EQ',
       'NOTEQ')
    def relop(self, p):
        pass

    def error(self, p):
        if p:
            print(">>>>>>>>>>")
            print("Syntax error at token:", p.value)
            print(dir(p))
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
