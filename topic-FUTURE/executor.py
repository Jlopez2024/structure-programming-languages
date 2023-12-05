environment = {}

def execute(ast):
    if ast["type"] == "program":
        for statement in ast["body"]:
            execute(statement)
    elif ast["type"] == "print_statement":
        for expr in ast["expressions"]:
            print(evaluate(expr), end=' ')
        print()
    elif ast["type"] == "assignment":
        environment[ast["name"]] = evaluate(ast["value"])
    elif ast["type"] == "array_assignment":
        name = ast["name"]
        index = evaluate(ast["index"])
        value = evaluate(ast["value"])
        environment[name][index] = value
    elif ast["type"] == "if_statement":
        if evaluate(ast["condition"]):
            execute(ast["true_branch"])
        elif ast["false_branch"]:
            execute(ast["false_branch"])
    elif ast["type"] == "while_statement":
        while evaluate(ast["condition"]):
            execute(ast["body"])
    elif ast["type"] == "block":
        for statement in ast["body"]:
            execute(statement)
    else:
        raise Exception(f"Unexpected AST node type {ast['type']}")

def evaluate(ast):
    if ast["type"] == "number":
        return ast["value"]
    elif ast["type"] == "string":
        return ast["value"]
    elif ast["type"] == "identifier":
        return environment[ast["name"]]
    elif ast["type"] == "additive":
        left = evaluate(ast["left"])
        right = evaluate(ast["right"])
        if ast["operator"] == "+":
            return left + right
        elif ast["operator"] == "-":
            return left - right
    elif ast["type"] == "multiplicative":
        left = evaluate(ast["left"])
        right = evaluate(ast["right"])
        if ast["operator"] == "*":
            return left * right
        elif ast["operator"] == "/":
            return left / right
    elif ast["type"] == "conditional":
        left = evaluate(ast["left"])
        right = evaluate(ast["right"])
        if ast["operator"] == "<":
            return left < right
        elif ast["operator"] == ">":
            return left > right
        elif ast["operator"] == "==":
            return left == right
        elif ast["operator"] == "!=":
            return left != right
        elif ast["operator"] == "<=":
            return left <= right
        elif ast["operator"] == ">=":
            return left >= right
    elif ast["type"] == "array":
        return [evaluate(element) for element in ast["elements"]]
    elif ast["type"] == "array_access":
        return environment[ast["name"]][evaluate(ast["index"])]
    else:
        raise Exception(f"Unexpected AST node type {ast['type']} for evaluation")

# Example of using this execution engine:
source_code = """
print "Hello", 3+4;
x = [1, 2, 3];
print x[1];
y = x[1];
print y;
"""

tokens = tokenize(source_code)
ast = parse_program()
execute(ast)


----

NEW

def execute(ast, environment={}):
    if ast["type"] == "program":
        for stmt in ast["body"]:
            execute(stmt, environment)

    elif ast["type"] == "number":
        return ast["value"]

    elif ast["type"] == "string":
        return ast["value"]

    elif ast["type"] == "binary":
        left = execute(ast["left"], environment)
        right = execute(ast["right"], environment)
        return binary_operation(ast["operator"], left, right)

    elif ast["type"] == "assignment":
        value = execute(ast["value"], environment)
        environment[ast["name"]] = value

    elif ast["type"] == "identifier":
        if ast["name"] in environment:
            return environment[ast["name"]]
        else:
            raise Exception(f"Unbound variable: {ast['name']}")

    elif ast["type"] == "print":
        for expr in ast["expressions"]:
            print(execute(expr, environment))

    elif ast["type"] == "if":
        condition = execute(ast["condition"], environment)
        if condition:
            execute(ast["if_body"], environment)
        elif ast["else_body"]:
            execute(ast["else_body"], environment)

    elif ast["type"] == "while":
        condition = execute(ast["condition"], environment)
        while condition:
            execute(ast["body"], environment)
            condition = execute(ast["condition"], environment)

    elif ast["type"] == "block":
        for stmt in ast["body"]:
            execute(stmt, environment)

    elif ast["type"] == "array_access":
        array = environment.get(ast["name"], [])
        index = execute(ast["index"], environment)
        return array[index]

    else:
        raise Exception(f"Unknown AST node type: {ast['type']}")

def binary_operation(op, left, right):
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        if right == 0:
            raise Exception("Division by zero!")
        return left / right
    elif op == "<":
        return left < right
    elif op == "<=":
        return left <= right
    elif op == ">":
        return left > right
    elif op == ">=":
        return left >= right
    elif op == "==":
        return left == right
    elif op == "!=":
        return left != right
    else:
        raise Exception(f"Unsupported binary operator: {op}")

-------

Version 3

--------

def execute(ast, environment=None):
    if environment is None:
        environment = {}
    
    # Define functions for each type of AST node.
    def execute_number(node):
        return node["value"]
    
    def execute_string(node):
        return node["value"]

    def execute_identifier(node):
        return environment[node["name"]]

    def execute_assignment(node):
        value = execute(node["value"], environment)
        environment[node["name"]] = value
        return value

    def execute_binary(node):
        left = execute(node["left"], environment)
        right = execute(node["right"], environment)
        operator = node["operator"]
        return eval(f"{left} {operator} {right}")

    def execute_array_access(node):
        array = environment[node["name"]]
        index = execute(node["index"], environment)
        return array[index]

    def execute_print(node):
        for expr in node["expressions"]:
            print(execute(expr, environment), end=" ")
        print()

    def execute_if(node):
        condition = execute(node["condition"], environment)
        if condition:
            execute(node["if_body"], environment)
        elif node["else_body"]:
            execute(node["else_body"], environment)
    
    def execute_while(node):
        while execute(node["condition"], environment):
            execute(node["body"], environment)
    
    def execute_block(node):
        # Create a new environment for the block
        new_environment = environment.copy()
        for stmt in node["body"]:
            execute(stmt, new_environment)
    
    # Node type to function mapping
    node_type_mapping = {
        "number": execute_number,
        "string": execute_string,
        "identifier": execute_identifier,
        "assignment": execute_assignment,
        "binary": execute_binary,
        "array_access": execute_array_access,
        "print": execute_print,
        "if": execute_if,
        "while": execute_while,
        "block": execute_block,
    }

    # Execute the AST
    node_type = ast["type"]
    if node_type in node_type_mapping:
        return node_type_mapping[node_type](ast)
    else:
        raise ValueError(f"Unknown node type {node_type}")

----------

Version 4


def execute(node, environment=None):
    if environment is None:
        environment = {}

    if node["type"] == "number":
        return node["value"]

    if node["type"] == "string":
        return node["value"]

    if node["type"] == "identifier":
        return environment[node["name"]]

    if node["type"] == "assignment":
        value = execute(node["value"], environment)
        environment[node["name"]] = value
        return value

    if node["type"] == "binary":
        left = execute(node["left"], environment)
        right = execute(node["right"], environment)
        operator = node["operator"]
        return eval(f"{left} {operator} {right}")

    if node["type"] == "array_access":
        array = environment[node["name"]]
        index = execute(node["index"], environment)
        return array[index]

    if node["type"] == "print":
        for expr in node["expressions"]:
            print(execute(expr, environment), end=" ")
        print()

    if node["type"] == "if":
        condition = execute(node["condition"], environment)
        if condition:
            execute(node["if_body"], environment)
        elif "else_body" in node:
            execute(node["else_body"], environment)

    if node["type"] == "while":
        while execute(node["condition"], environment):
            execute(node["body"], environment)

    if node["type"] == "block":
        # Create a new environment for the block
        new_environment = environment.copy()
        for stmt in node["body"]:
            execute(stmt, new_environment)

    return None  # Explicit return for clarity

