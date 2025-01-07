import Reader
import Expressions
import TokenType
import sys

if __name__ == "__main__":

    if len(sys.argv) not in {3, 4}:
        print("main.py <inFile> <outFile>")
        sys.exit(1)

    inFile = sys.argv[1]
    outFile = sys.argv[2]

    if len(sys.argv) == 4:
        inFile = sys.argv[2]
        outFile = sys.argv[3]

    reader = Reader.Reader(Expressions.expressions, outFile)

    with open('./data/Lexer/in.txt', 'r', encoding='utf-8') as f:
        data = f.read()

        data = data.replace(";", TokenType.SEMICOLON)
        data = data.replace("(", TokenType.LEFT_PAREN_BRACKET)
        data = data.replace(")", TokenType.RIGHT_ROUND_BRACKET)
        data = data.replace("+", TokenType.PLUS)
        data = data.replace("*", TokenType.MULT)

        reader.handle(data)
