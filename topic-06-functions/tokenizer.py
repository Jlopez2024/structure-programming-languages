import re

patterns = [
    [r"//.*\n", None],  # 
    [r"\s+", None],  # Whitespace
    [r"print", "#print"],  # print keyword
    [r"if", "#if"],  # if keyword
    [r"else", "#else"],  # else keyword
    [r"while", "#while"],  # while keyword
    [r"function", "#function"],  # function keyword
    [r"return", "#return"],  # return keyword
    [r"\+", "+"],
    [r"-", "-"],
    [r"\*", "*"],
    [r"/", "/"],
    [r"\(", "("],
    [r"\)", ")"],
    [r"\{", "{"],
    [r"\}", "}"],
    [r"\;", ";"],
    [r"==", "=="],
    [r"!=", "!="],
    [r"<=", "<="],
    [r">=", ">="],
    [r"<", "<"],
    [r">", ">"],
    [r"=", "="],
    [r"\.", "."],
    [r"\[", "["],
    [r"\]", "]"],
    [r",", ","],
    [r"\;", ";"],
    [r"\d+(\.\d*)?", "number"],  # numeric literals
    [r'"([^"]|"")*"', "string"],  # string literals
    [r"[a-zA-Z_][a-zA-Z0-9_]*", "identifier"],  # identifiers
    [r".", "error"],  # unexpected content
]


# general numeric literal conversion
def number(s):
    if "." in s:
        return float(s)
    else:
        return int(s)


# simple list class to hold token buffer
class List:
    def __init__(this, tokens):
        assert type(tokens) is list
        this.list = tokens

    def current(this):
        try:
            return this.list[0]
        except:
            return None

    def discard(this, token=None):
        if token:
            assert this.list[0] == token
        this.list = this.list[1:]


# The lex/tokenize function
def tokenize(characters):
    characters = characters + '\n'
    tokens = []
    pos = 0
    while pos < len(characters):
        for regex, token in patterns:
            pattern = re.compile(regex)
            match = pattern.match(characters, pos)
            if match:
                break
        assert match  # this should never fail
        pos = match.end()
        if token == None:
            continue
        assert token != "error", "Syntax error: illegal character at " + match.group(0)
        if token == "number":
            tokens.append(number(match.group(0)))
            continue
        if token == "string":
            # omit closing and beginning strings, replace two quotes with one quote
            tokens.append("$" + match.group(0)[1:-1].replace('""', '"'))
            continue
        if token == "identifier":
            tokens.append("@" + match.group(0))
            continue
        tokens.append(token)
    return List(tokens)


def test_simple_tokens():
    print("testing simple tokens")
    examples = ".,[,],+,-,*,/,(,),{,},;".split(",")
    for example in examples:
        assert tokenize(example).list == [example]


def test_number_tokens():
    print("testing number tokens")
    for s in ["1", "22", "12.1", "0", "12.", "123145"]:
        assert tokenize(s).list == [number(s)]


def test_string_tokens():
    print("testing string tokens")
    for s in ['"example"', '"this is a longer example"', '"an embedded "" quote"']:
        # adjust for the embedded quote behaviour
        r = "$" + s[1:-1].replace('""', '"')
        assert tokenize(s).list == [r], f"Expected {[r]}, got {[tokenize(s)]}."


def test_identifier_tokens():
    print("testing identifier tokens")
    for s in ["x", "y", "z", "alpha", "beta", "gamma"]:
        assert tokenize(s).list == ["@" + s]


def test_whitespace():
    print("testing whitespace")
    for s in ["1", "1  ", "  1", "  1  "]:
        assert tokenize(s).list == [1]


def test_multiple_tokens():
    print("testing multiple tokens")
    assert tokenize("1+2").list == [1, "+", 2]
    assert tokenize("1+2-3").list == [1, "+", 2, "-", 3]
    assert tokenize("3+4*(5-2)").list == [
        3,
        "+",
        4,
        "*",
        "(",
        5,
        "-",
        2,
        ")",
    ]
    assert tokenize("3+4*(5-2)").list == tokenize("3 + 4 * (5 - 2)").list
    assert tokenize("3+4*(5-2)").list == tokenize("  3  +  4 * (5 - 2)  ").list
    assert tokenize("3+4*(5-2)").list == tokenize(" 3 + 4 * (5 - 2) ").list


def test_keywords():
    print("testing keywords")
    for keyword in ["print", "if", "else", "while", "function", "return"]:
        assert tokenize(keyword).list == ["#" + keyword]

def test_comments():
    print("testing comments")
    assert tokenize("//comment\n").list == tokenize("\n").list
    assert tokenize("alpha//comment\n").list == tokenize("alpha\n").list
    assert tokenize("1+5  //comment\n").list == tokenize("1+5  \n").list
    assert tokenize('"beta"//comment\n').list == tokenize('"beta"\n').list


def test_list_class():
    tokens = List(["#print", 3, "+", 4, "*", "(", 5, "-", 2, ")", ";"])
    assert tokens.list == ["#print", 3, "+", 4, "*", "(", 5, "-", 2, ")", ";"]
    assert tokens.current() == "#print"
    tokens.discard()
    assert tokens.list == [3, "+", 4, "*", "(", 5, "-", 2, ")", ";"]
    assert tokens.current() == 3
    tokens.discard()
    assert tokens.list == ["+", 4, "*", "(", 5, "-", 2, ")", ";"]
    assert tokens.current() == "+"
    tokens.list=[1]
    assert tokens.current() == 1
    for i in range(0,3):
        tokens.discard()
        assert tokens.current() == None


if __name__ == "__main__":
    test_simple_tokens()
    test_number_tokens()
    test_string_tokens()
    test_identifier_tokens()
    test_whitespace()
    test_multiple_tokens()
    test_keywords()
    test_comments()
    test_list_class()
    print(tokenize("print 3+4*(5-2);").list)
    print(tokenize("\"x\"=y+1;").list)

