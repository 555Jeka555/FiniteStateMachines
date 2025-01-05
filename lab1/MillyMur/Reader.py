import Expressions
from typing import List

class Reader:
    def __init__(self, exs: List[Expressions.Expression]):
        self.exs = exs

    def handle(self, text: str):
        lineIdx = 1
        for line in text.splitlines():
            errIdx = None
            for ex in self.exs:
                errIdxtmp = ex.handle(line)
                if errIdxtmp is not None:
                    if errIdx is None:
                        errIdx = errIdxtmp
                else:
                    errIdx = None
                    break

            if errIdx is not None:
                print("ERROR", "(", lineIdx, ":", errIdx, ")")
                return
            lineIdx += 1
