import parser
import tokenizer
from pprint import pprint

def test_parse_factor():
    tokens = parser.Tokens(tokenizer.tokenize("3"))
    print(tokens)
    ast=parser.parse_factor(tokens)
    pprint(ast)

if __name__ == "__main__":
    test_parse_factor()
