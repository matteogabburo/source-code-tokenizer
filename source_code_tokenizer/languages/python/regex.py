LIST_KEYWORDS = [
    r"and",
    r"assert",
    r"async",
    r"as",
    r"await",
    r"break",
    r"class",
    r"continue",
    r"def",
    r"del",
    r"elif",
    r"else",
    r"except",
    r"False",
    r"finally",
    r"for",
    r"from",
    r"global",
    r"if",
    r"import",
    r"in",
    r"is",
    r"lambda",
    r"None",
    r"nonlocal",
    r"not",
    r"or",
    r"pass",
    r"raise",
    r"return",
    r"True",
    r"try",
    r"while",
    r"with",
    r"yield",
]

IDENTATION = r"(?P<INDENT>^[\t| ]+)"

NEWLINE = r"(?P<NEWLINE>$)"
NL = r"(?P<NL>^[ |\t]*\n)"

# Language keywords
_REGEX_KEYWORD = "|".join([r"{}(?!\w)".format(kw) for kw in LIST_KEYWORDS])
KEYWORD = "(?P<KW>" + _REGEX_KEYWORD + ")"

# numbers
_NUMBER_STD = r"[\d]+[\.]?[\d]*"
_DECIMAL_STD = r"[\.]?[\d]+"
_NUMBER_IMG = r"[\d]*[+-]?[\d]+[jJ]"
_NUMBER_SCI = r"[\d]*[\.]?[\d]*[eE][+-]?[\d]+"
_NUMBER_BIN = r"[0][bB][0-1]+"
_NUMBER_OCT = r"[0][oO][0-7]+"
_NUMBER_HEX = r"[0][xX][\da-fA-F]+"
_REGEX_NUMBER = "|".join(
    [_NUMBER_BIN, _NUMBER_OCT, _NUMBER_HEX, _NUMBER_SCI, _NUMBER_IMG, _DECIMAL_STD]
)
NUMBER = r"(?P<NUMBER>" + _REGEX_NUMBER + ")"

# variable names
_REGEX_NAME = r"[^\d\W]\w*"
NAME = r"(?P<NAME>" + _REGEX_NAME + ")"

# match every not-[\w] character (for example it match +,-,*,-,...) except spaces
_REGEX_OP = r"[^\s\w]"
OP = r"(?P<OP>" + _REGEX_OP + ")"

# comments regex
_REGEX_COMMENT = r"#[^\n]*"
COMMENT = r"(?P<COMMENT>" + _REGEX_COMMENT + ")"

# string regex
_STRING_CB = r"(?P<ERROR_{}>\Z)" # catastrofic backtracking if a string is not closed
_STRING_PREFIX = r"(b|r|u|f|br|fr)?"
_STRING_MULTILINE_T1 = _STRING_PREFIX + r'"{3}([^"]|\\"|""(?!")|"(?!"))*("{3}|'+ _STRING_CB.format("MT1") +')'
_STRING_MULTILINE_T2 = _STRING_PREFIX + r"'{3}([^']|\\'|''(?!')|'(?!'))*('{3}|"+ _STRING_CB.format("MT2") +")"
_REGEX_STRING_MULTILINE = _STRING_MULTILINE_T1 + "|" + _STRING_MULTILINE_T2
_STRING_MULTILINE = r"(?P<STRING_M>" + _REGEX_STRING_MULTILINE + ")"
_STRING_T1 = _STRING_PREFIX + r'"(\\\n|\\"|\\\\|\\|[^"]|.\n])*("|'+ _STRING_CB.format("T1") +')'
_STRING_T2 = _STRING_PREFIX + r"'(\\\n|\\'|\\\\|\\|[^']|.\n])*('|"+ _STRING_CB.format("T2") +")"
_REGEX_STRING = _STRING_T1 + "|" + _STRING_T2
_STRING = r"(?P<STRING>" + _REGEX_STRING + ")"
STRING = _STRING_MULTILINE + "|" + _STRING

FULL_PYREGEX = "|".join(
    [NEWLINE, STRING, COMMENT, KEYWORD, NUMBER, OP, NAME, NL, IDENTATION]
)


class PyRegex:
    def __init__(self):

        self.regex_groups = [
            NEWLINE,
            STRING,
            COMMENT,
            KEYWORD,
            NUMBER,
            OP,
            NAME,
            NL,
            IDENTATION,
        ]

    def get_full_regex(self):
        return FULL_PYREGEX
