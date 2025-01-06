import Expressions
from typing import List


class Reader:
    def __init__(self, expressions: List[Expressions.Expression], outFile: str):
        self.expressions = expressions
        self.outFile = outFile

    def handle(self, text: str):
        lineIdx = 1
        resultData = ""
        for line in text.splitlines():
            errIdx = None
            for ex in self.expressions:
                result, errIdxtmp = ex.handle(lineIdx, line)
                resultData += result

                if errIdxtmp is not None:
                    if errIdx is None:
                        errIdx = errIdxtmp
                else:
                    errIdx = None
                    break

            if errIdx is not None:
                print("BAD" + " (" + str(lineIdx) + ", " + str(errIdx) + ")")
                # return

            lineIdx += 1

        with open(self.outFile, 'w', newline='') as f:
            f.write(resultData)
