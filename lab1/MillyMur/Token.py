from abc import ABC, abstractmethod
from enum import Enum
import RegexToDFA


class TokenType(Enum):
    EMPTY_TOKEN = 0
    KEY_WORD_TOKEN = 1
    SEPARATOR_TOKEN = 2
    IDENTIFIER_TOKEN = 3
    DOT_TOKEN = 4
    ASSIGN_TOKEN = 5
    LITERAL_TOKEN = 6
    BOOLEAN_TOKEN = 7
    INTEGER_TOKEN = 8
    FUNC_TOKEN = 9
    TYPE_TOKEN = 10
    FLOAT_TOKEN = 11
    COMMENT_TOKEN = 12
    LINE_COMMENT_TOKEN = 13
    DIMENSION_OF_ARRAY_TOKEN = 14
    ARRAY_INDEX_TOKEN = 15
    MULTIPLICATION_TOKEN = 16  # *
    PLUS_TOKEN = 17  # +
    MINUS_TOKEN = 18  # -
    DIVIDE_TOKEN = 19  # /
    SEMICOLON_TOKEN = 20  # ;
    COMMA_TOKEN = 21  # ,
    LEFT_PAREN_TOKEN = 22  # (
    RIGHT_PAREN_TOKEN = 23  # )
    LEFT_BRACKET_TOKEN = 24  # [
    RIGHT_BRACKET_TOKEN = 25  # ]
    EQ_TOKEN = 26  # =
    GREATER_TOKEN = 27  # >
    LESS_TOKEN = 28  # <
    LESS_EQ_TOKEN = 29  # <=
    GREATER_EQ_TOKEN = 30  # >=
    NOT_EQ_TOKEN = 31  # <>
    COLON_TOKEN = 32  # :
    ASSIGN_OPERATOR = 33  # :=

    def convert(self) -> str:
        match self:
            case TokenType.EMPTY_TOKEN:
                return "Empty Token"
            case TokenType.KEY_WORD_TOKEN:
                return "Keyword Token"
            case TokenType.SEPARATOR_TOKEN:
                return "Separator Token"
            case TokenType.IDENTIFIER_TOKEN:
                return "Identifier Token"
            case TokenType.DOT_TOKEN:
                return "Dot Token"
            case TokenType.ASSIGN_TOKEN:
                return "Assign Token"
            case TokenType.LITERAL_TOKEN:
                return "Literal Token"
            case TokenType.BOOLEAN_TOKEN:
                return "Boolean Token"
            case TokenType.INTEGER_TOKEN:
                return "Integer Token"
            case TokenType.FUNC_TOKEN:
                return "Function Token"
            case TokenType.TYPE_TOKEN:
                return "Type Token"
            case TokenType.FLOAT_TOKEN:
                return "Float Token"
            case TokenType.COMMENT_TOKEN:
                return "Comment Token"
            case TokenType.LINE_COMMENT_TOKEN:
                return "Line Comment Token"
            case TokenType.DIMENSION_OF_ARRAY_TOKEN:
                return "Dimension Of Array Token"
            case TokenType.ARRAY_INDEX_TOKEN:
                return "Type Array Token"
            case TokenType.MULTIPLICATION_TOKEN:
                return "MULTIPLICATION_TOKEN (*)"
            case TokenType.PLUS_TOKEN:
                return "PLUS_TOKEN (+)"
            case TokenType.MINUS_TOKEN:
                return "MINUS_TOKEN (-)"
            case TokenType.DIVIDE_TOKEN:
                return "DIVIDE_TOKEN (/)"
            case TokenType.SEMICOLON_TOKEN:
                return "SEMICOLON_TOKEN (;)"
            case TokenType.COMMA_TOKEN:
                return "COMMA_TOKEN (,)"
            case TokenType.LEFT_PAREN_TOKEN:
                return "LEFT_PAREN_TOKEN (()"
            case TokenType.RIGHT_PAREN_TOKEN:
                return "RIGHT_PAREN_TOKEN ())"
            case TokenType.LEFT_BRACKET_TOKEN:
                return "LEFT_BRACKET_TOKEN ([)"
            case TokenType.RIGHT_BRACKET_TOKEN:
                return "RIGHT_BRACKET_TOKEN (])"
            case TokenType.EQ_TOKEN:
                return "EQ_TOKEN (=)"
            case TokenType.GREATER_TOKEN:
                return "GREATER_TOKEN (>)"
            case TokenType.LESS_TOKEN:
                return "LESS_TOKEN (<)"
            case TokenType.LESS_EQ_TOKEN:
                return "LESS_EQ_TOKEN (<=)"
            case TokenType.GREATER_EQ_TOKEN:
                return "GREATER_EQ_TOKEN (>=)"
            case TokenType.NOT_EQ_TOKEN:
                return "NOT_EQ_TOKEN (<>)"
            case TokenType.COLON_TOKEN:
                return "COLON_TOKEN (:)"
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
