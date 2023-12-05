from tokenizer import tokenize
from pprint import pprint

ebnf = """
<script>         ::= { <statement> }

<block>          ::= '{' [<statement> { ';' <statement> }] '}'

<statement>      ::= <if-statement> | 
                     <while-statement> | 
                     <print-statement> | 
                     <return-statement> |
                     <exit-statement> |
                     <function-declaration> | 
                     <block> |
                     <expression> |
                     <function_call> | 
                     <assignment>

<assignment>     ::= <reference> '=' <expression> ';'

<reference> ::= <identifier> { '.' <identifier>  | '[' <expression> ']' }

<if-statement>   ::= 'if' '(' <expression> ')' <statement> ['else' <statement>]

<while-statement> ::= 'while' '(' <expression> ')' <statement>

<print-statement> ::= 'print' '(' <expression-list> ')' 

<function-declaration> ::= 'function' <identifier> '(' <identifier> { ',' <identifier> } ')' '{' {<statement>} '}'

<expression>     ::= <term> { ('+' | '-') <term> } 

<term>           ::= <factor> { ('*' | '/') <factor> } 

<factor>         ::= <number> 
                   | <reference> 
                   | '(' <expression> ')' 
                   | '[' {<expression> { ',' <expression> }} ']' 
                   | <function-call>

<function-call>  ::= <reference> '(' [<expression-list>] ')'

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
    """
    <block>          ::= '{' [<statement> { ';' <statement> }] '}'
    """
    tokens.discard("{")
    statements = []
    while tokens.current() != "}":
        statements.append(parse_statement())
        if tokens.current() != "}":
            tokens.discard(";")
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
    reference = parse_reference(tokens)
    if tokens.current() == "=":
        return parse_assignment_statement(reference, tokens)
    if tokens.current() == "(":
        return parse_function_call(reference, tokens)
    raise Exception(f"Unexpected token [ '{token}' ] in statement.")


def parse_assignment_statement(reference, tokens):
    tokens.discard("=")
    expression = parse_expression(tokens)
    return {
        "type": "assignment",
        "reference": reference,
        "expression": expression,
    }


def parse_function_call(reference, tokens):
    """
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


def parse_identifier(tokens):
    identifier = tokens.current()
    assert type(identifier) is str and identifier.startswith("@")
    tokens.discard(identifier)
    return identifier


def parse_factor(tokens):
    """
    <factor>         ::= <number>
                   | '(' <expression> ')'
                   | '[' [ <expression> { ',' <expression> } ] ']'
                   | <reference>
                   | <function-call>

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
    if token == "[":
        tokens.discard("[")
        expressions = []
        if tokens.current() != "]":
            expressions.append(parse_expression(tokens))
            while tokens.current() != "]":
                tokens.discard(",")
                expressions.append(parse_expression(tokens))
        tokens.discard("]")
        return {
            "type": "array",
            "expressions": expressions,
        }
    reference = parse_reference(tokens)
    if tokens.current() == "(":
        return parse_function_call(reference, tokens)
    return reference


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


def parse_reference(tokens):
    """
    <reference> ::= <identifier> { '.' <identifier>  | '[' <expression> ']' }
    """
    assert tokens.current().startswith(
        "@"
    ), f"Error: Reference starts with {tokens.list}"
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
            indexes.append(parse_identifier)
    return {"type": "reference", "identifier": identifier, "indexes": indexes}


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
    print("pfd at ", [tokens.list])
    """
    <function-declaration> ::= 'function' <identifier> '(' <identifier> { ',' <identifier> } ')' '{' {<statement>} '}'
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
    block = parse_block
    statements = []
    tokens.discard("{")
    while tokens.current() != "}":
        print("starting parse at ", [tokens.list])
        statements.append(parse_statement(tokens))
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
    e("x", {"type": "reference", "identifier": "@x", "indexes": []})
    e(
        "x+y",
        {
            "type": "binary",
            "left": {"type": "reference", "identifier": "@x", "indexes": []},
            "operator": "+",
            "right": {"type": "reference", "identifier": "@y", "indexes": []},
        },
    )
    e(
        "x()",
        {
            "type": "function_call",
            "reference": {"type": "reference", "identifier": "@x", "indexes": []},
            "expressions": [],
        },
    )
    e(
        "x(1,2,3)",
        {
            "type": "function_call",
            "reference": {"type": "reference", "identifier": "@x", "indexes": []},
            "expressions": [1, 2, 3],
        },
    )
    e(
        "x(y)",
        {
            "type": "function_call",
            "reference": {"type": "reference", "identifier": "@x", "indexes": []},
            "expressions": [{"type": "reference", "identifier": "@y", "indexes": []}],
        },
    )


def test_statements():
    def s(code, ast):
        p = parse_statement(tokenize(code))
        assert p == ast, f"Expected {ast}, got {p}"

    s("{}", {"type": "block", "statements": []})
    s(
        "if(1){}",
        {
            "type": "if",
            "condition": 1,
            "then": {"type": "block", "statements": []},
            "else": None,
        },
    )
    s(
        "if(1){}else{}",
        {
            "type": "if",
            "condition": 1,
            "then": {"type": "block", "statements": []},
            "else": {"type": "block", "statements": []},
        },
    )
    s(
        "while(1){}",
        {
            "type": "while",
            "condition": 1,
            "do": {"type": "block", "statements": []},
        },
    )
    s(
        "print(1,2,3)",
        {"type": "print", "expressions": [1, 2, 3]},
    )
    s(
        "signal(4)",
        {
            "type": "function_call",
            "reference": {
                "type": "reference",
                "identifier": "@signal",
                "indexes": [],
            },
            "expressions": [4],
        },
    )
    s(
        "function add(x,y) {}",
        {"type": "function_declaraction", "parameters": ["@x", "@y"], "statements": []},
    )


def test_program():
    s(
        """

    """
    )


def test_example_script():
    with open("quicksort.t", "r") as f:
        script = f.read()
        t = tokenize(script)
        print(t.list)
        p = parse_script(t)


if __name__ == "__main__":
    test_expressions()
    test_statements()
    # test_program()
    # test_example_script()
