from itertools import product
from Token import *


def createAllRegisters(word: str) -> [str]:
    combinations = [''.join(p) for p in product(*[(char.lower(), char.upper()) for char in word])]

    return '|'.join(combinations)

SEMICOLON = "<ES>"
LEFT_PAREN_BRACKET = "<LRB>"
RIGHT_ROUND_BRACKET = "<RRB>"
PLUS = "<PLUS>"
MULT = "<MULT>"

UNDERLINE = "_"
ALL_DIGIT_WITHOUT_ZERO = "1|2|3|4|5|6|7|8|9"
ALL_DIGIT = f"0|{ALL_DIGIT_WITHOUT_ZERO}"
ALL_LET_LOWER = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_LET_UPPER = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_LET = ALL_LET_LOWER + "|" + ALL_LET_UPPER
ALL_SPEC_SYM = " |:|=|.|&" + "|" + SEMICOLON
ALL_SYM = ALL_LET + "|" + ALL_DIGIT
ALL_SYM_WITH_SPEC = ALL_LET + "|" + ALL_DIGIT + "|" + ALL_SPEC_SYM

tokenIdToRegMap = {
    TokenType.PROGRAM_TOKEN: Token(TokenType.PROGRAM_TOKEN, "(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m)"),
    TokenType.VAR_TOKEN: Token(TokenType.VAR_TOKEN, "(V|v)(A|a)(R|r)"),
    TokenType.BEGIN_TOKEN: Token(TokenType.BEGIN_TOKEN, "(B|b)(E|e)(G|g)(I|i)(N|n)"),
    TokenType.END_TOKEN: Token(TokenType.END_TOKEN, "(E|e)(N|n)(D|d)"),
    TokenType.OF_TOKEN: Token(TokenType.OF_TOKEN, "(O|o)(F|f)"),
    TokenType.ARRAY_TOKEN: Token(TokenType.ARRAY_TOKEN, "(A|a)(R|r)(R|r)(A|a)(Y|y)"),
    TokenType.IF_TOKEN: Token(TokenType.IF_TOKEN, "(I|i)(F|f)"),
    TokenType.OR_TOKEN: Token(TokenType.OR_TOKEN, "(O|o)(R|r)"),
    TokenType.PROCEDURE_TOKEN: Token(TokenType.PROCEDURE_TOKEN, "(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e)"),
    TokenType.THEN_TOKEN: Token(TokenType.THEN_TOKEN, "(T|t)(H|h)(E|e)(N|n)"),
    TokenType.ELSE_TOKEN: Token(TokenType.ELSE_TOKEN, "(E|e)(L|l)(S|s)(E|e)"),
    TokenType.TYPE_KEY_TOKEN: Token(TokenType.TYPE_TOKEN, "(T|t)(Y|y)(P|p)(E|e)"),

    TokenType.FUNC_TOKEN: Token(TokenType.FUNC_TOKEN, "WRITE|READ|WRITELN|READLN"),
    TokenType.TYPE_TOKEN: Token(TokenType.TYPE_TOKEN, "BOOLEAN|STRING|TEXT|FLOAT|INTEGER"),
    TokenType.LITERAL_TOKEN: Token(TokenType.LITERAL_TOKEN, "'" + "(" + ALL_SYM + ")" + "*" + "'"),
    TokenType.INTEGER_TOKEN: Token(TokenType.INTEGER_TOKEN, f"(-(({ALL_DIGIT})+))|((({ALL_DIGIT})+))"),
    TokenType.BOOLEAN_TOKEN: Token(TokenType.BOOLEAN_TOKEN, "TRUE|true|True|FALSE|False|false"),
    TokenType.IDENTIFIER_TOKEN: Token(TokenType.IDENTIFIER_TOKEN, "(" + UNDERLINE + "|" + ALL_LET_LOWER + ")" + "(" + UNDERLINE + "|" + ALL_SYM + ")" + "*"),
    TokenType.FLOAT_TOKEN: Token(TokenType.FLOAT_TOKEN, f"(-(({ALL_DIGIT})+).(({ALL_DIGIT})+))|((({ALL_DIGIT})+).(({ALL_DIGIT})+))"),
    TokenType.COMMENT_TOKEN: Token(TokenType.COMMENT_TOKEN, "({)" + f"({ALL_SYM_WITH_SPEC})*" + "(})"),
    TokenType.LINE_COMMENT_TOKEN: Token(TokenType.LINE_COMMENT_TOKEN, "(//)" + f"({ALL_SYM_WITH_SPEC})*"),

    TokenType.DOT_TOKEN: Token(TokenType.DOT_TOKEN, "."),
    TokenType.ASSIGN_TOKEN: Token(TokenType.ASSIGN_TOKEN, ":="),
    TokenType.SEMICOLON_TOKEN: Token(TokenType.SEMICOLON_TOKEN, SEMICOLON),
    TokenType.MULTIPLICATION_TOKEN: Token(TokenType.MULTIPLICATION_TOKEN, "*"),
    TokenType.PLUS_TOKEN: Token(TokenType.PLUS_TOKEN, "+"),
    TokenType.MINUS_TOKEN: Token(TokenType.MINUS_TOKEN, "-"),
    TokenType.DIVIDE_TOKEN: Token(TokenType.DIVIDE_TOKEN, "/"),
    TokenType.COMMA_TOKEN: Token(TokenType.COMMA_TOKEN, ","),
    TokenType.LEFT_PAREN_TOKEN: Token(TokenType.LEFT_PAREN_TOKEN, "("),
    TokenType.RIGHT_PAREN_TOKEN: Token(TokenType.RIGHT_PAREN_TOKEN, ")"),
    TokenType.LEFT_BRACKET_TOKEN: Token(TokenType.LEFT_BRACKET_TOKEN, "["),
    TokenType.RIGHT_BRACKET_TOKEN: Token(TokenType.RIGHT_BRACKET_TOKEN, "]"),
    TokenType.EQ_TOKEN: Token(TokenType.EQ_TOKEN, "="),
    TokenType.GREATER_TOKEN: Token(TokenType.GREATER_TOKEN, ">"),
    TokenType.LESS_TOKEN: Token(TokenType.LESS_TOKEN, "<"),
    TokenType.LESS_EQ_TOKEN: Token(TokenType.LESS_EQ_TOKEN, "<="),
    TokenType.GREATER_EQ_TOKEN: Token(TokenType.GREATER_EQ_TOKEN, ">="),
    TokenType.NOT_EQ_TOKEN: Token(TokenType.NOT_EQ_TOKEN, "<>"),
    TokenType.COLON_TOKEN: Token(TokenType.COLON_TOKEN, ":")
}

SpaceToken = EmptyToken(" ")
ColonToken = EmptyToken(":")
TabToken = EmptyToken("(    )")
SpacesToken = EmptyToken("( )*")
LeftRoundBracketToken = EmptyToken(LEFT_PAREN_BRACKET)
RightRoundBracketToken = EmptyToken(RIGHT_ROUND_BRACKET)

ProgramToken = ConcreteToken(tokenIdToRegMap[TokenType.PROGRAM_TOKEN], "PROGRAM")
VarToken = ConcreteToken(tokenIdToRegMap[TokenType.VAR_TOKEN], "VAR")
BeginToken = ConcreteToken(tokenIdToRegMap[TokenType.BEGIN_TOKEN], "BEGIN")
EndToken = ConcreteToken(tokenIdToRegMap[TokenType.END_TOKEN], "END")
OfToken = ConcreteToken(tokenIdToRegMap[TokenType.OF_TOKEN], "OF")
ArrayTypeToken = ConcreteToken(tokenIdToRegMap[TokenType.ARRAY_TOKEN], "ARRAY")
ElseToken = ConcreteToken(tokenIdToRegMap[TokenType.ELSE_TOKEN], "ELSE")
IfToken = ConcreteToken(tokenIdToRegMap[TokenType.IF_TOKEN], "IF")
OrToken = ConcreteToken(tokenIdToRegMap[TokenType.OR_TOKEN], "OR")
ProcedureToken = ConcreteToken(tokenIdToRegMap[TokenType.PROCEDURE_TOKEN], "PROCEDURE")
ThenToken = ConcreteToken(tokenIdToRegMap[TokenType.THEN_TOKEN], "THEN")
TypeKeyToken = ConcreteToken(tokenIdToRegMap[TokenType.TYPE_KEY_TOKEN], "TYPE")

TypeToken = tokenIdToRegMap[TokenType.TYPE_TOKEN]

IDToken = tokenIdToRegMap[TokenType.IDENTIFIER_TOKEN]

IntegerToken = tokenIdToRegMap[TokenType.INTEGER_TOKEN]
BoolToken = tokenIdToRegMap[TokenType.BOOLEAN_TOKEN]

LiteralToken = tokenIdToRegMap[TokenType.LITERAL_TOKEN]

WriteToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "WRITE")
ReadToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "READ")
WritelnToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "WRITELN")
ReadlnToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "READLN")

CommentToken = tokenIdToRegMap[TokenType.COMMENT_TOKEN]
LineCommentToken = tokenIdToRegMap[TokenType.LINE_COMMENT_TOKEN]
FloatToken = tokenIdToRegMap[TokenType.FLOAT_TOKEN]

DotToken = tokenIdToRegMap[TokenType.DOT_TOKEN]
AssignToken = tokenIdToRegMap[TokenType.ASSIGN_TOKEN]
EndLineToken = ConcreteToken(tokenIdToRegMap[TokenType.SEMICOLON_TOKEN], SEMICOLON)
MultiplicationToken = tokenIdToRegMap[TokenType.MULTIPLICATION_TOKEN]
PlusToken = tokenIdToRegMap[TokenType.PLUS_TOKEN]
MinusToken = tokenIdToRegMap[TokenType.MINUS_TOKEN]
DivideToken = tokenIdToRegMap[TokenType.DIVIDE_TOKEN]
CommaToken = tokenIdToRegMap[TokenType.COMMA_TOKEN]
LeftParenToken = tokenIdToRegMap[TokenType.LEFT_PAREN_TOKEN]
RightParenToken = tokenIdToRegMap[TokenType.RIGHT_PAREN_TOKEN]
LeftBracketToken = tokenIdToRegMap[TokenType.LEFT_BRACKET_TOKEN]
RightBracketToken = tokenIdToRegMap[TokenType.RIGHT_BRACKET_TOKEN]
EqToken = tokenIdToRegMap[TokenType.EQ_TOKEN]
GreaterToken = tokenIdToRegMap[TokenType.GREATER_TOKEN]
LessToken = tokenIdToRegMap[TokenType.LESS_TOKEN]
LessEqToken = tokenIdToRegMap[TokenType.LESS_EQ_TOKEN]
GreaterEqToken = tokenIdToRegMap[TokenType.GREATER_EQ_TOKEN]
NotEqToken = tokenIdToRegMap[TokenType.NOT_EQ_TOKEN]