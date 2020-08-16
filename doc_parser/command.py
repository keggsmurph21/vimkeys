from typing import Any, IO, List, Optional, Sequence, Tuple

import enum

from .mode import Mode


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
