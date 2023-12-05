tokens = []
current_token_index = -1

def lookahead():
    if current_token_index + 1 < len(tokens):
        return tokens[current_token_index + 1]
    return None

def consume(expected_type, expected_value=None):
    global current_token_index
    current_token_index += 1
    token = tokens[current_token_index]

    if token[0] != expected_type or (expected_value and token[1] != expected_value):
        raise Exception(f"Expected token {expected_type} but got {token[0]}")
    return token

def parse_program():
    stmts = []
    while current_token := lookahead():
        stmts.append(parse_statement())
    return {"type": "program", "body": stmts}

def parse_statement():
    token = lookahead()
    if token[0] == 'keyword' and token[1] == "print":
        return parse_print_statement()
    elif token[0] == 'keyword' and token[1] == "if":
        return parse_if_statement()
    elif token[0] == 'keyword' and token[1] == "while":
        return parse_while_statement()
    elif token[0] == 'symbol' and token[1] == "{":
        return parse_block()
    elif token[0] == "identifier":
        return parse_assignment_or_array_access()
    else:
        raise Exception(f"Unexpected token: {token}")

def parse_print_statement():
    consume('keyword', 'print')
    expressions = []
    while lookahead() and lookahead()[1] != ';':
        expressions.append(parse_expression())
        if lookahead() and lookahead()[1] == ',':
            consume('symbol', ',')
    consume('symbol', ';')
    return {"type": "print_statement", "expressions": expressions}

def parse_expression():
    return parse_conditional()

def parse_conditional():
    expr = parse_additive()
    token = lookahead()
    while token and token[0] == 'symbol' and token[1] in ["<", ">", "<=", ">=", "==", "!="]:
        consume('symbol')
        right_expr = parse_additive()
        expr = {"type": "conditional", "operator": token[1], "left": expr, "right": right_expr}
        token = lookahead()
    return expr

def parse_additive():
    expr = parse_multiplicative()
    token = lookahead()
    while token and token[0] == 'symbol' and token[1] in ['+', '-']:
        consume('symbol')
        right_expr = parse_multiplicative()
        expr = {"type": "additive", "operator": token[1], "left": expr, "right": right_expr}
        token = lookahead()
    return expr

def parse_multiplicative():
    expr = parse_term()
    token = lookahead()
    while token and token[0] == 'symbol' and token[1] in ['*', '/']:
        consume('symbol')
        right_expr = parse_term()
        expr = {"type": "multiplicative", "operator": token[1], "left": expr, "right": right_expr}
        token = lookahead()
    return expr

def parse_term():
    token = lookahead()
    if token[0] == 'number':
        consume('number')
        return {"type": "number", "value": token[1]}
    elif token[0] == 'symbol' and token[1] == "(":
        consume('symbol', '(')
        expr = parse_expression()
        consume('symbol', ')')
        return expr
    elif token[0] == "string":
        consume("string")
        return {"type": "string", "value": token[1]}
    elif token[0] == "identifier":
        consume("identifier")
        return {"type": "identifier", "name": token[1]}
    elif token[0] == "symbol" and token[1] == "[":
        return parse_array()
    else:
        raise Exception(f"Unexpected token: {token}")

def parse_if_statement():
    consume('keyword', 'if')
    consume('symbol', '(')
    condition = parse_expression()
    consume('symbol', ')')
    true_branch = parse_statement()
    
    false_branch = None
    if lookahead() and lookahead()[1] == 'else':
        consume('keyword', 'else')
        false_branch = parse_statement()

    return {"type": "if_statement", "condition": condition, "true_branch": true_branch, "false_branch": false_branch}

def parse_while_statement():
    consume('keyword', 'while')
    consume('symbol', '(')
    condition = parse_expression()
    consume('symbol', ')')
    body = parse_statement()
    return {"type": "while_statement", "condition": condition, "body": body}

def parse_block():
    consume('symbol', '{')
    stmts = []
    while lookahead() and lookahead()[1] != "}":
        stmts.append(parse_statement())
    consume('symbol', '}')
    return {"type": "block", "body": stmts}

def parse_assignment_or_array_access():
    name = consume('identifier')[1]
    if lookahead()[1] == "=":
        consume('symbol', '=')
        value = parse_expression()
        consume('symbol', ';')
        return {"type": "assignment", "name": name, "value": value}
    elif lookahead()[1] == "[":
        consume('symbol', '[')
        index = parse_expression()
        consume('symbol', ']')
        if lookahead()[1] == "=":
            consume('symbol', '=')
            value = parse_expression()
            consume('symbol', ';')
            return {"type": "array_assignment", "name": name, "index": index, "value": value}
        else:
            return {"type": "array_access", "name": name, "index": index}
    else:
        raise Exception("Unexpected token after identifier.")

def parse_array():
    elements = []
    consume('symbol', '[')
    while lookahead() and lookahead()[1] != ']':
        elements.append(parse_expression())
        if lookahead() and lookahead()[1] == ",":
            consume('symbol', ',')
    consume('symbol', ']')
    return {"type": "array", "elements": elements}

# Usage:
source_code = 'print "Hello", 3+4; x = [1, 2, 3]; y = x[1];'
tokens = tokenize(source_code)
ast = parse_program()
print(ast)



# -----

# NEW VERSION


def lookahead(tokens, offset=0):
    if offset < len(tokens):
        return tokens[offset]
    return None

def consume(tokens):
    return tokens.pop(0)

def parse_program(tokens):
    statements = []
    while lookahead(tokens) and lookahead(tokens) != "}":
        statements.append(parse_statement(tokens))
        if lookahead(tokens) == ";":
            consume(tokens)  # Consume the semicolon
    return {"type": "program", "body": statements}

def parse_statement(tokens):
    if lookahead(tokens) == "print":
        return parse_print(tokens)
    elif lookahead(tokens) == "if":
        return parse_if_statement(tokens)
    elif lookahead(tokens) == "while":
        return parse_while_statement(tokens)
    elif lookahead(tokens) == "{":
        return parse_block(tokens)
    elif lookahead(tokens, 1) == "=":
        return parse_assignment(tokens)
    else:
        return parse_expression(tokens)

def parse_assignment(tokens):
    name = consume(tokens)
    _ = consume(tokens)  # "="
    value = parse_expression(tokens)
    return {"type": "assignment", "name": name, "value": value}

def parse_expression(tokens):
    left = parse_term(tokens)
    while lookahead(tokens) in ("+", "-", "<", ">", "==", "!=", "<=", ">="):
        operator = consume(tokens)
        right = parse_term(tokens)
        left = {"type": "binary", "operator": operator, "left": left, "right": right}
    return left

def parse_term(tokens):
    left = parse_factor(tokens)
    while lookahead(tokens) in ("*", "/"):
        operator = consume(tokens)
        right = parse_factor(tokens)
        left = {"type": "binary", "operator": operator, "left": left, "right": right}
    return left

def parse_factor(tokens):
    if lookahead(tokens) == "(":
        _ = consume(tokens)  # "("
        expr = parse_expression(tokens)
        _ = consume(tokens)  # ")"
        return expr
    elif lookahead(tokens) and isinstance(lookahead(tokens), list) and lookahead(tokens)[0] == "number":
        return {"type": "number", "value": consume(tokens)[1]}
    elif lookahead(tokens) and isinstance(lookahead(tokens), list) and lookahead(tokens)[0] == "string":
        return {"type": "string", "value": consume(tokens)[1]}
    elif lookahead(tokens) and isinstance(lookahead(tokens), list) and lookahead(tokens)[0] == "identifier":
        if lookahead(tokens, 1) == "[":
            return parse_array_access(tokens)
        return {"type": "identifier", "name": consume(tokens)[1]}
    else:
        raise Exception(f"Unexpected token {lookahead(tokens)} in factor")

def parse_array_access(tokens):
    name = consume(tokens)[1]
    _ = consume(tokens)  # "["
    index = parse_expression(tokens)
    _ = consume(tokens)  # "]"
    return {"type": "array_access", "name": name, "index": index}

def parse_print(tokens):
    _ = consume(tokens)  # "print"
    expressions = []
    while lookahead(tokens) != ";" and lookahead(tokens) != "}":
        expressions.append(parse_expression(tokens))
        if lookahead(tokens) == ",":
            consume(tokens)
    return {"type": "print", "expressions": expressions}

def parse_if_statement(tokens):
    _ = consume(tokens)  # "if"
    _ = consume(tokens)  # "("
    condition = parse_expression(tokens)
    _ = consume(tokens)  # ")"
    if_body = parse_statement(tokens)
    else_body = None
    if lookahead(tokens) == "else":
        _ = consume(tokens)  # "else"
        else_body = parse_statement(tokens)
    return {"type": "if", "condition": condition, "if_body": if_body, "else_body": else_body}

def parse_while_statement(tokens):
    _ = consume(tokens)  # "while"
    _ = consume(tokens)  # "("
    condition = parse_expression(tokens)
    _ = consume(tokens)  # ")"
    body = parse_statement(tokens)
    return {"type": "while", "condition": condition, "body": body}

def parse_block(tokens):
    _ = consume(tokens)  # "{"
    body = parse_program(tokens)
    _ = consume(tokens)  # "}"
    return {"type": "block", "body": body["body"]}

