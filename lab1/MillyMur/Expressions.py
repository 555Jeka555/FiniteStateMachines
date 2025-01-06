from TokenType import *
from typing import List


class Expression:
    def __init__(self, tokens: List[IRegular]):
        self.tokens = tokens

    def handle(self, lineIdx: int,  string: str) -> [str, int | None]:
        start = 0
        result = ""
        for token in self.tokens:
            tokenId, find, errIdx = token.handle(string, start)
            token.reset()
            if errIdx is not None:
                return result, errIdx
            elif tokenId != TokenType.EMPTY_TOKEN:

                findOut = find.replace(SEMICOLON, ";")
                findOut = findOut.replace(LEFT_ROUND_BRACKET, "(")
                findOut = findOut.replace(RIGHT_ROUND_BRACKET, ")")

                result += tokenId.convert() + f" ({lineIdx}, {start}) " + '"' + findOut + '"' + "\n"
            start += len(find)
        if len(string) > start:
            return result, start + 1

        print(result, end="")
        return result, None


expressions = [
    Expression([ProgramToken, SpaceToken, IDToken, EndLineToken]),

    Expression([BeginToken]),
    Expression([EndToken, DotToken]),

    Expression([VarToken]),
    Expression([SpacesToken, IDToken, ColonToken, SpaceToken, ArrayTypeToken, DimensionToken, SpaceToken, OfToken, SpaceToken, TypeToken, EndLineToken]),
    Expression([SpacesToken, IDToken, ColonToken, SpaceToken, TypeToken, EndLineToken]),

    Expression([SpacesToken, IDToken, ArrayIndexToken, SpaceToken, AssignToken, SpaceToken, IDToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IDToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IntegerToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, BoolToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, LiteralToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, FloatToken, EndLineToken]),

    Expression([TabToken, WriteToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, WriteToken, LeftRoundBracketToken, LiteralToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, ReadToken, EndLineToken]),
    Expression([TabToken, ReadToken, LeftRoundBracketToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, ReadToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),

    Expression([TabToken, WritelnToken, EndLineToken]),
    Expression([TabToken, WritelnToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, WritelnToken, LeftRoundBracketToken, LiteralToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, ReadlnToken, EndLineToken]),
    Expression([TabToken, ReadlnToken, LeftRoundBracketToken, IDToken, RightRoundBracketToken, EndLineToken]),
    Expression([TabToken, ReadlnToken, LeftRoundBracketToken, RightRoundBracketToken, EndLineToken]),

    Expression([SpacesToken, CommentToken]),
    Expression([SpacesToken, LineCommentToken]),
]


