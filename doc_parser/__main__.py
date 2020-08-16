from typing import Any, IO, List, Optional, Sequence, Tuple

import argparse
import enum

from .parser import parse_commands


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


class CharacterType(enum.Enum):
    LITERAL = enum.auto()
    NAMED = enum.auto()
    IDENTIFIER = enum.auto()
    REGEX = enum.auto()


class Character(enum.Enum):
    DOUBLE_QUOTE = ('"', CharacterType.LITERAL)
    HASH = ("#", CharacterType.LITERAL)
    PERCENT = ("%", CharacterType.LITERAL)
    AMPERSAND = ("&", CharacterType.LITERAL)
    SINGLE_QUOTE = ("'", CharacterType.LITERAL)
    PAREN_OPEN = ("(", CharacterType.LITERAL)
    PAREN_CLOSE = (")", CharacterType.LITERAL)
    ANGLE_OPEN = ("<", CharacterType.LITERAL)
    ANGLE_CLOSE = (">", CharacterType.LITERAL)
    BRACKET_OPEN = ("[", CharacterType.LITERAL)
    BRACKET_CLOSE = ("]", CharacterType.LITERAL)
    CURLY_OPEN = ("{", CharacterType.LITERAL)
    CURLY_CLOSE = ("}", CharacterType.LITERAL)
    TILDE = ("~", CharacterType.LITERAL)
    ASTERISK = ("*", CharacterType.LITERAL)
    PLUS = ("+", CharacterType.LITERAL)
    BACK_TICK = ("`", CharacterType.LITERAL)
    PERIOD = (".", CharacterType.LITERAL)
    COLON = (":", CharacterType.LITERAL)
    EXCLAMATION_MARK = ("!", CharacterType.LITERAL)
    EQUALS = ("=", CharacterType.LITERAL)
    AT = ("@", CharacterType.LITERAL)
    FORWARD_SLASH = ("/", CharacterType.LITERAL)
    BACK_SLASH = ("\\", CharacterType.LITERAL)
    CARET = ("^", CharacterType.LITERAL)
    UNDERSCORE = ("_", CharacterType.LITERAL)
    PIPE = ("|", CharacterType.LITERAL)
    DOLLAR_SIGN = ("$", CharacterType.LITERAL)
    ZERO = ("0", CharacterType.LITERAL)
    ONE = ("1", CharacterType.LITERAL)
    TWO = ("2", CharacterType.LITERAL)
    THREE = ("3", CharacterType.LITERAL)
    FOUR = ("4", CharacterType.LITERAL)
    FIVE = ("5", CharacterType.LITERAL)
    SIX = ("6", CharacterType.LITERAL)
    SEVEN = ("7", CharacterType.LITERAL)
    EIGHT = ("8", CharacterType.LITERAL)
    NINE = ("9", CharacterType.LITERAL)
    BACK_SPACE = ("BS", CharacterType.NAMED)
    END = ("End", CharacterType.NAMED)
    HOME = ("Home", CharacterType.NAMED)
    LEFT = ("Left", CharacterType.NAMED)
    LEFT_MOUSE = ("LeftMouse", CharacterType.NAMED)
    DEL = ("Del", CharacterType.NAMED)
    CARRIAGE_RETURN = ("CR", CharacterType.NAMED)
    RIGHT = ("Right", CharacterType.NAMED)
    RIGHT_MOUSE = ("RightMouse", CharacterType.NAMED)
    DOWN = ("Down", CharacterType.NAMED)
    ESC = ("Esc", CharacterType.NAMED)
    F1 = ("F1", CharacterType.NAMED)
    MIDDLE_MOUSE = ("MiddleMouse", CharacterType.NAMED)
    UP = ("Up", CharacterType.NAMED)
    HELP = ("Help", CharacterType.NAMED)
    INSERT = ("Insert", CharacterType.NAMED)
    NEW_LINE = ("NL", CharacterType.NAMED)
    PAGE_DOWN = ("PageDown", CharacterType.NAMED)
    PAGE_UP = ("PageUp", CharacterType.NAMED)
    pattern = ("{pattern}", CharacterType.IDENTIFIER)
    SCROLL_WHEEL_DOWN = ("ScrollWheelDown", CharacterType.NAMED)
    SCROLL_WHEEL_LEFT = ("ScrollWheelLeft", CharacterType.NAMED)
    SCROLL_WHEEL_RIGHt = ("ScrollWheelRight", CharacterType.NAMED)
    SCROLL_WHEEL_UP = ("ScrollWheelUp", CharacterType.NAMED)
    SPACE = ("Space", CharacterType.NAMED)
    TAB = ("Tab", CharacterType.NAMED)
    UNDO = ("Undo", CharacterType.NAMED)
    char = ("{char}", CharacterType.IDENTIFIER)
    char1 = ("{char}", CharacterType.IDENTIFIER)
    char2 = ("{char}", CharacterType.IDENTIFIER)
    RE_lower_alpha = ("{a-z}", CharacterType.REGEX)
    RE_alpha = ("{a-zA-Z}", CharacterType.REGEX)
    RE_alpha_numeric = ("{a-zA-Z0-9}", CharacterType.REGEX)
    RE_mark = ("{a-zA-Z0-9.%#:-}", CharacterType.REGEX)
    RE_mark_lower = ("{a-z0-9.%#:-}", CharacterType.REGEX)
    count = ("{count}", CharacterType.IDENTIFIER)
    expr = ("{expr}", CharacterType.IDENTIFIER)
    filter = ("{filter}", CharacterType.IDENTIFIER)
    height = ("{height}", CharacterType.IDENTIFIER)
    mark = ("{mark}", CharacterType.IDENTIFIER)
    mode = ("{mode}", CharacterType.IDENTIFIER)
    motion = ("{motion}", CharacterType.IDENTIFIER)
    number = ("{number}", CharacterType.IDENTIFIER)
    range = ("{range}", CharacterType.IDENTIFIER)
    register = ("{register}", CharacterType.IDENTIFIER)
    regname = ("{regname}", CharacterType.IDENTIFIER)


class CharacterModifier(enum.Enum):
    SHIFT = "S"
    CONTROL = "C"


class CharacterCombination:
    def __init__(
        self,
        char: Character,
        modifiers: Sequence[CharacterModifier],
        is_optional: bool = False,
    ):
        self.char = char
        self.modifiers = modifiers
        self.is_optional = is_optional


class Command:
    def __init__(
        self,
        mode: Mode,
        tag: Optional[str],
        chars: str,
        flags: Optional[str],
        description: str,
    ):
        self.mode = mode
        self.tag = tag
        self.chars = chars
        print(chars)
        self.description = description

        self.is_cursor_movement_command = False
        self.is_undoable = False
        if flags is not None:
            if self.mode in (
                Mode.NormalMode,
                Mode.SquareBracketCommandMode,
                Mode.GCommandMode,
                Mode.ZCommandMode,
                Mode.VisualMode,
            ):
                self.is_cursor_movement_command = "1" in flags
                self.is_undoable = "2" in flags
            else:
                assert False  # this should never happen

    def append_description(self, more_description: str):
        if self.description:
            self.description += " "
        self.description += more_description

    def __str__(self) -> str:
        return f"Command({self.mode}, {self.tag}, {self.chars}, {self.description})"


def main(index_fp: IO[str]) -> None:
    commands = parse_commands(index_fp)
    print(len(commands))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", type=argparse.FileType("r"), dest="index_fp", required=True
    )
    args = parser.parse_args()

    main(args.index_fp)
