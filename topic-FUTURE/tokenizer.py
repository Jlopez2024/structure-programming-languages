import re

def tokenize(source_code):
    token_patterns = [
        (r'\s+', None),                      # Whitespace
        (r'[0-9]+(\.[0-9]+)?', "number"),    # Numbers
        (r'\+', "+"),                        # Plus operator
        (r'-', "-"),                         # Minus operator
        (r'\*', "*"),                        # Multiplication operator
        (r'/', "/"),                         # Division operator
        (r'\(', "("),                        # Left parenthesis
        (r'\)', ")"),                        # Right parenthesis
        (r'{', "{"),                         # Left brace
        (r'}', "}"),                         # Right brace
        (r';', ";"),                         # Semicolon
        (r'print', "print"),                 # print keyword
        (r'if', "if"),                       # if keyword
        (r'else', "else"),                   # else keyword
        (r'while', "while"),                 # while keyword
        (r'==', "=="),                       # Equality operator
        (r'!=', "!="),                       # Inequality operator
        (r'<=', "<="),                       # Less than or equal to operator
        (r'>=', ">="),                       # Greater than or equal to operator
        (r'<', "<"),                         # Less than operator
        (r'>', ">"),                         # Greater than operator
        (r'=', "="),                         # Assignment operator
        (r'\[', "["),                        # Left square bracket
        (r'\]', "]"),                        # Right square bracket
        (r',', ","),                         # Comma
        (r'"([^"]|"")*"', "string"),         # String literals
        (r'[a-zA-Z_][a-zA-Z0-9_]*', "identifier"),  # Identifiers
    ]

    tokens = []
    i = 0
    while i < len(source_code):
        matched = False
        for pattern, tag in token_patterns:
            match = re.match(pattern, source_code[i:])
            if match:
                value = match.group(0)
                if tag:  # Only add non-whitespace tokens
                    if tag == "number":
                        tokens.append(["number", float(value) if '.' in value else int(value)])
                    elif tag == "string":
                        # Replacing doubled quotes with a solitary quote mark
                        processed_value = value[1:-1].replace('""', '"')
                        tokens.append(["string", processed_value])
                    else:
                        tokens.append(value)
                i += len(value)
                matched = True
                break
        if not matched:
            raise Exception(f"Invalid token at position {i}")
    
    return tokens

# Example usage:
source_code = 'print "Hello, World!"; x = "Say ""hi"" again";'
print(tokenize(source_code))
