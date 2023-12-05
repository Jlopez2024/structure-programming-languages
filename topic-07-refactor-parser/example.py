# example demonstration code for a feature

# get the pprint module to print nicely formatted
from pprint import pprint

# import the language system
from tokenizer import tokenize
from parser import parse

code = """

if (x) {
    print("true")
} else {
    print("false")
}

"""

ast = parse(tokenize(code))
pprint(ast)
