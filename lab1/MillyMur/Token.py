from abc import ABC, abstractmethod
from enum import Enum
import RegexToDFA


class TokenType(Enum):
    EMPTY_TOKEN = 0
    KEY_WORD_TOKEN = 1
    IDENTIFIER_TOKEN = 2
    DOT_TOKEN = 3
    ASSIGN_TOKEN = 4
    LITERAL_TOKEN = 5
    BOOLEAN_TOKEN = 6
    INTEGER_TOKEN = 7
    FUNC_TOKEN = 8
    TYPE_TOKEN = 9
    FLOAT_TOKEN = 10
    COMMENT_TOKEN = 11
    LINE_COMMENT_TOKEN = 12
    DIMENSION_OF_ARRAY_TOKEN = 13

    MULTIPLICATION_TOKEN = 15  # *
    PLUS_TOKEN = 16  # +
    MINUS_TOKEN = 17  # -
    DIVIDE_TOKEN = 18  # /
    SEMICOLON_TOKEN = 19  # ;
    COMMA_TOKEN = 20  # ,
    LEFT_PAREN_TOKEN = 21  # (
    RIGHT_PAREN_TOKEN = 22  # )
    LEFT_BRACKET_TOKEN = 23  # [
    RIGHT_BRACKET_TOKEN = 24  # ]
    EQ_TOKEN = 25  # =
    GREATER_TOKEN = 26  # >
    LESS_TOKEN = 27  # <
    LESS_EQ_TOKEN = 28  # <=
    GREATER_EQ_TOKEN = 29  # >=
    NOT_EQ_TOKEN = 30  # <>
    COLON_TOKEN = 31  # :

    def convert(self) -> str:
        match self:
            case TokenType.EMPTY_TOKEN:
                return "EMPTY"
            case TokenType.KEY_WORD_TOKEN:
                return "KEYWORD"
            case TokenType.IDENTIFIER_TOKEN:
                return "IDENTIFIER"
            case TokenType.DOT_TOKEN:
                return "DOT"
            case TokenType.ASSIGN_TOKEN:
                return "ASSIGN"
            case TokenType.LITERAL_TOKEN:
                return "LITERAL"
            case TokenType.BOOLEAN_TOKEN:
                return "BOOLEAN"
            case TokenType.INTEGER_TOKEN:
                return "INTEGER"
            case TokenType.FUNC_TOKEN:
                return "FUNCTION"
            case TokenType.TYPE_TOKEN:
                return "TYPE"
            case TokenType.FLOAT_TOKEN:
                return "FLOAT"
            case TokenType.COMMENT_TOKEN:
                return "COMMENT"
            case TokenType.LINE_COMMENT_TOKEN:
                return "LINE COMMENT"
            case TokenType.DIMENSION_OF_ARRAY_TOKEN:
                return "DIMENSION OF ARRAY"
            case TokenType.MULTIPLICATION_TOKEN:
                return "MULTIPLICATION"
            case TokenType.PLUS_TOKEN:
                return "PLUS"
            case TokenType.MINUS_TOKEN:
                return "MINUS"
            case TokenType.DIVIDE_TOKEN:
                return "DIVIDE"
            case TokenType.SEMICOLON_TOKEN:
                return "SEMICOLON"
            case TokenType.COMMA_TOKEN:
                return "COMMA"
            case TokenType.LEFT_PAREN_TOKEN:
                return "LEFT PAREN"
            case TokenType.RIGHT_PAREN_TOKEN:
                return "RIGHT PAREN"
            case TokenType.LEFT_BRACKET_TOKEN:
                return "LEFT BRACKET"
            case TokenType.RIGHT_BRACKET_TOKEN:
                return "RIGHT BRACKET"
            case TokenType.EQ_TOKEN:
                return "EQ"
            case TokenType.GREATER_TOKEN:
                return "GREATER"
            case TokenType.LESS_TOKEN:
                return "LESS"
            case TokenType.LESS_EQ_TOKEN:
                return "LESS EQ"
            case TokenType.GREATER_EQ_TOKEN:
                return "GREATER EQ"
            case TokenType.NOT_EQ_TOKEN:
                return "NOT EQ"
            case TokenType.COLON_TOKEN:
                return "COLON"
            case _:
                return "Unknown Token Type"


class IRegular(ABC):
    @abstractmethod
    def handle(self, string: str, start: int) -> [TokenType, str, int | None]:
        pass

    @abstractmethod
    def reset(self):
        pass


class Token(IRegular):
    def __init__(self, id: TokenType, reg: str):
        self.id = id
        self.reg = reg
        self.slider = RegexToDFA.RegToDKAConverter().convert(reg)

    def handle(self, string: str, start: int) -> [TokenType, str, int | None]:
        i = start
        for c in string[start:]:
            if self.slider.IsFinal():
                break
            try:
                self.slider.Move(c)
            except:
                if self.slider.IsPossibleFinish():
                    break
                return "", "", i
            i += 1
        return self.id, string[start: i], None

    def reset(self):
        self.slider.Reset()


class ConcreteToken(IRegular):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def handle(self, string: str, start: int) -> [TokenType, str, int | None]:
        token, val, errIndx = self.token.handle(string, start)
        if errIndx is not None:
            return token, val, errIndx
        if val.upper() != self.value.upper():
            return token, "", start
        return token, val, None

    def reset(self):
        self.token.reset()


class EmptyToken(IRegular):
    def __init__(self, reg: str):
        self.token = Token(TokenType.EMPTY_TOKEN, reg)

    def handle(self, string: str, start: int) -> [TokenType, str, int]:
        return self.token.handle(string, start)

    def reset(self):
        self.token.reset()
