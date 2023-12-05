from tokenizer import tokenize

'''
<factor> = 
    <number>
    (expression)
    <identifier>
    <identifier>[<expression>]
    <identifier>.<identifier>
    <identifier>(<expression-list>)

<term> = 
    <factor>
    
'''

def parse_factor(tokens):
    token = tokens.current()
    if type(token) in [int, float]:
        tokens.discard()
        return token

def test_parse_factor():
    print("testing parse factor")
    tokens = tokenize("3 + 4")
    print(tokens.list)
    assert parse_factor(tokens) == 3

if __name__ == "__main__":
    test_parse_factor()
    print("done")

# # def parse_parameters():
# #     parameters = []
# #     assert get_current_token() == "("
# #     consume_token()
# #     current_token == get_current_token()
# #     while current_token() != ")":
# #         assert current_token[0] == "identifier"
# #         parameters.append(current_token[1])
# #         current_token == get_current_token()
# #         if current_token != ")":
# #             assert current_token == ","
# #             consume_token()
# #     assert current_token == ")"  # not necesssary
# #     consume_token()
# #     return parameters


# # def parse_function_declaration():
# #     assert get_current_token() == "function"
# #     consume_token()
# #     current_token = get_current_token()
# #     name = consume_token("identifier")[1]
# #     parameters = parse_parameters()
# #     body = parse_block()
# #     return {type: "function", name: name, parameters: parameters, body: body}


# # def parse_return_statement():
# #     consume_token("return")
# #     if get_current_token() != ";":
# #         expression = parse_expression()
# #     else:
# #         expression = None
# #     consume_token(";")
# #     return {"type": "return", "expression": expression}


# # def parse_block():
# #     assert get_current_token() == "("
# #     consume_token()  # Consume '{'
# #     statements = []
# #     while get_current_token() != "}":
# #         statements.append(parse_statement())
# #     assert get_current_token() == "}"
# #     consume_token()  # Consume '}'
# #     return {"type": "block", "statements": statements}


# # def parse_expression():
# #     left_term = parse_term()
# #     while get_current_token() in ["+", "-"]:
# #         operator = get_current_token()
# #         consume_token()
# #         right_term = parse_term()
# #         # left_term = [op, left_term, right_term]
# #         left_term = {
# #             "type": "binary",
# #             "left": left_term,
# #             "operator": operator,
# #             "right": right_term,
# #         }
# #     return left_term


# # def parse_term():
# #     left_factor = parse_factor()
# #     while get_current_token() in ["*", "/"]:
# #         operator = get_current_token()
# #         consume_token()
# #         right_factor = parse_factor()
# #         # left_factor = [op, left_factor, right_factor]
# #         left_factor = {
# #             "type": "binary",
# #             "left": left_factor,
# #             "operator": operator,
# #             "right": right_factor,
# #         }
# #     return left_factor


# # def parse_arguments():
# #     arguments = []
# #     while get_current_token != ")":
# #         arguments.append(parse_expression())
# #         current_token = get_current_token()
# #         if current_token != ")":
# #             consume_token(",")
# #     return arguments


# # def parse_function_call(identifier):
# #     consume_token("(")
# #     arguments = parse_arguments()
# #     consume_token(")")
# #     return {"type": "function_call", "name": identifier, "arguments": arguments}


# # def parse_factor():
# #     current_token = get_current_token()
# #     if isinstance(current_token, list) and current_token[0] == "number":
# #         consume_token()
# #         return float(current_token[1])
# #     elif isinstance(current_token, list) and current_token[0] == "identifier":
# #         identifier = current_token[1]
# #         consume_token()
# #         if get_current_token() != "(":
# #             return {"type": "identifier", "name": identifier}
# #         parse_function_call(identifier)

# #     elif current_token == "-":
# #         operator = get_current_token()
# #         consume_token()  # Consume '-'
# #         factor = parse_factor()
# #         return {"type": "unary", "operator": operator, "expression": factor}
# #     elif current_token == "(":
# #         consume_token()  # Consume '('
# #         expression = parse_expression()
# #         if get_current_token() != ")":
# #             raise Exception("Expected ')'")
# #         consume_token()  # Consume ')'
# #         return expression
# #     else:
# #         raise Exception("Unexpected token in factor")

# def parse_factor(tokens):
#     current_token = tokens.current_token
#     if type(current_token) in [int, float]:
#         tokens.next_token()
#         return current_token
# #     if isinstance(current_token, list) and current_token[0] == "number":
# #         consume_token()
# #         return float(current_token[1])
# #     elif isinstance(current_token, list) and current_token[0] == "identifier":
# #         identifier = current_token[1]
# #         consume_token()
# #         if get_current_token() != "(":
# #             return {"type": "identifier", "name": identifier}
# #         parse_function_call(identifier)

# #     elif current_token == "-":
# #         operator = get_current_token()
# #         consume_token()  # Consume '-'
# #         factor = parse_factor()
# #         return {"type": "unary", "operator": operator, "expression": factor}
# #     elif current_token == "(":
# #         consume_token()  # Consume '('
# #         expression = parse_expression()
# #         if get_current_token() != ")":
# #             raise Exception("Expected ')'")
# #         consume_token()  # Consume ')'
# #         return expression
# #     else:
# #         raise Exception("Unexpected token in factor")

# def parse_term(tokens):
#     left_factor = parse_factor(tokens)
#     while tokens.current_token in ["*", "/"]:
#         operator = tokens.current_token
#         tokens.next_token()
#         right_factor = parse_factor(tokens)
#         left_factor = {
#             "type": "binary",
#             "left": left_factor,
#             "operator": operator,
#             "right": right_factor,
#         }
#     return left_factor


# def parse_expression(tokens):
#     left_term = parse_term(tokens)
#     while tokens.current_token in ["+", "-"]:
#         operator = tokens.current_token
#         tokens.next_token()
#         right_term = parse_term(tokens)
#         left_term = {
#             "type": "binary",
#             "left": left_term,
#             "operator": operator,
#             "right": right_term,
#         }
#     return left_term


# def parse_print_statement(tokens):
#     tokens.discard("#print")
#     expression = parse_expression()
#     tokens.discard(";")
#     return expression


# def parse_statement(tokens):
#     if tokens.current_token == "#print":
#         result = parse_print_statement(tokens)
#         tokens.discard(";")
#         return result


# #         consume_token()  # Consume 'print'
# #         expression = parse_expression()
# #         if get_current_token() != ";":
# #             raise Exception("Expected ';'")
# #         consume_token()
# #         # return ["print", expression]
# #         return {"type": "print", "expression": expression}

# #     if current_token == "if":
# #         consume_token()  # Consume 'if'
# #         if get_current_token() != "(":
# #             raise Exception("Expected '('")
# #         consume_token()
# #         condition = parse_expression()
# #         if get_current_token() != ")":
# #             raise Exception("Expected ')'")
# #         consume_token()
# #         then_statement = parse_statement()

# #         if get_current_token() == "else":
# #             consume_token()
# #             else_statement = parse_statement()
# #         else:
# #             else_statement = None

# #         return {
# #             "type": "if",
# #             "condition": condition,
# #             "then": then_statement,
# #             "else": else_statement,
# #         }

# #     if current_token == "while":
# #         consume_token()  # Consume 'while'
# #         if get_current_token() != "(":
# #             raise Exception("Expected '('")
# #         consume_token()
# #         condition = parse_expression()
# #         if get_current_token() != ")":
# #             raise Exception("Expected ')'")
# #         consume_token()
# #         do_statement = parse_statement()
# #         return {
# #             "type": "while",
# #             "condition": condition,
# #             "do": do_statement,
# #         }

# #     if type(current_token) is list and current_token[0] == "identifier":
# #         name = current_token[1]
# #         consume_token()
# #         if get_current_token() != "=":
# #             raise Exception("Expected '=' for assignment statement")
# #         consume_token()
# #         expression = parse_expression()
# #         if get_current_token() != ";":
# #             raise Exception("Expected ';'")
# #         consume_token()
# #         return {"type": "assignment", "name": name, "expression": expression}

# #     if current_token == "function":
# #         return parse_function_declaration()

# #     if current_token == "return":
# #         return parse_return_statement()

# #     if current_token == "{":
# #         return parse_block()

# #     raise Exception("Unexpected token in statement")


# def parse_program(tokens):
#     statements = []
#     while tokens.current_token is not None:
#         statements.append(parse_statement(tokens))
#     return {"type": "program", "statements": statements}


# def parse(program_tokens):
#     tokens = Tokens(program_tokens)
#     print(tokens.tokens)
#     return parse_program(tokens)


# from tokenizer import tokenize
# from pprint import pprint


# def test_parse():
#     print("testing parse")
#     program_tokens = tokenize("print 1+2; {print 3; print 4;}")
#     print(program_tokens)
#     assert program_tokens == [
#         "#print",
#         1,
#         "+",
#         2,
#         ";",
#         "{",
#         "#print",
#         3,
#         ";",
#         "#print",
#         4,
#         ";",
#         "}",
#     ]
#     ast = parse(program_tokens)
#     pprint(ast, sort_dicts=False)


# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {
# #                 "type": "print",
# #                 "expression": {
# #                     "type": "binary",
# #                     "left": 1.0,
# #                     "operator": "+",
# #                     "right": 2.0,
# #                 },
# #             },
# #             {
# #                 "type": "block",
# #                 "statements": [
# #                     {"type": "print", "expression": 3.0},
# #                     {"type": "print", "expression": 4.0},
# #                 ],
# #             },
# #         ],
# #     }


# # def test_parse_with_identifier():
# #     print("testing parse with identifier")
# #     program_tokens = tokenize("x=4;")
# #     print(program_tokens)
# #     ast = parse(program_tokens)
# #     print(ast)
# #     program_tokens = tokenize("print x+3;")
# #     print(program_tokens)
# #     ast = parse(program_tokens)
# #     print(ast)


# # def test_parse_unary_negation():
# #     print("testing parse unary negation")
# #     tokens = tokenize("print -2-2;")
# #     print(tokens)
# #     ast = parse(tokens)
# #     pprint(ast, sort_dicts=False)
# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {
# #                 "type": "print",
# #                 "expression": {
# #                     "type": "binary",
# #                     "left": {"type": "unary", "operator": "-", "expression": 2.0},
# #                     "operator": "-",
# #                     "right": 2.0,
# #                 },
# #             }
# #         ],
# #     }


# # def test_if_statement():
# #     tokens = tokenize("if (1) j = 2;")
# #     print(tokens)
# #     ast = parse(tokens)
# #     pprint(ast, sort_dicts=False)
# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {
# #                 "type": "if",
# #                 "condition": 1.0,
# #                 "then": {"type": "assignment", "name": "j", "expression": 2.0},
# #                 "else": None,
# #             }
# #         ],
# #     }
# #     tokens = tokenize("if (1) j = 2; else j = 0;")
# #     print(tokens)
# #     ast = parse(tokens)
# #     pprint(ast, sort_dicts=False)
# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {
# #                 "type": "if",
# #                 "condition": 1.0,
# #                 "then": {"type": "assignment", "name": "j", "expression": 2.0},
# #                 "else": {"type": "assignment", "name": "j", "expression": 0.0},
# #             }
# #         ],
# #     }
# #     tokens = tokenize("if (1) {j=1; k=2;} else {j=0; k=1;}")
# #     print(tokens)
# #     ast = parse(tokens)
# #     pprint(ast, sort_dicts=False)
# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {
# #                 "type": "if",
# #                 "condition": 1.0,
# #                 "then": {
# #                     "type": "block",
# #                     "statements": [
# #                         {"type": "assignment", "name": "j", "expression": 1.0},
# #                         {"type": "assignment", "name": "k", "expression": 2.0},
# #                     ],
# #                 },
# #                 "else": {
# #                     "type": "block",
# #                     "statements": [
# #                         {"type": "assignment", "name": "j", "expression": 0.0},
# #                         {"type": "assignment", "name": "k", "expression": 1.0},
# #                     ],
# #                 },
# #             }
# #         ],
# #     }


# # def test_while_statement():
# #     tokens = tokenize("k = 3; while (k) k = k - 1;")
# #     ast = parse(tokens)
# #     # pprint(ast, sort_dicts=False)
# #     assert ast == {
# #         "type": "program",
# #         "statements": [
# #             {"type": "assignment", "name": "k", "expression": 3.0},
# #             {
# #                 "type": "while",
# #                 "condition": {"type": "identifier", "name": "k"},
# #                 "do": {
# #                     "type": "assignment",
# #                     "name": "k",
# #                     "expression": {
# #                         "type": "binary",
# #                         "left": {"type": "identifier", "name": "k"},
# #                         "operator": "-",
# #                         "right": 1.0,
# #                     },
# #                 },
# #             },
# #         ],
# #     }


# # def test_function_declaration():
# #     tokens = tokenize("function add(x,y) {return x;}")
# #     print(tokens)
# #     ast = parse(tokens)


    # test_parse_with_identifier()
    # test_parse_unary_negation()
    # test_parse_assignment() ### TODO ###
    # test_if_statement()
    # test_while_statement()
    # test_function_declaration()
