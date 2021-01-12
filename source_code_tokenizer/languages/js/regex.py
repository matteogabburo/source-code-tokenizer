LIST_KEYWORDS = [
    r"await",
    r"break",
    r"case",
    r"catch",
    r"class",
    r"const",
    r"continue",
    r"debugger",
    r"default",
    r"delete",
    r"do",
    r"else",
    r"enum",
    r"export",
    r"extends",
    r"false",
    r"finally",
    r"for",
    r"function",
    r"if",
    r"implements",
    r"import",
    r"instanceof",
    r"interface",
    r"in",
    r"let",
    r"new",
    r"null",
    r"package",
    r"private",
    r"protected",
    r"public",
    r"return",
    r"super",
    r"switch",
    r"static",
    r"this",
    r"throw",
    r"try",
    r"True",
    r"typeof",
    r"var",
    r"void",
    r"while",
    r"with",
    r"yield",
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
_INT_SUFFIX = r"[n]?"
_NUMBER_OCT = r"[0][oO]?[0-7]+" + _INT_SUFFIX
_NUMBER_HEX = r"[0][xX][\da-fA-F]+" + _INT_SUFFIX
_NUMBER_BIN = r"[0][bB][0-1]+" + _INT_SUFFIX
_NUMBER_INT = r"[^0\D][\d]*" + _INT_SUFFIX
_NUMBER_SCI = r"[\d]+[\.]?[\d]*[eE][+-]?[\d]+" + _INT_SUFFIX
_NUMBER_FLO1 = r"[\d]+\.[\d]*"
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
_REGEX_STRING1 = r'"(\\\n|\\"|[^"]|.\n])*"'
_REGEX_STRING2 = r"'(\\\n|\\'|[^']|.\n])*'"
_REGEX_STRING3 = r"`(\\\n|\\`|[^`]|.\n])*`"
_REGEX_STRING = _REGEX_STRING1 + "|" + _REGEX_STRING2 + "|" + _REGEX_STRING3
STRING = r"(?P<STRING>" + _REGEX_STRING + ")"

# char regex
_REGEX_CHAR = r"'(\\(\\|'|\"|\?|a|b|f|n|r|t|v|[0-9]{1,3}|x[a-fA-F0-9]+)|\w)'"
CHAR = r"(?P<CHAR>" + _REGEX_CHAR + ")"

FULL_JSREGEX = "|".join([COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME])


class JSRegex:
    def __init__(self):

        self.regex_groups = [COMMENT, STRING, KEYWORD, NUMBER, OP, NAME]

    def get_full_regex(self):
        return FULL_JSREGEX

    def get_clean_indent_regex(self):
        return RM_INDENT

    def get_remove_doublespaces_regex(self):
        return RM_MULTIPLE_SPACES
