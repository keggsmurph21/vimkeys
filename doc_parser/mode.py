from typing import Any, IO, List, Optional, Sequence, Tuple

import enum


class Mode(enum.Enum):
    InsertMode = ("1. Insert mode", 3, [16, 32])
    CtrlXSubMode = ("commands in CTRL-X submode", 1, [24, 40])
    CompletionMode = ("commands in completion mode", 1, [16, 31])
    NormalMode = ("2. Normal mode", 12, [16, 32, 35])
    TextObjectMode = ("2.1 Text objects", 5, [16, 35])
    WindowCommandMode = ("2.2 Window commands", 3, [16, 32])
    SquareBracketCommandMode = ("2.3 Square bracket commands", 3, [16, 32, 35])
    GCommandMode = ("2.4 Commands starting with 'g'", 3, [16, 32, 35])
    ZCommandMode = ("2.5 Commands starting with 'z'", 3, [16, 32, 35])
    OperatorPendingMode = ("2.6 Operator-pending mode", 5, [16, 32])
    VisualMode = ("3. Visual mode", 6, [16, 32, 35])
    CommandLineMode = ("4. Command-line editing", 8, [16, 32])
    TerminalJobMode = ("5. Terminal-Job mode", 7, [16, 32])
    ExMode = ("6. EX commands", 7, [16, 30])

    def __init__(
        self, header_text: str, lines_to_skip: int, column_indices: Sequence[int]
    ):
        self.header_text = header_text
        self.lines_to_skip = lines_to_skip
        self.chars_column = column_indices[0]
        self.flags_column = None if len(column_indices) == 2 else column_indices[1]
        self.description_column = column_indices[-1]

    def next(self) -> Optional["Mode"]:
        found_self = False
        for mode in self.__class__:
            if found_self:
                return mode
            if mode == self:
                found_self = True
        return None
