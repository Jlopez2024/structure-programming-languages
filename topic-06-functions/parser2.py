from tokenizer import tokenize
from pprint import pprint

ebnf = """
<script>         ::= { <statement> }

<statement>      ::= <if-statement> | 
                     <while-statement> | 
                     <print-statement> | 
                     <function-declaration> | 
                     <function_call> | 
                     <assignment>

<assignment>     ::= <lhs-expression> '=' <expression> ';'

<left-expression> ::= <identifier> { <left-tail> }

<left-tail>       ::= '.' <identifier> 
                    | '[' <expression> ']'

<if-statement>   ::= 'if' '(' <expression> ')' <statement> ['else' <statement>]

<while-statement> ::= 'while' '(' <expression> ')' <statement>

<print-statement> ::= 'print' '(' <expression-list> ')' 

<function-declaration> ::= 'function' <identifier> '(' [<identifier-list>] ')' '{' {<statement>} '}'

<identifier-list>     ::= <identifier> { ',' <identifier> }

<expression>     ::= <term> { ('+' | '-') <term> } 

<term>           ::= <factor> { ('*' | '/') <factor> } 

<factor>         ::= <number> 
                   | <lhs-expression> 
                   | '(' <expression> ')' 
                   | <function-call>

<function-call>  ::= <identifier> '(' [<expression-list>] ')'

<expression-list> ::= <expression> { ',' <expression> }

<identifier>     ::= <letter> { <letter> | <digit> }

<letter>         ::= 'a'...'z' | 'A'...'Z'

<digit>          ::= '0'...'9'

<number>         ::= { <digit> } ['.' { <digit> }]

"""


def parse_script(tokens):
    """<script>  ::= { <statement> }"""
    statements = []
    while tokens.current():
        statements.append(parse_statement(tokens))
    return {"type": "script", "statements": statements}


def parse_block(tokens):
    tokens.discard("{")
    statements = []
    while tokens.current() != "}":
        statements.append(parse_statement())
    tokens.discard("}")
    return {"type": "block", "statements": statements}


def parse_statement(tokens):
    """
    <statement>  ::= <if-statement> |
                     <while-statement> |
                     <print-statement> |
                     <function-declaration> |
                     <function_call> |
                     <assignment>
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
    if token == "#print":
        return parse_print_statement(tokens)
    if token == "#function":
        return parse_function_declaration(tokens)
    if token == "{":
        return parse_block(tokens)
    left_expression = parse_left_expression(tokens)
    if tokens.current() == "=":
        return parse_assignment_statement(left_expression, tokens)
    if tokens.current() == "(":
        return parse_function_call(left_expression, tokens)
    raise Exception(f"Unexpected token [ '{token}' ] in statement.")


def parse_assignment_statement(left_expression, tokens):
    tokens.discard("=")
    expression = parse_expression(tokens)
    return {
        "type": "assignment",
        "left_expression": left_expression,
        "expression": expression,
    }


def parse_function_call(left_expression, tokens):
    """
    <function-call>  ::= <identifier> '(' [<expression-list>] ')'
    <expression-list> ::= <expression> { ',' <expression> }
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
        "left_expression": left_expression,
        "expressions": expressions,
    }


def parse_identifier(tokens):
    identifier = tokens.current()
    assert type(identifier) is str and identifier.startswith("@")
    tokens.discard(identifier)
    return identifier


def parse_factor(tokens):
    """
    <factor>         ::= <number>
                   | '(' <expression> ')'
                   | <lhs-expression>
                   | <function-call>

    <function-call>  ::= <identifier> '(' [<expression-list>] ')'
    """
    token = tokens.current()
    if type(token) in [int, float]:
        tokens.discard(token)
        return token
    if token == "(":
        tokens.discard("(")
        expression = parse_expression(tokens)
        tokens.discard(")")
        return expression
    left_expression = parse_left_expression(tokens)
    if tokens.current() == "(":
        return parse_function_call(left_expression, tokens)
    return left_expression


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


def parse_left_expression(tokens):
    """
    <left-expression> ::= <identifier> { <left-tail> }

    <left-tail>       ::= '.' <identifier>  |
                          '[' <expression> ']'
    """
    assert tokens.current().startswith("@")
    identifier = tokens.current()
    indexes = []
    tokens.discard()
    while tokens.current() in [".", "["]:
        if tokens.current() == "[":
            tokens.discard("[")
            indexes.append(parse_expression(tokens))
            tokens.discard("]")
        if tokens.current() == ".":
            tokens.discard(".")
            assert tokens.current().startswith("@")
            indexes.append(tokens.current())
            tokens.discard()
    return {"type": "left_expression", "identifier": identifier, "indexes": indexes}


def parse_if_statement(tokens):
    """<if-statement>   ::= 'if' '(' <expression> ')' <statement> ['else' <statement>]"""
    tokens.discard("#if")
    tokens.discard("(")
    condition = parse_expression(tokens)
    tokens.discard(")")
    then_statement = parse_statement(tokens)
    if tokens.current() == "#else":
        tokens.discard("#else")
        else_statement = parse_statement(tokens)
    else:
        else_statement = None
    return {
        "type": "if",
        "condition": condition,
        "then": then_statement,
        "else": else_statement,
    }


def parse_while_statement(tokens):
    """<while-statement> ::= 'while' '(' <expression> ')' <statement>"""
    tokens.discard("#while")
    tokens.discard("(")
    condition = parse_expression(tokens)
    tokens.discard(")")
    do_statement = parse_statement(tokens)
    return {
        "type": "while",
        "condition": condition,
        "do": do_statement,
    }


def parse_print_statement(tokens):
    """
    <print-statement> ::= 'print' '('{<expression-list>}')'
    <expression-list> ::= <expression> { ',' <expression> }
    """
    tokens.discard("#print")
    expressions = []
    tokens.discard("(")
    while tokens.current() != ")":
        expressions.append(parse_expression(tokens))
        if tokens.current() != ")":
            tokens.discard(",")
    tokens.discard(")")
    return {
        "type": "print",
        "expressions": expressions,
    }


def parse_return_statement(tokens):
    """<return-statement> ::= 'return' <expression>"""
    tokens.discard("#return")
    expression = parse_expression(tokens)
    return {
        "type": "return",
        "expression": expression,
    }


def parse_function_declaration(tokens):
    """
    <function-declaration> ::= 'function' <identifier> '(' [<parameter-list>] ')' '{' {<statement>} '}'
    <parameter-list> ::= <identifier> { ',' <identifier> }
    """
    tokens.discard("#function")
    identifier = parse_identifier(tokens)
    parameters = []
    tokens.discard("(")
    while tokens.current() != ")":
        parameters.append(parse_identifier(tokens))
        if tokens.current() != ")":
            tokens.discard(",")
    tokens.discard(")")
    statements = []
    tokens.discard("{")
    while tokens.current() != "}":
        statements.append(parse_statement())
    tokens.discard("}")
    return {
        "type": "function_declaraction",
        "parameters": parameters,
        "statements": statements,
    }


### TESTS


def test_expressions():
    def e(code, ast):
        p = parse_expression(tokenize(code))
        assert p == ast, f"Expected {ast}, got {p}"

    e("1", 1)
    e("1+2", {"type": "binary", "left": 1, "operator": "+", "right": 2})
    e(
        "1+2*3",
        {
            "type": "binary",
            "left": 1,
            "operator": "+",
            "right": {"type": "binary", "left": 2, "operator": "*", "right": 3},
        },
    )
    e(
        "(1+2)*3",
        {
            "type": "binary",
            "left": {"type": "binary", "left": 1, "operator": "+", "right": 2},
            "operator": "*",
            "right": 3,
        },
    )
    e("x", {"type": "left_expression", "identifier": "@x", "indexes": []})
    e(
        "x+y",
        {
            "type": "binary",
            "left": {"type": "left_expression", "identifier": "@x", "indexes": []},
            "operator": "+",
            "right": {"type": "left_expression", "identifier": "@y", "indexes": []},
        },
    )
    e("x()", {'type': 'function_call', 'left_expression': {'type': 'left_expression', 'identifier': '@x', 'indexes': []}, 'expressions': []})
    e("x(1,2,3)", {'type': 'function_call', 'left_expression': {'type': 'left_expression', 'identifier': '@x', 'indexes': []}, 'expressions': [1, 2, 3]})
    e("x(y)", {'type': 'function_call', 'left_expression': {'type': 'left_expression', 'identifier': '@x', 'indexes': []}, 'expressions': [{'type': 'left_expression', 'identifier': '@y', 'indexes': []}]})


def test_statements():
    def s(code, ast):
        p = parse_statement(tokenize(code))
        assert p == ast, f"Expected {ast}, got {p}"

    s("{}", {"type": "block", "statements": []})
    s(
        "if(1){};",
        {
            "type": "if",
            "condition": 1,
            "then": {"type": "block", "statements": []},
            "else": None,
        },
    )
    s(
        "if(1){}else{};",
        {
            "type": "if",
            "condition": 1,
            "then": {"type": "block", "statements": []},
            "else": {"type": "block", "statements": []},
        },
    )
    s(
        "while(1){};",
        {
            "type": "while",
            "condition": 1,
            "do": {"type": "block", "statements": []},
        },
    )
    s(
        "print(1,2,3);",
        {"type": "print", "expressions": [1, 2, 3]},
    )
    s(
        "signal(4);",
        {
            "type": "function_call",
            "left_expression": {
                "type": "left_expression",
                "identifier": "@signal",
                "indexes": [],
            },
            "expressions": [4],
        },
    )
    s(
        "function add(x,y) {};",
        {"type": "function_declaraction", "parameters": ["@x", "@y"], "statements": []},
    )


# def test_parse_left_expression():
#     ast = parse_left_expression(tokenize("x=1"))
#     pprint(ast, sort_dicts=False)
#     ast = parse_left_expression(tokenize("x[3]=1"))
#     pprint(ast, sort_dicts=False)
#     ast = parse_left_expression(tokenize("x[3][4]=1"))
#     pprint(ast, sort_dicts=False)
#     t = tokenize("x.y=1")
#     pprint(t.list)
#     ast = parse_left_expression(tokenize("x.y=1"))
#     pprint(ast, sort_dicts=False)
#     ast = parse_left_expression(tokenize("x.y[3]=1"))
#     pprint(ast, sort_dicts=False)
#     ast = parse_left_expression(tokenize("x[3].y=1"))
#     pprint(ast, sort_dicts=False)


if __name__ == "__main__":
    test_expressions()
    test_statements()
