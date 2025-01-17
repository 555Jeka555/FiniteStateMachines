from __future__ import annotations
from typing import Callable, List
from Tokens import Token, TokenProcessResult


class LexerToken:
    def __init__(self, tokenType: str, value: str, position: tuple[int, int]):
        self.type = tokenType
        self.value = value
        self.position = position

    def __repr__(self):
        return f"{self.type}('{self.value}') at {self.position}"


class Lexer:
    def __init__(self, tokens: List[Token], valueGetter: Callable[[], str]):
        self.tokens = tokens
        self.line = 1
        self.column = 1
        self.buffer = valueGetter()
        self.valueGetter = valueGetter
        self.statistics = dict()

    def nextToken(self) -> LexerToken | None:
        if not self.buffer and not self.appendNewBuffer():
            return None

        for token in self.tokens:
            token.reset()

            bufferIndex = 0
            resultValue = ""

            while True:
                charResult = token.nextChar(self.buffer[bufferIndex])

                if charResult == TokenProcessResult.SUCCESS:
                    resultValue += self.buffer[bufferIndex]
                    bufferIndex += 1

                if charResult == TokenProcessResult.END or (
                    charResult == TokenProcessResult.SUCCESS
                    and token.isEnd()
                    and bufferIndex == len(self.buffer)
                    and not self.appendNewBuffer()
                ):
                    self.buffer = self.buffer[bufferIndex:]
                    startPosition = (self.line, self.column)
                    self.column += len(resultValue)

                    if resultValue == "\n":
                        self.column = 1
                        self.line += 1

                    if token.id == 'BLOCK_COMMENT' or token.id == 'LINE_COMMENT':
                        token.reset()
                        bufferIndex = 0
                        continue

                    lexerToken = LexerToken(token.id, resultValue, startPosition)
                    self.appendIntoStatistics(lexerToken)

                    return lexerToken

                if charResult == TokenProcessResult.FAILED:
                    break

                if bufferIndex == len(self.buffer) and not self.appendNewBuffer():
                    break

        tmp = self.buffer
        self.buffer = self.buffer[1:]
        return LexerToken("BAD", tmp[0], (self.line, self.column))

    def appendIntoStatistics(self, lexerToken: LexerToken):
        if lexerToken.value not in self.statistics.keys():
            l = []
            l.append(lexerToken)
            self.statistics[lexerToken.value] = l
        else:
            self.statistics[lexerToken.value].append(lexerToken)

    def printStatistics(self):
        print()
        print("STATISTICS")

        print("VALUE".ljust(30) + "TYPE".ljust(15) + "COUNT".ljust(15) + "POSITIONS")
        print("-" * 75)

        for resultValue, lexerTokens in self.statistics.items():
            value = (resultValue if resultValue else "<EMPTY>").ljust(30)
            token_type = lexerTokens[0].type.ljust(15)
            count = str(len(lexerTokens)).ljust(15)
            positions = []

            for lexerToken in lexerTokens:
                position_str = ",".join(map(str, lexerToken.position))
                positions.append(position_str)

            print(f"{value}{token_type}{count}{'; '.join(positions)}")

    def appendNewBuffer(self) -> bool:
        newData = self.valueGetter()

        if not newData:
            return False

        self.buffer += newData

        return True
