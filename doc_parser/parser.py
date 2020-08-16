from typing import Any, IO, List, Optional, Sequence, Tuple

import abc
import argparse
import enum
import logging

from .command import Command
from .mode import Mode


logger = logging.getLogger(__name__)


def parse_tag(line: str, index: int) -> Tuple[str, int]:
    tag = ""
    index += 1
    while line[index] != "|":
        tag += line[index]
        index += 1
    index += 1
    while line[index] == " ":
        index += 1
    return tag, index


def parse_chars(line: str, index: int, last_index: int) -> Tuple[str, int]:
    chars = ""
    waiting_to_close_paren = False
    while index < len(line):
        if line[index] == "(":
            if index + 1 < len(line) and line[index + 1] != " ":
                waiting_to_close_paren = True
        elif line[index] == ")":
            waiting_to_close_paren = False
        if line[index] == " " and index >= last_index and not waiting_to_close_paren:
            break
        chars += line[index]
        index += 1
    return chars.rstrip(), index


def parse_flags(line: str, index: int) -> Tuple[Optional[str], int]:
    saved_index = index
    last_char_was_space = False
    buf = ""
    while index < len(line):
        if line[index] == " ":
            if last_char_was_space:
                return buf, saved_index + len(buf)
            last_char_was_space = True
        else:
            last_char_was_space = False
            buf += line[index]
        index += 1
    return None, saved_index


def consume_whitespace(line: str, index: int) -> int:
    while index < len(line) and line[index] == " ":
        index += 1
    return index


def split_columns(
    mode: Mode, line: str
) -> Optional[Tuple[Optional[str], Optional[str], Optional[str], str]]:
    logger.debug("-------------")
    for i in range(len(line)):
        if i % 10 == 0:
            logger.debug(int(i / 10), end="")
        else:
            logger.debug(" ", end="")
    logger.debug("\n")
    for i in range(len(line)):
        logger.debug(i % 10, end="")
    logger.debug(f"{line: <90}")

    if not line:
        return None

    index = 0
    tag: Optional[str] = None
    chars: Optional[str] = None
    flags: Optional[str] = None
    description: str

    if line[index] == "|":
        tag, index = parse_tag(line, index)
    elif line[index] == " ":
        if index + 1 < len(line) and line[index + 1] != " ":
            return None
        index = mode.chars_column
    else:
        return None

    if line[index] == " ":
        index = consume_whitespace(line, index)
    else:
        next_column = (
            mode.description_column if mode.flags_column is None else mode.flags_column
        )
        chars, index = parse_chars(line, index, next_column)

    index = consume_whitespace(line, index)

    if mode.flags_column is not None:
        flags, index = parse_flags(line, index)

    index = consume_whitespace(line, index)

    description = line[index:]

    logger.debug(" -> NO TAG" if tag is None else f' -> TAG="{tag}"')
    logger.debug(" -> NO CHARS" if chars is None else f' -> CHARS="{chars.rstrip()}"')
    logger.debug(" -> NO FLAGS" if flags is None else f' -> FLAGS="{flags}"')
    logger.debug(f' -> DESC="{line[index:]}"')
    logger.debug("-------------")

    return tag, chars, flags, description


def read_header(index_fp: IO[str]) -> None:
    for line in index_fp:
        if line.startswith("=========="):
            return


def parse_commands(index_fp: IO[str]) -> Sequence[Command]:

    # set up some parser state
    next_mode: Optional[Mode] = Mode.InsertMode
    current_mode: Optional[Mode] = None
    current_command: Optional[Command] = None
    commands: List[Command] = []
    lines_to_skip = 0

    read_header(index_fp)
    for line in index_fp:
        if lines_to_skip > 0:
            lines_to_skip -= 1
            continue

        line = line.replace("\t", " " * 8).rstrip()
        if current_mode:
            columns = split_columns(current_mode, line)
            if columns is None:
                logger.debug(f'Invalid line: "{line}"')
                current_command = None
            else:
                tag, chars, flags, description = columns
                if chars is not None:
                    if current_command is not None:
                        commands.append(current_command)
                        if description == '"':
                            description = current_command.description
                    current_command = Command(
                        current_mode, tag, chars, flags, description,
                    )
                    logger.debug(f"created {current_command}")
                else:
                    assert current_command is not None
                    assert tag is None
                    assert len(description) > 0
                    current_command.append_description(description)
                    logger.debug(f"appending to {current_command}")

        if next_mode is not None and line.startswith(next_mode.header_text):
            current_mode = next_mode
            next_mode = next_mode.next()
            logger.debug("***", current_mode, "***")
            lines_to_skip = current_mode.lines_to_skip

    return commands
