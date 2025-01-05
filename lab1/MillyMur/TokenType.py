from Token import *

ALL_DIGIT = "0|1|2|3|4|5|6|7|8|9"
ALL_DIGIT_WITHOUT_ZERO = "1|2|3|4|5|6|7|8|9"
ALL_LET_LOWER = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ALL_LET_UPPER = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
ALL_LET = ALL_LET_LOWER + "|" + ALL_LET_UPPER
ALL_SPEC_SYM = " |:|=|.|&"
ALL_SYM = ALL_LET + "|" + ALL_DIGIT
ALL_SYM_WITH_SPEC = ALL_LET + "|" + ALL_DIGIT + "|" + ALL_SPEC_SYM

tokenIdToRegMap = {
    TokenType.KEY_WORD_TOKEN: Token(TokenType.KEY_WORD_TOKEN, "VAR|BEGIN|END"),
    TokenType.FUNC_TOKEN: Token(TokenType.FUNC_TOKEN, "WRITE|READ|WRITELN|READLN"),
    TokenType.TYPE_TOKEN: Token(TokenType.TYPE_TOKEN, "BOOLEAN|STRING|TEXT|FLOAT|INTEGER"),
    TokenType.LITERAL_TOKEN: Token(TokenType.LITERAL_TOKEN, "'" + "(" + ALL_SYM + ")" + "*" + "'"),
    TokenType.INTEGER_TOKEN: Token(TokenType.INTEGER_TOKEN,  "(" + ALL_DIGIT + ")" + "|" + "(" + "(" + ALL_DIGIT_WITHOUT_ZERO + ")" + "(" + ALL_DIGIT + ")" + "+" + ")"),
    TokenType.BOOLEAN_TOKEN: Token(TokenType.BOOLEAN_TOKEN, "TRUE|true|True|FALSE|False|false"),
    TokenType.SEPARATOR_TOKEN: Token(TokenType.SEPARATOR_TOKEN, "&"),
    TokenType.DOT_TOKEN: Token(TokenType.DOT_TOKEN, "."),
    TokenType.IDENTIFIER_TOKEN: Token(TokenType.IDENTIFIER_TOKEN, "(" + ALL_LET_LOWER + ")" + "(" + ALL_SYM + ")" + "*"),
    TokenType.ASSIGN_TOKEN: Token(TokenType.ASSIGN_TOKEN, ":="),
    TokenType.FLOAT_TOKEN: Token(TokenType.FLOAT_TOKEN, f"((({ALL_DIGIT})+).(({ALL_DIGIT})+))|(.({ALL_DIGIT})+)"),
    TokenType.COMMENT_TOKEN: Token(TokenType.COMMENT_TOKEN, "(///)" + f"({ALL_SYM_WITH_SPEC})*" + "(///)"),
}

SpaceToken = EmptyToken(" ")
TabToken = EmptyToken("(    )")
SpacesToken = EmptyToken("( )*")
LeftRoundBracketToken = EmptyToken("[")
RightRoundBracketToken = EmptyToken("]")

VarToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "VAR")
BeginToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "BEGIN")
EndToken = ConcreteToken(tokenIdToRegMap[TokenType.KEY_WORD_TOKEN], "END")
DotToken = tokenIdToRegMap[TokenType.DOT_TOKEN]
TypeToken = tokenIdToRegMap[TokenType.TYPE_TOKEN]
IDToken = tokenIdToRegMap[TokenType.IDENTIFIER_TOKEN]
IntegerToken = tokenIdToRegMap[TokenType.INTEGER_TOKEN]
BoolToken = tokenIdToRegMap[TokenType.BOOLEAN_TOKEN]
AssignToken = tokenIdToRegMap[TokenType.ASSIGN_TOKEN]
LiteralToken = tokenIdToRegMap[TokenType.LITERAL_TOKEN]
EndLineToken = ConcreteToken(tokenIdToRegMap[TokenType.SEPARATOR_TOKEN], "&")
WriteToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "WRITE")
ReadToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "READ")
WritelnToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "WRITELN")
ReadlnToken = ConcreteToken(tokenIdToRegMap[TokenType.FUNC_TOKEN], "READLN")
CommentToken = tokenIdToRegMap[TokenType.COMMENT_TOKEN]
FloatToken = tokenIdToRegMap[TokenType.FLOAT_TOKEN]
