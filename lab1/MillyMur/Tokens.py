from __future__ import annotations
import RegexToDFA
from enum import Enum


class TokenProcessResult(Enum):
    END = 1
    SUCCESS = 2
    FAILED = 3


class Token:
    def __init__(self, id: str, reg: str, maxLength=None):
        self.id = id
        self.reg = reg
        self.slider = RegexToDFA.RegToDFAConverter().convert(reg)
        self.maxLength = maxLength
        self.length = 0

    def nextChar(self, c: str) -> TokenProcessResult:
        status = TokenProcessResult.SUCCESS
        if self.maxLength is not None and self.length >= self.maxLength:
            status = TokenProcessResult.FAILED

        if self.slider.IsFinal():
            status = TokenProcessResult.END
        try:
            self.slider.Move(c)
            self.length += 1
        except:
            if self.slider.IsPossibleFinish():
                status = TokenProcessResult.END
            else:
                status = TokenProcessResult.FAILED
        if status in [TokenProcessResult.END, TokenProcessResult.FAILED]:
            self.slider.Reset()
        return status

    def isEnd(self) -> bool:
        return self.slider.IsPossibleFinish()

    def reset(self):
        self.slider.Reset()


