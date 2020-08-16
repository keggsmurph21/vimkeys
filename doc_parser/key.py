from typing import Any, Dict, IO, Generic, List, Optional, Set, Sequence, Tuple, TypeVar

import enum
import logging


logger = logging.getLogger(__name__)


class KeyType(enum.Enum):
    LITERAL = enum.auto()
    NAMED = enum.auto()
    IDENTIFIER = enum.auto()
    REGEX = enum.auto()
    MODIFIER = enum.auto()
    MULTIWORD = enum.auto()


class Key(enum.Enum):
    DOUBLE_QUOTE = (('"',), KeyType.LITERAL)
    HASH = (("#",), KeyType.LITERAL)
    PERCENT = (("%",), KeyType.LITERAL)
    AMPERSAND = (("&",), KeyType.LITERAL)
    SINGLE_QUOTE = (("'",), KeyType.LITERAL)
    PAREN_OPEN = (("(",), KeyType.LITERAL)
    PAREN_CLOSE = ((")",), KeyType.LITERAL)
    ANGLE_OPEN = (("<",), KeyType.LITERAL)
    ANGLE_CLOSE = ((">",), KeyType.LITERAL)
    BRACKET_OPEN = (("[",), KeyType.LITERAL)
    BRACKET_CLOSE = (("]",), KeyType.LITERAL)
    CURLY_OPEN = (("{",), KeyType.LITERAL)
    CURLY_CLOSE = (("}",), KeyType.LITERAL)
    TILDE = (("~",), KeyType.LITERAL)
    ASTERISK = (("*",), KeyType.LITERAL)
    PLUS = (("+",), KeyType.LITERAL)
    BACK_TICK = (("`",), KeyType.LITERAL)
    PERIOD = ((".",), KeyType.LITERAL)
    COMMA = ((",",), KeyType.LITERAL)
    COLON = ((":",), KeyType.LITERAL)
    SEMICOLON = ((";",), KeyType.LITERAL)
    EXCLAMATION_MARK = (("!",), KeyType.LITERAL)
    QUESTION_MARK = (("?",), KeyType.LITERAL)
    EQUALS = (("=",), KeyType.LITERAL)
    AT = (("@",), KeyType.LITERAL)
    FORWARD_SLASH = (("/",), KeyType.LITERAL)
    BACK_SLASH = (("\\",), KeyType.LITERAL)
    CARET = (("^",), KeyType.LITERAL)
    HYPHEN = (("-",), KeyType.LITERAL)
    UNDERSCORE = (("_",), KeyType.LITERAL)
    PIPE = (("|",), KeyType.LITERAL)
    DOLLAR_SIGN = (("$",), KeyType.LITERAL)
    ZERO = (("0",), KeyType.LITERAL)
    ONE = (("1",), KeyType.LITERAL)
    TWO = (("2",), KeyType.LITERAL)
    THREE = (("3",), KeyType.LITERAL)
    FOUR = (("4",), KeyType.LITERAL)
    FIVE = (("5",), KeyType.LITERAL)
    SIX = (("6",), KeyType.LITERAL)
    SEVEN = (("7",), KeyType.LITERAL)
    EIGHT = (("8",), KeyType.LITERAL)
    NINE = (("9",), KeyType.LITERAL)
    BACK_SPACE = (("BS",), KeyType.NAMED)
    END = (("End",), KeyType.NAMED)
    HOME = (("Home",), KeyType.NAMED)
    LEFT = (("Left",), KeyType.NAMED)
    LEFT_MOUSE = (("LeftMouse",), KeyType.NAMED)
    DEL = (("Del",), KeyType.NAMED)
    CARRIAGE_RETURN = (("CR",), KeyType.NAMED)
    RIGHT = (("Right",), KeyType.NAMED)
    RIGHT_MOUSE = (("RightMouse",), KeyType.NAMED)
    DOWN = (("Down",), KeyType.NAMED)
    ESC = (("Esc",), KeyType.NAMED)
    F1 = (("F1",), KeyType.NAMED)
    MIDDLE_MOUSE = (("MiddleMouse",), KeyType.NAMED)
    UP = (("Up",), KeyType.NAMED)
    HELP = (("Help",), KeyType.NAMED)
    INSERT = (("Insert",), KeyType.NAMED)
    NEW_LINE = (("NL",), KeyType.NAMED)
    PAGE_DOWN = (("PageDown",), KeyType.NAMED)
    PAGE_UP = (("PageUp",), KeyType.NAMED)
    pattern = (("{pattern}",), KeyType.IDENTIFIER)
    SCROLL_WHEEL_DOWN = (("ScrollWheelDown",), KeyType.NAMED)
    SCROLL_WHEEL_LEFT = (("ScrollWheelLeft",), KeyType.NAMED)
    SCROLL_WHEEL_RIGHt = (("ScrollWheelRight",), KeyType.NAMED)
    SCROLL_WHEEL_UP = (("ScrollWheelUp",), KeyType.NAMED)
    SPACE = (("Space",), KeyType.NAMED)
    TAB = (("Tab",), KeyType.NAMED)
    UNDO = (("Undo",), KeyType.NAMED)
    char = (("{char}", "{char1}", "{char2}"), KeyType.IDENTIFIER)
    RE_lower_alpha = (("{a-z}",), KeyType.REGEX)
    RE_alpha = (("{a-zA-Z}", "{A-Za-z}"), KeyType.REGEX)
    RE_alpha_numeric = (("{a-zA-Z0-9}",), KeyType.REGEX)
    RE_alpha_numeric_with_quote = (('{0-9a-zA-Z"}',), KeyType.REGEX)
    RE_mark = (('{a-zA-Z0-9.%#:-"}',), KeyType.REGEX)
    RE_mark_lower = (('{a-z0-9.%#:-"}',), KeyType.REGEX)
    RE_mark_something = (('{0-9a-z"%#*:=}',), KeyType.REGEX)
    count = (("{count}",), KeyType.IDENTIFIER)
    expr = (("{expr}",), KeyType.IDENTIFIER)
    filter = (("{filter}",), KeyType.IDENTIFIER)
    height = (("{height}",), KeyType.IDENTIFIER)
    mark = (("{mark}",), KeyType.IDENTIFIER)
    mode = (("{mode}",), KeyType.IDENTIFIER)
    motion = (("{motion}",), KeyType.IDENTIFIER)
    number = (("{number}",), KeyType.IDENTIFIER)
    range = (("{range}",), KeyType.IDENTIFIER)
    register = (("{register}",), KeyType.IDENTIFIER)
    regname = (("{regname}",), KeyType.IDENTIFIER)
    other = (("other", "others"), KeyType.IDENTIFIER)
    A = (("A", "a"), KeyType.LITERAL)
    B = (("B", "b"), KeyType.LITERAL)
    C = (("C", "c"), KeyType.LITERAL)
    D = (("D", "d"), KeyType.LITERAL)
    E = (("E", "e"), KeyType.LITERAL)
    F = (("F", "f"), KeyType.LITERAL)
    G = (("G", "g"), KeyType.LITERAL)
    H = (("H", "h"), KeyType.LITERAL)
    I = (("I", "i"), KeyType.LITERAL)
    J = (("J", "j"), KeyType.LITERAL)
    K = (("K", "k"), KeyType.LITERAL)
    L = (("L", "l"), KeyType.LITERAL)
    M = (("M", "m"), KeyType.LITERAL)
    N = (("N", "n"), KeyType.LITERAL)
    O = (("O", "o"), KeyType.LITERAL)
    P = (("P", "p"), KeyType.LITERAL)
    Q = (("Q", "q"), KeyType.LITERAL)
    R = (("R", "r"), KeyType.LITERAL)
    S = (("S", "s"), KeyType.LITERAL)
    T = (("T", "t"), KeyType.LITERAL)
    U = (("U", "u"), KeyType.LITERAL)
    V = (("V", "v"), KeyType.LITERAL)
    W = (("W", "w"), KeyType.LITERAL)
    X = (("X", "x"), KeyType.LITERAL)
    Y = (("Y", "y"), KeyType.LITERAL)
    Z = (("Z", "z"), KeyType.LITERAL)
    CONTROL = (("CTRL-", "C-"), KeyType.MODIFIER)
    ALT = (("ALT-", "A-"), KeyType.MODIFIER)
    SHIFT = (("SHIFT-", "S-"), KeyType.MODIFIER)
    SPACE_TO_TILDE = (("<Space> to '~'",), KeyType.MULTIWORD)
    x80_TO_xFF = (("Meta characters (0x80 to 0xff, 128 to 255)",), KeyType.MULTIWORD)
    A_TO_Z = (("a - z",), KeyType.MULTIWORD)  # FIXME: This isn't working *quite* right

    def __init__(self, patterns: str, key_type: KeyType):
        self.patterns = patterns
        self.key_type = key_type


class KeyCombination:
    def __init__(
        self,
        principal_key: Key,
        *,
        with_shift: bool = False,
        with_control: bool = False,
        with_alt: bool = False,
        is_optional: bool = False,
    ):
        self.principal_key = principal_key
        self.with_shift = with_shift
        self.with_control = with_control
        self.with_alt = with_alt
        self.is_optional = is_optional

    def __str__(self) -> str:
        s = ""
        if self.is_optional:
            s += "["
        if self.with_control:
            s += "Ctrl+"
        if self.with_alt:
            s += "Alt+"
        if self.with_shift:
            s += "Shift+"
        s += self.key.name
        if self.is_optional:
            s += "]"
        return s


T = TypeVar("T")


class TrieNode(Generic[T]):
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.value: Optional[T] = None

    def get(self, char: str) -> Optional["TrieNode[T]"]:
        return self.children.get(char, None)

    def add_child(self, char: str) -> "TrieNode":
        if char not in self.children:
            self.children[char] = TrieNode()
        return self.children[char]

    def is_leaf(self) -> bool:
        return self.value is not None

    def dump(self, indent: int, char: str) -> None:
        print(f"{'  ' * indent}{char} => TrieNode(", end="")
        if self.is_leaf():
            print("value=" + str(self.value), end="")
        for char, child in self.children.items():
            print()
            child.dump(indent + 1, char)
        print(")", end="")


class Trie(Generic[T]):
    def __init__(self):
        self.root = TrieNode[T]()

    def insert(self, key: str, value: T) -> None:
        node = self.root
        for char in key:
            node = node.add_child(char)
        assert node.value is None
        node.value = value

    def dump(self) -> None:
        print("Trie(")
        self.root.dump(1, "START")
        print(")")

    def get(self, key: str) -> Optional[T]:
        node = self.root
        for char in key:
            node = node.get(char)
            if node is None:
                return None
        if not node.is_leaf():
            return None
        return node.value

    def get_longest_match(self, needle: str) -> Tuple[int, Optional[T]]:
        for i in range(len(needle)):
            key = self.get(needle[:-i] if i else needle)
            if key is not None:
                return len(needle) - i, key
        return 0, None


def parse_line(trie: Trie[Key], line: str) -> Sequence[KeyCombination]:

    # print(">>>", line.rstrip())
    key_combos: List[KeyCombination] = []

    print(line)

    key = trie.get(line)
    if key is not None and key.key_type is KeyType.MULTIWORD:
        key_combos.append(KeyCombination(key))
        logger.debug(line)
        logger.debug(key)
        logger.debug("\n")

    else:
        for word in line.split(" "):
            logger.debug(word)
            index = 0
            key_buf: List[Key] = []
            while index < len(word):
                word = word[index:]
                if word.startswith("<") and ">" in word:
                    close_bracket_index = word.index(">")
                    word = word[1:close_bracket_index] + word[close_bracket_index + 1 :]
                index, key = trie.get_longest_match(word)
                logger.debug(word, index, key)
                assert key is not None
                key_buf.append(key)

            with_control = False
            with_alt = False
            with_shift = False
            for key in key_buf:
                logger.debug(key)
                if key is Key.CONTROL:
                    with_control = True
                elif key is Key.ALT:
                    with_alt = True
                elif key is Key.SHIFT:
                    with_shift = True
                else:
                    key_combos.append(
                        KeyCombination(
                            key,
                            with_control=with_control,
                            with_alt=with_alt,
                            with_shift=with_shift,
                        )
                    )

    return key_combos


if __name__ == "__main__":

    trie = Trie[Key]()

    for key in Key:
        for pattern in key.patterns:
            trie.insert(pattern, key)

    # trie.dump()

    seen_keys: Set[Key] = set()

    with open("/tmp/chars.txt") as fp:
        for line in fp:

            key_combos = parse_line(trie, line.rstrip())

            assert len(key_combos)
            for key_combo in key_combos:
                print("->", key_combo)
                seen_keys.add(key_combo.key)

            print()
