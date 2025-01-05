from TokenType import *
from typing import List


class Expression:
    def __init__(self, ts: List[IRegular]):
        self.tokens = ts

    def handle(self, string: str) -> int | None:
        start = 0
        result = ""
        for token in self.tokens:
            tokenId, find, errIdx = token.handle(string, start)
            token.reset()
            if errIdx is not None:
                return errIdx
            elif tokenId != TokenType.EMPTY_TOKEN:
                result += tokenId.convert() + "(" + find + ") " + str(start) + "\n"
            start += len(find)
        if len(string) > start:
            return start + 1

        print(result, end="")
        return None


expressions = [
    Expression([BeginToken]),
    Expression([EndToken, DotToken]),
    Expression([TabToken, VarToken, SpaceToken, TypeToken, SpaceToken, IDToken, EndLineToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, IDToken, EndLineToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, IntegerToken, EndLineToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, BoolToken, EndLineToken]),
    Expression([TabToken, IDToken, SpaceToken, AssignToken, SpaceToken, LiteralToken, EndLineToken]),

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

    Expression([SpacesToken, VarToken, SpaceToken, TypeToken, SpaceToken, IDToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, FloatToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IntegerToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, BoolToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, LiteralToken, EndLineToken]),
    Expression([SpacesToken, IDToken, SpaceToken, AssignToken, SpaceToken, IDToken, EndLineToken]),
    Expression([SpacesToken, CommentToken]),
]


