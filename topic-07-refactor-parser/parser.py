from tokenizer import tokenize
from pprint import pprint

ebnf = """

<block>           ::= '{' [<statement> { ';' <statement> }] '}'

<expression-list> ::= '(' [ <expression> { ',' <expression> }] ')'

<array> ::=           '[' [ <expression> { ',' <expression> }] ']'

<if-statement>   ::= 'if' '(' <expression> ')' <block> ['else' <block>]

<while-statement> ::= 'while' '(' <expression> ')' <statement>

<print-statement> ::= 'print' <expression-list> 

<return-statement> ::= 'return' [ '(' <expression> ')' ] 

<exit-statement> ::= 'exit' [ '(' <expression> ')' ]

<function-declaration-statement> ::= 'function' <identifier> '(' <identifier> { ',' <identifier> } ')' '{' {<statement>} '}'

<statement>      ::= <if-statement> | 
                     <while-statement> | 
                     <print-statement> | 
                     <return-statement> |
                     <exit-statement> |
                     <function-declaration-statement> | 
                     <block> |
                     <assignment> |
                     <expression>


<reference> ::= <identifier> { '.' <identifier>  | '[' <expression> ']' }

<expression>     ::= <reference> '=' <expression> |
                     







#                     <function_call> | 
#                     <assignment>


<assignment-expression>  ::= <reference> '=' <expression>

<function_call>          ::= <reference> <expression-list> 

<expression>              ::= <term> { ('+' | '-') <term> } 




<print-statement> ::= 'print' '(' <expression-list> ')' 



<term>           ::= <factor> { ('*' | '/') <factor> } 

<factor>         ::= <number> 
                   | <reference> 
                   | '(' <expression> ')' 
                   | '[' {<expression> { ',' <expression> }} ']' 
                   | <function-call>

<function-call>  ::= <reference> '(' [<expression-list>] ')'

<expression-list> ::= <expression> { ',' <expression> }
"""

### EXPRESSIONS


def parse_identifier(tokens):
    """
    An identifier names an entry in the environment.

    <identifier>     ::= <letter> { <letter> | <digit> }
    """
    identifier = tokens.current()
    assert type(identifier) is str and identifier.startswith("@")
    tokens.discard(identifier)
    return identifier


def test_parse_identifier():
    ast = parse_identifier(tokenize("z=x+y"))
    assert ast == "@z"
    try:
        ast = parse_identifier(tokenize("*2+3"))
        raise "An error was expected."
    except:
        pass
    try:
        ast = parse_identifier(tokenize("2+3"))
        raise "An error was expected."
    except:
        pass


def parse_reference(tokens):
    """
    A reference identifies location holding a value that may be set or retrieved.

    <reference> ::= <identifier> { '.' <identifier>  | '[' <expression> ']' }
    """
    name = parse_identifier(tokens)
    indexes = []
    while tokens.current() in [".", "["]:
        if tokens.current() == "[":
            tokens.discard("[")
            indexes.append(parse_expression(tokens))
            tokens.discard("]")
        if tokens.current() == ".":
            tokens.discard(".")
            indexes.append(parse_identifier(tokens))
    if indexes == []:
        return {"type": "reference", "name": name}
    else:
        return {"type": "reference", "name": name, "indexes": indexes}


def test_parse_reference():
    ast = parse_reference(tokenize("x"))
    assert ast == {"type": "reference", "name": "@x"}
    ast = parse_reference(tokenize("x.y"))
    assert ast == {"type": "reference", "name": "@x", "indexes": ["@y"]}
    ast = parse_reference(tokenize("x.y.z"))
    assert ast == {"type": "reference", "name": "@x", "indexes": ["@y", "@z"]}
    ast = parse_reference(tokenize("x[1][2][3]"))
    assert ast == {"type": "reference", "name": "@x", "indexes": [1, 2, 3]}


def parse_expression_list(tokens):
    """
    An expression list is a parenthesized list of zero or more expressions.

    <expression-list> ::= '(' [ <expression> { ',' <expression> }] ')'
    """
    tokens.discard("(")
    expressions = []
    while tokens.current() != ")":
        expressions.append(parse_expression(tokens))
        if tokens.current() != ")":
            tokens.discard(",")
    tokens.discard(")")
    return {"type": "expression-list", "expressions": expressions}


def test_parse_expression_list():
    ast = parse_expression_list(tokenize("()"))
    assert ast == {"type": "expression-list", "expressions": []}
    ast = parse_expression_list(tokenize("(1)"))
    assert ast == {"type": "expression-list", "expressions": [1]}
    ast = parse_expression_list(tokenize("(1,2)"))
    assert ast == {"type": "expression-list", "expressions": [1, 2]}
    ast = parse_expression_list(tokenize("(x,y)"))
    assert ast == {
        "type": "expression-list",
        "expressions": [
            {"type": "reference", "name": "@x"},
            {"type": "reference", "name": "@y"},
        ],
    }


def parse_function_call(reference, tokens):
    """
    A function_call invokes a function with a list of zero or more arguments.
    Note that the reference is passed in.

    <function-call>  ::= <identifier> '(' [ <expression> { ',' <expression> } ] ')'
    """
    expressions = []
    tokens.discard("(")
    while tokens.current() != ")":
        expressions.append(parse_expression(tokens))
        if tokens.current() != ")":
            tokens.discard(",")
    tokens.discard(")")
    return {
        "type": "function_call",
        "reference": reference,
        "expressions": expressions,
    }


def test_parse_function_call():
    reference = parse_reference(tokenize("x"))
    ast = parse_function_call(reference, tokenize("()"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [],
    }
    ast = parse_function_call(reference, tokenize("(1)"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [1],
    }
    ast = parse_function_call(reference, tokenize("(1,2,3)"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [1, 2, 3],
    }


def parse_array_expression(tokens):
    """
    An array_expression list is a bracketed list of zero or more expressions.

    <array> ::= '[' [ <expression> { ',' <expression> }] ']'
    """
    tokens.discard("[")
    expressions = []
    while tokens.current() != "]":
        expressions.append(parse_expression(tokens))
        if tokens.current() != "]":
            tokens.discard(",")
    tokens.discard("]")
    return {"type": "array-expression", "expressions": expressions}


def test_parse_array_expression():
    ast = parse_array_expression(tokenize("[]"))
    assert ast == {"type": "array-expression", "expressions": []}
    ast = parse_array_expression(tokenize("[1]"))
    assert ast == {"type": "array-expression", "expressions": [1]}
    ast = parse_array_expression(tokenize("[1,2]"))
    assert ast == {"type": "array-expression", "expressions": [1, 2]}


def parse_factor(tokens):
    """
    <factor>     ::= <number>
                   | <string>              #not implemented yet
                   | '(' <expression> ')'
                   | <array_expression>
                   | <reference>
                   | <function-call>

    """
    token = tokens.current()
    if type(token) in [int, float]:
        tokens.discard(token)
        return token
    if token.startswith("$"):
        tokens.discard(token)
        return token[1:]
    if token == "(":
        tokens.discard("(")
        expression = parse_expression(tokens)
        tokens.discard(")")
        return expression
    if token == "[":
        return parse_array_expression(tokens)
    reference = parse_reference(tokens)
    if tokens.current() == "(":
        return parse_function_call(reference, tokens)
    return reference


def test_parse_factor():
    ast = parse_factor(tokenize("1"))
    assert ast == 1
    ast = parse_factor(tokenize("1.2"))
    assert ast == 1.2
    ast = parse_factor(tokenize('"banana"'))
    assert ast == "banana"
    ast = parse_factor(tokenize("(1)"))
    assert ast == 1
    ast = parse_factor(tokenize("[1]"))
    assert ast == {"type": "array-expression", "expressions": [1]}
    ast = parse_factor(tokenize("[1,2,3]"))
    assert ast == {"type": "array-expression", "expressions": [1, 2, 3]}
    ast = parse_factor(tokenize("x"))
    assert ast == {"type": "reference", "name": "@x"}
    ast = parse_factor(tokenize("x()"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [],
    }
    ast = parse_factor(tokenize("x(y)"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [{"type": "reference", "name": "@y"}],
    }


def parse_term(tokens):
    """<term>     ::= <factor> { ('*' | '/') <factor> }"""
    left_factor = parse_factor(tokens)
    while tokens.current() in ["*", "/"]:
        operator = tokens.current()
        tokens.discard(operator)
        right_factor = parse_factor(tokens)
        left_factor = {
            "type": "binary",
            "left": left_factor,
            "operator": operator,
            "right": right_factor,
        }
    return left_factor


def test_parse_term():
    ast = parse_term(tokenize("1"))
    assert ast == 1
    ast = parse_term(tokenize("1*2"))
    assert ast == {"type": "binary", "left": 1, "operator": "*", "right": 2}
    ast = parse_term(tokenize("1/2"))
    assert ast == {"type": "binary", "left": 1, "operator": "/", "right": 2}


def parse_expression(tokens):
    """<expression>     ::= <term> { ('+' | '-') <term> }"""
    left_term = parse_term(tokens)
    while tokens.current() in ["+", "-"]:
        operator = tokens.current()
        tokens.discard(operator)
        right_term = parse_term(tokens)
        left_term = {
            "type": "binary",
            "left": left_term,
            "operator": operator,
            "right": right_term,
        }
    return left_term


def test_parse_expression():
    ast = parse_expression(tokenize("1"))
    assert ast == 1
    ast = parse_expression(tokenize("1*2"))
    assert ast == {"type": "binary", "left": 1, "operator": "*", "right": 2}
    ast = parse_expression(tokenize("1+2"))
    assert ast == {"type": "binary", "left": 1, "operator": "+", "right": 2}
    ast = parse_expression(tokenize("1+2*3"))
    assert ast == {
        "type": "binary",
        "left": 1,
        "operator": "+",
        "right": {"type": "binary", "left": 2, "operator": "*", "right": 3},
    }
    ast = parse_expression(tokenize("(1+2)*3"))
    assert ast == {
        "type": "binary",
        "left": {"type": "binary", "left": 1, "operator": "+", "right": 2},
        "operator": "*",
        "right": 3,
    }
    ast = parse_expression(tokenize("x"))
    assert ast == {"type": "reference", "name": "@x"}
    ast = parse_expression(tokenize("x+y"))
    assert ast == {
        "type": "binary",
        "left": {"type": "reference", "name": "@x"},
        "operator": "+",
        "right": {"type": "reference", "name": "@y"},
    }
    ast = parse_expression(tokenize("x()"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [],
    }
    ast = parse_expression(tokenize("x(1,2,3)"))
    assert ast == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [1, 2, 3],
    }


def test_expressions():
    test_parse_identifier()
    test_parse_reference()
    test_parse_expression_list()
    test_parse_function_call()
    test_parse_array_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()


### STATEMENTS


def parse_block(tokens):
    """ 
    <block> ::= '{' [<statement> { ';' <statement> }] '}'
    """
    tokens.discard("{")
    statements = []
    while tokens.current() != "}":
        statements.append(parse_statement(tokens))
        if tokens.current() != "}":
            tokens.discard(";")
    tokens.discard("}")
    return {"type": "block", "statements": statements}


def test_parse_block():
    ast = parse_block(tokenize("{}"))
    assert ast == {"type": "block", "statements": []}
    ## TODO:
    ast = parse_block(tokenize("{{}}"))
    assert ast == {"type": "block", "statements": [{"type": "block", "statements": []}]}
    ast = parse_block(tokenize("{if(1){}}"))
    assert ast == {
        "type": "block",
        "statements": [
            {
                "type": "if",
                "condition": 1,
                "then": {"type": "block", "statements": []},
                "else": None,
            }
        ],
    }
    ast = parse_block(tokenize("{if(1){};if(2){if(1){}}}"))
    assert ast == {
        "type": "block",
        "statements": [
            {
                "type": "if",
                "condition": 1,
                "then": {"type": "block", "statements": []},
                "else": None,
            },
            {
                "type": "if",
                "condition": 2,
                "then": {
                    "type": "block",
                    "statements": [
                        {
                            "type": "if",
                            "condition": 1,
                            "then": {"type": "block", "statements": []},
                            "else": None,
                        }
                    ],
                },
                "else": None,
            },
        ],
    }


def parse_if_statement(tokens):
    """
    <if-statement>   ::= 'if' '(' <expression> ')' <block> ['else' <block>]
    """
    tokens.discard("#if")
    tokens.discard("(")
    condition = parse_expression(tokens)
    tokens.discard(")")
    then_block = parse_block(tokens)
    if tokens.current() == "#else":
        tokens.discard("#else")
        else_block = parse_block(tokens)
    else:
        else_block = None
    return {
        "type": "if",
        "condition": condition,
        "then": then_block,
        "else": else_block,
    }


def test_parse_if_statement():
    ast = parse_if_statement(tokenize("if(1){}"))
    assert ast == {
        "type": "if",
        "condition": 1,
        "then": {"type": "block", "statements": []},
        "else": None,
    }
    ast = parse_if_statement(tokenize("if(1){}else{}"))
    assert ast == {
        "type": "if",
        "condition": 1,
        "then": {"type": "block", "statements": []},
        "else": {"type": "block", "statements": []},
    }


def parse_while_statement(tokens):
    """
    <while-statement> ::= 'while' '(' <expression> ')' <statement>
    """
    tokens.discard("#while")
    tokens.discard("(")
    condition = parse_expression(tokens)
    tokens.discard(")")
    do_block = parse_block(tokens)
    return {
        "type": "while",
        "condition": condition,
        "do": do_block,
    }


def test_parse_while_statement():
    ast = parse_while_statement(tokenize("while(0){}"))
    assert ast == {
        "type": "while",
        "condition": 0,
        "do": {"type": "block", "statements": []},
    }


def parse_print_statement(tokens):
    """
    <print-statement> ::= 'print' <expression-list>
    """
    tokens.discard("#print")
    expression_list = parse_expression_list(tokens)
    return {
        "type": "print",
        "expression_list": expression_list,
    }


def test_parse_print_statement():
    ast = parse_print_statement(tokenize("print(1,2,3)"))
    assert ast == {
        "type": "print",
        "expression_list": {"type": "expression-list", "expressions": [1, 2, 3]},
    }


def parse_return_statement(tokens):
    """
    <return-statement> ::= 'return' '(' <expression> ')'
    """
    tokens.discard("#return")
    tokens.discard("(")
    expression = parse_expression(tokens)
    tokens.discard(")")
    return {
        "type": "return",
        "expression": expression,
    }


def test_parse_return_statement():
    ast = parse_return_statement(tokenize("return (1)"))
    assert ast == {"type": "return", "expression": 1}


def parse_exit_statement(tokens):
    """
    <exit-statement> ::= 'exit' '(' <expression> ')'
    """
    tokens.discard("#exit")
    tokens.discard("(")
    expression = parse_expression(tokens)
    tokens.discard(")")
    return {
        "type": "exit",
        "expression": expression,
    }


def test_parse_exit_statement():
    ast = parse_exit_statement(tokenize("exit (1)"))
    assert ast == {"type": "exit", "expression": 1}


def parse_function_declaration(tokens):
    """
    <function-declaration-statement> ::= 'function' <identifier> '(' <identifier> { ',' <identifier> } ')' <block>
    """
    tokens.discard("#function")
    name = parse_identifier(tokens)
    parameters = []
    tokens.discard("(")
    while tokens.current() != ")":
        parameters.append(parse_identifier(tokens))
        if tokens.current() != ")":
            tokens.discard(",")
    tokens.discard(")")
    block = parse_block(tokens)
    return {
        "type": "function_declaraction",
        "name": name,
        "parameters": parameters,
        "block": block,
    }


def test_parse_function_declaration():
    ast = parse_function_declaration(tokenize("function add(x,y) {}"))
    assert ast == {
        "type": "function_declaraction",
        "name": "@add",
        "parameters": ["@x", "@y"],
        "block": {"type": "block", "statements": []},
    }


def parse_assignment(reference, tokens):
    """
    <expression> ::= <reference> = <expression>

    """
    tokens.discard("=")
    expression = parse_expression(tokens)
    return {
        "type": "assignment",
        "reference": reference,
        "expression": expression,
    }


def test_parse_assignment():
    reference = parse_reference(tokenize("x"))
    ast = parse_assignment(reference, tokenize("=12"))
    assert ast == {
        "type": "assignment",
        "reference": {"type": "reference", "name": "@x"},
        "expression": 12,
    }


def parse_statement(tokens):
    """
    <statement>      ::= <if-statement> |
                        <while-statement> |
                        <print-statement> |
                        <return-statement> |
                        <exit-statement> |
                        <function-declaration-statement> |
                        <block> |
                        <assignment> |
                        <expression>
    """
    token = tokens.current()
    if token == "#if":
        return parse_if_statement(tokens)
    if token == "#while":
        return parse_while_statement(tokens)
    if token == "#print":
        return parse_print_statement(tokens)
    if token == "#return":
        return parse_return_statement(tokens)
    if token == "#exit":
        return parse_exit_statement(tokens)
    if token == "#function":
        return parse_function_declaration(tokens)
    if token == "{":
        return parse_block(tokens)
    expression = parse_expression(tokens)
    if tokens.current() == "=":
        return parse_assignment(expression, tokens)
    return expression


def test_parse_statement():
    t = tokenize
    p = parse_statement
    assert p(t("{}")) == parse_block(t("{}"))
    assert p(t("if(2){}")) == parse_if_statement(t("if(2){}"))
    assert p(t("while(2){}")) == parse_while_statement(t("while(2){}"))
    assert p(t("print(2,3)")) == parse_print_statement(t("print(2,3)"))
    assert p(t("return(2)")) == parse_return_statement(t("return(2)"))
    assert p(t("exit(2)")) == parse_exit_statement(t("exit(2)"))
    assert p(t("function add(x,y) {}")) == parse_function_declaration(
        t("function add(x,y) {}")
    )
    assert p(t("function add(x,y) {}")) == parse_function_declaration(
        t("function add(x,y) {}")
    )
    assert p(t("x=12")) == {
        "type": "assignment",
        "reference": {"type": "reference", "name": "@x"},
        "expression": 12,
    }
    assert p(t("x(2)")) == {
        "type": "function_call",
        "reference": {"type": "reference", "name": "@x"},
        "expressions": [2],
    }
    assert p(t("z=foo(4+4+x)")) == {
        "type": "assignment",
        "reference": {"type": "reference", "name": "@z"},
        "expression": {
            "type": "function_call",
            "reference": {"type": "reference", "name": "@foo"},
            "expressions": [
                {
                    "type": "binary",
                    "left": {"type": "binary", "left": 4, "operator": "+", "right": 4},
                    "operator": "+",
                    "right": {"type": "reference", "name": "@x"},
                }
            ],
        },
    }


def test_statements():
    test_parse_block()
    test_parse_if_statement()
    test_parse_while_statement()
    test_parse_print_statement()
    test_parse_return_statement()
    test_parse_exit_statement()
    test_parse_function_declaration()
    test_parse_assignment()
    test_parse_statement()

def parse(program_tokens):
    global tokens
    global current_token_index
    current_token_index = 0
    tokens = program_tokens
    statements = []
    while tokens.current():
        statements.append(parse_statement())
    # return ["program", statements]
    return {"type":"program","statements":statements}

def test_parse():
    print("testing parse")
    program_tokens = tokenize("print 1+2; {print 3; print 4;}")
    assert program_tokens.list == ['#print', 1, '+', 2, ';', '{', '#print', 3, ';', '#print', 4, ';', '}']
    ast = parse(program_tokens)
    pprint(ast, sort_dicts=False)   
    # assert ast == {'type': 'program', 'statements': [
    #     {'type': 'print', 'expression': 
    #         {'type': 'binary', 'left': 1.0, 'operator': '+', 'right': 2.0}
    #     }, 
    #     {'type': 'block', 'statements': [{'type': 'print', 'expression': 3.0}, {'type': 'print', 'expression': 4.0}]}]}

if __name__ == "__main__":
    test_expressions()
    test_statements()
    test_parse()
    print("done.")
