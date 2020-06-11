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
              ID, FLOATLIT, NUMBER,
              PLUS, MINUS, TIMES, DIVIDE, MOD, PLUSEQ, MINUSEQ, TIMESEQ, DIVEQ,
              EQ, ASSIGN, REF, AND, OR,
              LT, LTE, GT, GTE, NOTEQ, NOT,
              SCOPE, ARROW, OUTSTREAM, INSTREAM,
              RETURN, BREAK, CONTINUE,
              IF, ELSE, FOR, WHILE, SWITCH, DO,
              STATIC, CONST, VOLATILE, PUBLIC, PRIVATE, PROTECTED, VIRTUAL,
              QUOTED, CHARLIT,
              CASE, DEFAULT,
              USING, NAMESPACE,
              FRIEND, TYPEDEF, CONSTEXPR,
              INLINE, VIRTUAL, EXPLICIT, STATIC,
              CHAR, BOOL, SHORT, INT, LONG, SIGNED, UNSIGNED,
              FLOAT, DOUBLE, VOID, AUTO}

    literals = ['.', '"', ',', ':', ';',
                '(', ')', '{', '}', '[', ']', '<', '>']

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Other ignored patterns
    # ignore_comment = r'//.*'
    ignore_newline = r'\n+'

    #USING = r'using\s+namespace'
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
    ID['volatile'] = VOLATILE
    ID['public'] = PUBLIC
    ID['private'] = PRIVATE
    ID['protected'] = PROTECTED
    ID['virtual'] = VIRTUAL
    ID['case'] = CASE
    ID['default'] = DEFAULT
    ID['using'] = USING
    ID['namespace'] = NAMESPACE
    ID['friend'] = FRIEND
    ID['typedef'] = TYPEDEF
    ID['constexpr'] = CONSTEXPR
    ID['inline'] = INLINE
    ID['virtual'] = VIRTUAL
    ID['explicit'] = EXPLICIT
    ID['static'] = STATIC

    # primitive types
    ID['char'] = CHAR
    ID['bool'] = BOOL
    ID['short'] = SHORT
    ID['int'] = INT
    ID['long'] = LONG
    ID['signed'] = SIGNED
    ID['unsigned'] = UNSIGNED
    ID['float'] = FLOAT
    ID['double'] = DOUBLE
    ID['void'] = VOID
    ID['auto'] = AUTO


    # MULTCOMMENT = r'/*[^*]*[*]+(?:[^/*][^*]*[*]+)*/'
    # MULTCOMMENTSTART = r'/\*'
    # MULTCOMMENTEND = r'\*/'
    # LINES = '[^*\n]+'
    COMMENT = r'//(.+?)\n'

    FLOATLIT = r'\d+\.\d+'
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

    LTE = r'<='

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

    @_('CASE constant_expression ":" statement')
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
    def selection_statement(self, p):
        print('selection_statement IF1', p.condition, p.statement)
        return 'selection_statement IF1', p.condition, p.statement

    @_('IF "(" condition ")" statement ELSE statement')
    def selection_statement(self, p):
        print('selection_statement IF2', p.condition, p.statement0, p.statement1)
        return 'selection_statement IF2', p.condition, p.statement0, p.statement1

    @_('SWITCH "(" condition ")" statement')
    def selection_statement(self, p):
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

    @_('DO statement WHILE "(" expression ")" ";" ')
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
        return 'iteration_statement FOR empty', p.statement

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
    @_('declaration_seq')
    def declaration_statement(self, p):
        pass

    # ********** declaration_seq ***********
    @_('declaration')
    def declaration_seq(self, p):
        print('declaration_seq', p.declaration)
        return 'declaration_seq', p.declaration

    @_('declaration_seq declaration')
    def declaration_seq(self, p):
        print('declaration_seq', p.declaration_seq, p.declaration)
        return 'declaration_seq', p.declaration_seq, p.declaration

    # ********** declaration ***********
    @_('block_declaration')
    def declaration(self, p):
        print('declaration', p.block_declaration)
        return 'declaration', p.block_declaration

    @_('function_definition')
    def declaration(self, p):
        print('declaration', p.function_definition)
        return 'declaration', p.function_definition

    @_('template_declaration')
    def declaration(self, p):
        print('declaration', p.template_declaration)
        return 'declaration', p.template_declaration

    @_('namespace_definition')
    def declaration(self, p):
        print('declaration', p.namespace_definition)
        return 'declaration', p.namespace_definition

    @_('empty_declaration')
    def declaration(self, p):
        print('declaration', p.empty_declaration)
        return 'declaration', p.empty_declaration

    @_('empty ";"')
    def empty_declaration(self, p):
        pass

    # ********** block_declaration ***********
    @_('simple_declaration')
    def block_declaration(self, p):
        print('block_declaration', p)

    @_('using_directive')
    def block_declaration(self, p):
        print('block_declaration', p)

    # ********** simple_declaration ***********
    @_('decl_specifier_seq init_declarator_list ";"')
    def simple_declaration(self, p):
        print('simple_declaration', p)

    # ********** decl_specifier_seq **********
    @_('decl_specifier decl_specifier_seq')
    def decl_specifier_seq(self, p):
        print('decl_specifier_seq', p.decl_specifier, p.decl_specifier_seq)
        return 'decl_specifier_seq', p.decl_specifier, p.decl_specifier_seq

    @_('decl_specifier')
    def decl_specifier_seq(self, p):
        print('decl_specifier_seq', p.decl_specifier)
        return 'decl_specifier_seq', p.decl_specifier

    # ********** decl_specifier **********
    @_('storage_class_specifier')
    def decl_specifier(self, p):
        print('decl_specifier', p.storage_class_specifier)
        return 'decl_specifier', p.storage_class_specifier

    @_('type_specifier')
    def decl_specifier(self, p):
        print('decl_specifier', p.type_specifier)
        return 'decl_specifier', p.type_specifier

    @_('function_specifier')
    def decl_specifier(self, p):
        print('decl_specifier', p.type_specifier)
        return 'decl_specifier', p.type_specifier

    @_('FRIEND')
    def decl_specifier(self, p):
        print('decl_specifier', p.FRIEND)
        return 'decl_specifier', p.FRIEND

    @_('TYPEDEF')
    def decl_specifier(self, p):
        print('decl_specifier', p.TYPEDEF)
        return 'decl_specifier', p.TYPEDEF

    @_('CONSTEXPR')
    def decl_specifier(self, p):
        print('decl_specifier', p.CONSTEXPR)
        return 'decl_specifier', p.CONSTEXPR

    # ********** function_specifier **********
    @_('INLINE')
    def function_specifier(self, p):
        print('function_specifier', p.INLINE)
        return 'function_specifier', p.INLINE

    @_('VIRTUAL')
    def function_specifier(self, p):
        print('function_specifier', p.VIRTUAL)
        return 'function_specifier', p.VIRTUAL

    @_('EXPLICIT')
    def function_specifier(self, p):
        print('function_specifier', p.EXPLICIT)
        return 'function_specifier', p.EXPLICIT

    # ********** storage_class_specifier **********
    @_('STATIC')
    def storage_class_specifier(self, p):
        print('storage_class_specifier', p.STATIC)
        return 'storage_class_specifier', p.STATIC

    # ********** type_specifier **********
    @_('trailing_type_specifier')
    def type_specifier(self, p):
        print('type_specifier', p.trailing_type_specifier)
        return 'type_specifier', p.trailing_type_specifier

    @_('class_specifier')
    def type_specifier(self, p):
        print('type_specifier', p.class_specifier)
        return 'type_specifier', p.class_specifier

    @_('enum_specifier')
    def type_specifier(self, p):
        print('type_specifier', p.enum_specifier)
        return 'type_specifier', p.enum_specifier

    # ********** trailing_type_specifier **********
    @_('simple_type_specifier')
    def trailing_type_specifier(self, p):
        print('trailing_type_specifier', p.simple_type_specifier)
        return 'trailing_type_specifier', p.simple_type_specifier

    @_('typename_specifier')
    def trailing_type_specifier(self, p):
        print('trailing_type_specifier', p.typename_specifier)
        return 'trailing_type_specifier', p.typename_specifier

    @_('cv_qualifier')
    def trailing_type_specifier(self, p):
        print('trailing_type_specifier', p.cv_qualifier)
        return 'trailing_type_specifier', p.cv_qualifier

    # ********** simple_type_specifier **********
    @_('empty type_name')
    def simple_type_specifier(self, p):
        print('simple_type_specifier', p.type_name)
        return 'simple_type_specifier', p.type_name

    @_('nested_name_specifier type_name')
    def simple_type_specifier(self, p):
        print('simple_type_specifier', p.nested_name_specifier, p.type_name)
        return 'simple_type_specifier', p.nested_name_specifier, p.type_name

    @_('CHAR',
       'BOOL',
       'SHORT',
       'INT',
       'LONG',
       'SIGNED',
       'UNSIGNED',
       'FLOAT',
       'DOUBLE',
       'VOID',
       'AUTO')
    def simple_type_specifier(self, p):
        print('simple_type_specifier', p)
        return 'simple_type_specifier', p

    # ********** type_name **********
    @_('class_name')
    def type_name(self, p):
        print('type_name', p.class_name)
        return 'type_name', p.class_name

    @_('enum_name')
    def type_name(self, p):
        print('type_name', p.enum_name)
        return 'type_name', p.enum_name

    @_('typedef_name')
    def type_name(self, p):
        print('type_name', p.typedef_name)
        return 'type_name', p.typedef_name

    @_('simple_template_id')
    def type_name(self, p):
        print('type_name', p.simple_template_id)
        return 'type_name', p.simple_template_id

    # ********** class_name **********
    @_('identifier')
    def class_name(self, p):
        print('class_name', p.identifier)
        return 'class_name', p.identifier

    @_('simple_template_id')
    def class_name(self, p):
        print('class_name', p.simple_template_id)
        return 'class_name', p.simple_template_id

    # ********** enum_name **********
    @_('identifier')
    def enum_name(self, p):
        print('enum_name', p.identifier)
        return 'enum_name', p.identifier

    # ********** typedef_name **********
    @_('identifier')
    def typedef_name(self, p):
        print('typedef_name', p.identifier)
        return 'typedef_name', p.identifier

    # ********** simple_template_id **********
    @_('template_name "<" template_argument_list ">" ')
    def simple_template_id(self, p):
        print('simple_template_id', p.template_name, p.template_argument_list)
        return 'simple_template_id', p.template_name, p.template_argument_list

    @_('template_name "<" empty ">" ')
    def simple_template_id(self, p):
        print('simple_template_id', p.template_name)
        return 'simple_template_id', p.template_name

    # ********** template_name **********
    @_('identifier')
    def template_name(self, p):
        print('template_name', p.identifier)
        return 'template_name', p.identifier

    # ********** template_argument_list **********
    @_('template_argument')
    def template_argument_list(self, p):
        print('template_argument_list', p.template_argument)
        return 'template_argument_list', p.template_argument

    @_('template_argument_list template_argument')
    def template_argument_list(self, p):
        print('template_argument_list', p.template_argument_list, p.template_argument)
        return 'template_argument_list', p.template_argument_list, p.template_argument

    # ********** template_argument **********
    @_('constant_expression')
    def template_argument(self, p):
        print('template_argument', p.constant_expression)
        return 'template_argument', p.constant_expression

    @_('type_id')
    def template_argument(self, p):
        print('template_argument', p.type_id)
        return 'template_argument', p.type_id

    @_('id_expression')
    def template_argument(self, p):
        print('template_argument', p.id_expression)
        return 'template_argument', p.id_expression

    # ********** type_id **********
    @_('type_specifier_seq abstract_declarator')
    def type_id(self, p):
        print('type_id', p.type_specifier_seq, p.abstract_declarator)
        return 'type_id', p.type_specifier_seq, p.abstract_declarator

    @_('type_specifier_seq empty')
    def type_id(self, p):
        print('type_id', p.type_specifier_seq)
        return 'type_id', p.type_specifier_seq

    # ********** abstract_declarator **********
    @_('ptr_abstract_declarator')
    def abstract_declarator(self, p):
        print('abstract_declarator', p.ptr_abstract_declarator)
        return 'abstract_declarator', p.ptr_abstract_declarator

    @_('noptr_abstract_declarator parameters_and_qualifiers trailing_return_type')
    def abstract_declarator(self, p):
        print('abstract_declarator', p.noptr_abstract_declarator, p.parameters_and_qualifiers,
              p.trailing_return_type)
        return 'abstract_declarator', p.noptr_abstract_declarator, p.parameters_and_qualifiers, p.trailing_return_type

    @_('abstract_pack_declarator')
    def abstract_declarator(self, p):
        print('abstract_declarator', p.abstract_pack_declarator)
        return 'abstract_declarator', p.abstract_pack_declarator

    # ********** ptr_abstract_declarator **********
    @_('noptr_abstract_declarator')
    def ptr_abstract_declarator(self, p):
        print('ptr_abstract_declarator', p.noptr_abstract_declarator)
        return 'ptr_abstract_declarator', p.noptr_abstract_declarator

    @_('ptr_operator ptr_abstract_declarator')
    def ptr_abstract_declarator(self, p):
        print('ptr_abstract_declarator', p.ptr_operator, p.ptr_abstract_declarator)
        return 'ptr_abstract_declarator', p.ptr_operator, p.ptr_abstract_declarator

    @_('ptr_operator empty')
    def ptr_abstract_declarator(self, p):
        print('ptr_abstract_declarator', p.ptr_operator)
        return 'ptr_abstract_declarator', p.ptr_operator

    # ********** ptr_operator **********
    @_('TIMES cv_qualifier_seq')
    def ptr_operator(self, p):
        print('ptr_operator', p.TIMES, p.cv_qualifier_seq)
        return 'ptr_operator', p.TIMES, p.cv_qualifier_seq

    @_('TIMES empty')
    def ptr_operator(self, p):
        print('ptr_operator', p.TIMES)
        return 'ptr_operator', p.TIMES

    @_('REF')
    def ptr_operator(self, p):
        print('ptr_operator', p.REF)
        return 'ptr_operator', p.REF

    @_('AND')
    def ptr_operator(self, p):
        print('ptr_operator', p.AND)
        return 'ptr_operator', p.AND

    @_('nested_name_specifier TIMES cv_qualifier_seq')
    def ptr_operator(self, p):
        print('ptr_operator', p.nested_name_specifier, p.TIMES, p.cv_qualifier_seq)
        return 'ptr_operator', p.nested_name_specifier, p.TIMES, p.cv_qualifier_seq

    @_('nested_name_specifier TIMES empty')
    def ptr_operator(self, p):
        print('ptr_operator', p.nested_name_specifier, p.TIMES)
        return 'ptr_operator', p.nested_name_specifier, p.TIMES

    # ********** cv_qualifier_seq **********
    @_('cv_qualifier cv_qualifier_seq')
    def cv_qualifier_seq(self, p):
        print('cv_qualifier_seq', p.cv_qualifier, cv_qualifier_seq)
        return 'cv_qualifier_seq', p.cv_qualifier, cv_qualifier_seq

    @_('cv_qualifier empty')
    def cv_qualifier_seq(self, p):
        print('cv_qualifier_seq', p.cv_qualifier)
        return 'cv_qualifier_seq', p.cv_qualifier

    # ********** cv_qualifier **********
    @_('CONST')
    def cv_qualifier(self, p):
        print('cv_qualifier', p.CONST)
        return 'cv_qualifier', p.CONST

    @_('VOLATILE')
    def cv_qualifier(self, p):
        print('cv_qualifier', p.VOLATILE)
        return 'cv_qualifier', p.VOLATILE

    # ********** nested_name_specifier **********
    @_('SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.SCOPE)
        return 'nested_name_specifier', p.SCOPE

    @_('type_name SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.type_name, p.SCOPE)
        return 'nested_name_specifier', p.type_name, p.SCOPE

    @_('namespace_name SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.namespace_name, p.SCOPE)
        return 'nested_name_specifier', p.namespace_name, p.SCOPE

    @_('nested_name_specifier identifier SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.nested_name_specifier, p.identifier, p.SCOPE)
        return 'nested_name_specifier', p.nested_name_specifier, p.identifier, p.SCOPE

    @_('nested_name_specifier TEMPLATE simple_template_id SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.nested_name_specifier, p.TEMPLATE, p.simple_template_id, p.SCOPE)
        return 'nested_name_specifier', p.nested_name_specifier, p.TEMPLATE, p.simple_template_id, p.SCOPE

    @_('nested_name_specifier empty simple_template_id SCOPE')
    def nested_name_specifier(self, p):
        print('nested_name_specifier', p.nested_name_specifier, p.simple_template_id, p.SCOPE)
        return 'nested_name_specifier', p.nested_name_specifier, p.simple_template_id, p.SCOPE

    # ********** namespace_name **********
    @_('identifier')
    def namespace_name(self, p):
        print('namespace_name', p.identifier)
        return 'namespace_name', p.identifier

    # ********** noptr_abstract_declarator **********
    @_('noptr_abstract_declarator parameters_and_qualifiers')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.noptr_abstract_declarator, p.parameters_and_qualifiers)
        return 'noptr_abstract_declarator', p.noptr_abstract_declarator, p.parameters_and_qualifiers

    @_('empty parameters_and_qualifiers')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.parameters_and_qualifiers)
        return 'noptr_abstract_declarator', p.parameters_and_qualifiers

    @_('noptr_abstract_declarator "[" constant_expression "]"')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.noptr_abstract_declarator, p.constant_expression)
        return 'noptr_abstract_declarator', p.noptr_abstract_declarator, p.constant_expression

    @_('noptr_abstract_declarator "[" empty "]"')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.noptr_abstract_declarator)
        return 'noptr_abstract_declarator', p.noptr_abstract_declarator

    @_('empty "[" constant_expression "]"')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.constant_expression)
        return 'noptr_abstract_declarator', p.constant_expression

    @_('empty "[" empty "]"')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator []')
        return 'noptr_abstract_declarator []'

    @_('"(" ptr_abstract_declarator ")"')
    def noptr_abstract_declarator(self, p):
        print('noptr_abstract_declarator', p.ptr_abstract_declarator)
        return 'noptr_abstract_declarator', p.ptr_abstract_declarator

    # ********** parameters_and_qualifiers **********

    # TODO
    '''
    parameters_and_qualifiers
    
    trailing_return_type
    
    type_specifier_seq
    
    id_expression
    
    typename_specifier
    class_specifier
    enum_specifier
    
    
    
    init_declarator_list
    using_directive
    function_definition
    template_declaration
    namespace_definition
    
    
    try_catch_statement
    
    expression
    constant_expression
    simple_declaration
    identifier
    
    
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
