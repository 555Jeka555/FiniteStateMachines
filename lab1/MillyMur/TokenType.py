from itertools import product
from Token import *


def createAllRegisters(word: str) -> [str]:
    combinations = [''.join(p) for p in product(*[(char.lower(), char.upper()) for char in word])]

    return '|'.join(combinations)

SEMICOLON = "<ES>"
LEFT_ROUND_BRACKET = "<LRB>"
RIGHT_ROUND_BRACKET = "<RRB>"
ALL_DIGIT = "0|1|2|3|4|5|6|7|8|9"
ALL_DIGIT_WITHOUT_ZERO = "1|2|3|4|5|6|7|8|9"
ALL_LET_LOWER = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_LET_UPPER = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_LET = ALL_LET_LOWER + "|" + ALL_LET_UPPER
ALL_SPEC_SYM = " |:|=|.|&" + "|" + SEMICOLON
ALL_SYM = ALL_LET + "|" + ALL_DIGIT
ALL_SYM_WITH_SPEC = ALL_LET + "|" + ALL_DIGIT + "|" + ALL_SPEC_SYM

tokenIdToRegMap = {
    # TokenType.KEY_WORD_TOKEN: Token(TokenType.KEY_WORD_TOKEN,
    #                                     f"{createAllRegisters('PROGRAM')}|"
    #                                     f"{createAllRegisters('VAR')}|"
    #                                     f"{createAllRegisters('BEGIN')}|"
    #                                     f"{createAllRegisters('END')}|"
    #                                     f"{createAllRegisters('OF')}|"
    #                                     f"{createAllRegisters('ARRAY')}|"
    #                                     f"{createAllRegisters('IF')}|"
    #                                     f"{createAllRegisters('OR')}|"
    #                                     f"{createAllRegisters('PROCEDURE')}|"
    #                                     f"{createAllRegisters('THEN')}|"
    #                                     f"{createAllRegisters('ELSE')}|"
    #                                     f"{createAllRegisters('TYPE')}|"
    #                                     ),
    TokenType.KEY_WORD_TOKEN: Token(TokenType.KEY_WORD_TOKEN,
                                    "PROGRAM|"
                                    "VAR|"
                                    "BEGIN|"
                                    "END|"
                                    "OF|"
                                    "ARRAY|"
                                    "IF|"
                                    "OR|"
                                    "PROCEDURE|"
                                    "THEN|"
                                    "ELSE|"
                                    "TYPE"
                                    ),
    TokenType.FUNC_TOKEN: Token(TokenType.FUNC_TOKEN, "WRITE|READ|WRITELN|READLN"),
    TokenType.TYPE_TOKEN: Token(TokenType.TYPE_TOKEN, "BOOLEAN|STRING|TEXT|REAL|INTEGER"),
    TokenType.LITERAL_TOKEN: Token(TokenType.LITERAL_TOKEN, "'" + "(" + ALL_SYM + ")" + "*" + "'"),
    TokenType.INTEGER_TOKEN: Token(TokenType.INTEGER_TOKEN, f"(-({ALL_DIGIT})|(-({ALL_DIGIT_WITHOUT_ZERO})({ALL_DIGIT})+))|(({ALL_DIGIT})|(({ALL_DIGIT_WITHOUT_ZERO})({ALL_DIGIT})+))"),
    TokenType.BOOLEAN_TOKEN: Token(TokenType.BOOLEAN_TOKEN, "TRUE|true|True|FALSE|False|false"),
    TokenType.IDENTIFIER_TOKEN: Token(TokenType.IDENTIFIER_TOKEN, "(" + ALL_LET_LOWER + ")" + "(" + ALL_SYM + ")" + "*"),
    TokenType.FLOAT_TOKEN: Token(TokenType.FLOAT_TOKEN, f"(-(({ALL_DIGIT})+).(({ALL_DIGIT})+))|((({ALL_DIGIT})+).(({ALL_DIGIT})+))"),
    TokenType.COMMENT_TOKEN: Token(TokenType.COMMENT_TOKEN, "({)" + f"({ALL_SYM_WITH_SPEC})*" + "(})"),
    TokenType.LINE_COMMENT_TOKEN: Token(TokenType.LINE_COMMENT_TOKEN, "(//)" + f"({ALL_SYM_WITH_SPEC})*"),
    TokenType.DIMENSION_OF_ARRAY_TOKEN: Token(TokenType.DIMENSION_OF_ARRAY_TOKEN, f"[({ALL_DIGIT_WITHOUT_ZERO})+(..)({ALL_DIGIT_WITHOUT_ZERO})({ALL_DIGIT})*]"),
    TokenType.ARRAY_INDEX_TOKEN: Token(TokenType.ARRAY_INDEX_TOKEN, f"[({ALL_SYM})+]"),

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
LeftRoundBracketToken = EmptyToken(LEFT_ROUND_BRACKET)
RightRoundBracketToken = EmptyToken(RIGHT_ROUND_BRACKET)

ProgramToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "PROGRAM")
VarToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "VAR")
BeginToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "BEGIN")
ArrayTypeToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "ARRAY")
EndToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "END")
OfToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "OF")
ElseToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "ELSE")
IfToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "IF")
OrToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "OR")
ProcedureToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "PROCEDURE")
ThenToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "THEN")
TypeKeyToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "TYPE")

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

DimensionToken = tokenIdToRegMap[TokenType.DIMENSION_OF_ARRAY_TOKEN]
ArrayIndexToken = tokenIdToRegMap[TokenType.ARRAY_INDEX_TOKEN]

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