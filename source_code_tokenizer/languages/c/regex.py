LIST_KEYWORDS = [
    r"_Alignas",
    r"_Alignof",
    r"_Atomic",
    r"_Bool",
    r"_Complex",
    r"_Decimal128",
    r"_Decimal32",
    r"_Decimal64",
    r"_Generic",
    r"_Imaginary",
    r"_Noreturn",
    r"_Static_assert",
    r"_Thread_local",
    r"asm",
    r"auto",
    r"break",
    r"case",
    r"char",
    r"const",
    r"continue",
    r"default",
    r"define",
    r"double",
    r"do",
    r"elif",
    r"else",
    r"endif",
    r"enum",
    r"error",
    r"extern",
    r"float",
    r"fortran",
    r"for",
    r"goto",
    r"ifdef",
    r"ifndef",
    r"if",
    r"include",
    r"inline",
    r"int",
    r"line",
    r"long",
    r"pragma",
    r"register",
    r"restrict",
    r"return",
    r"short",
    r"signed",
    r"sizeof",
    r"static",
    r"struct",
    r"switch",
    r"typedef",
    r"undef",
    r"union",
    r"unsigned",
    r"void",
    r"volatile",
    r"while",
]

# cleaning regex
RM_INDENT = r"(//[^\n]*\n)|(\s*^\s*)"
RM_MULTIPLE_SPACES = r"[^\n\S]+"

# Language keywords
_REGEX_KEYWORD = "|".join([r"{}(?!\w)".format(kw) for kw in LIST_KEYWORDS])
KEYWORD = "(?P<KW>" + _REGEX_KEYWORD + ")"

# variable names
_REGEX_NAME = r"[^\d\W]\w*"
NAME = r"(?P<NAME>" + _REGEX_NAME + ")"

# match every not-[\w] character (for example it match +,-,*,-,...) except spaces
_REGEX_OP = r"[^\s\w]"
OP = r"(?P<OP>" + _REGEX_OP + ")"

# numbers regex
_INT_SUFFIX = r"(lu|lU|ul|uL|Lu|LU|Ul|UL|l|u|L|U)?"
_NUMBER_OCT = r"[0][0-7]+" + _INT_SUFFIX
_NUMBER_HEX = r"[0][xX][\da-fA-F]+" + _INT_SUFFIX
_NUMBER_BIN = r"[0][bB][0-1]+" + _INT_SUFFIX
_NUMBER_INT = r"[^0\D][\d]*" + _INT_SUFFIX
_NUMBER_SCI = r"[\d]+[\.]?[\d]*[eE][+-]?[\d]+"
_NUMBER_FLO1 = r"[\d]+[\.]?[\d]*"
_NUMBER_FLO2 = r"[\.][\d]+"
_NUMBER_FLO = _NUMBER_FLO1 + "|" + _NUMBER_FLO2
_REGEX_NUMBER = "|".join(
    [_NUMBER_BIN, _NUMBER_OCT, _NUMBER_HEX, _NUMBER_INT, _NUMBER_SCI, _NUMBER_FLO]
)
NUMBER = r"(?P<NUMBER>" + _REGEX_NUMBER + ")"

# comments regex
_COMMENT = r"//[^\n]*"
_COMMENT_MULTILINE = r"/\*(.|[\r\n])*?\*/"
_REGEX_COMMENT = _COMMENT + "|" + _COMMENT_MULTILINE
COMMENT = r"(?P<COMMENT>" + _REGEX_COMMENT + ")"

# string regex
_REGEX_STRING = r'"(\\\n|\\"|[^"]|.\n])*"'
STRING = r"(?P<STRING>" + _REGEX_STRING + ")"

# char regex
_REGEX_CHAR = r"'(\\(\\|'|\"|\?|a|b|f|n|r|t|v|[0-9]{1,3}|x[a-fA-F0-9]+)|\w)'"
CHAR = r"(?P<CHAR>" + _REGEX_CHAR + ")"

FULL_CREGEX = "|".join([COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME])


class CRegex:
    def __init__(self):

        self.regex_groups = [COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME]

    def get_full_regex(self):
        return FULL_CREGEX

    def get_clean_indent_regex(self):
        return RM_INDENT

    def get_remove_doublespaces_regex(self):
        return RM_MULTIPLE_SPACES
