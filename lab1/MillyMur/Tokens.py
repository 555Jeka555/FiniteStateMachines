from __future__ import annotations
import RegexToDFA
from enum import Enum


class TokenProcessResult(Enum):
    END = 1
    SUCCESS = 2
    FAILED = 3


class Token:
    def __init__(self, id: str, reg: str):
        self.id = id
        self.reg = reg
        self.slider = RegexToDFA.RegToDFAConverter().convert(reg)

    def nextChar(self, c: str) -> TokenProcessResult:
        status = TokenProcessResult.SUCCESS
        if self.slider.IsFinal():
            status = TokenProcessResult.END
        try:
            self.slider.Move(c)
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


