LIST_KEYWORDS = [
    r"abstract",
    r"assert",
    r"boolean",
    r"break",
    r"byte",
    r"case",
    r"catch",
    r"char",
    r"class",
    r"const",
    r"continue",
    r"default",
    r"double",
    r"do",
    r"else",
    r"enum",
    r"extends",
    r"finally",
    r"final",
    r"float",
    r"for",
    r"goto",
    r"if",
    r"implements",
    r"import",
    r"instanceof",
    r"interface",
    r"int",
    r"long",
    r"native",
    r"new",
    r"package",
    r"private",
    r"protected",
    r"public",
    r"return",
    r"short",
    r"static",
    r"strictfp",
    r"super",
    r"switch",
    r"synchronized",
    r"this",
    r"throws",
    r"throw",
    r"transient",
    r"try",
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
_NUMBER_OCT1 = r"[0][0-7][_0-7]*[0-7][lL]?"
_NUMBER_OCT2 = r"[0][0-7][lL]?"
_NUMBER_HEX1 = r"[0][xX][\da-fA-F][_\da-fA-F]*[\da-fA-F][lL]?"
_NUMBER_HEX2 = r"[0][xX][\da-fA-F][lL]?"
_NUMBER_BIN1 = r"[0][bB][0-1][_0-1]*[0-1][lL]?"
_NUMBER_BIN2 = r"[0][bB][0-1][lL]?"
_NUMBER_INT = r"[^0\D][\d_]*\d[lL]?"
_NUMBER_SCI = r"[\d]*[\.]?[\d]*[eE][+-]?[\d]+[FDfd]?"
_NUMBER_FLO1 = r"[\d]+[\.]?[\d]*[DFfd]"
_NUMBER_FLO2 = r"[\.]?[\d]+[FDfd]?"
_REGEX_NUMBER = "|".join(
    [
        _NUMBER_OCT1,
        _NUMBER_OCT2,
        _NUMBER_HEX1,
        _NUMBER_HEX2,
        _NUMBER_BIN1,
        _NUMBER_BIN2,
        _NUMBER_INT,
        _NUMBER_SCI,
        _NUMBER_FLO1,
    ]
)
NUMBER = r"(?P<NUMBER>" + _REGEX_NUMBER + ")"

# comments regex
_COMMENT = r"//[^\n]*"
_STRING_CB = r"(?P<ERROR_{}>\Z)"  # catastrofic backtracking if a string is not closed
_COMMENT_MULTILINE = r"/\*(.|[\r\n])*?(\*/|" + _STRING_CB.format("COMM_M") + ")"
_REGEX_COMMENT = _COMMENT + "|" + _COMMENT_MULTILINE
COMMENT = r"(?P<COMMENT>" + _REGEX_COMMENT + ")"

# string regex
_STRING_CB = r"(?P<ERROR_{}>\Z)"  # catastrofic backtracking if a string is not closed
_STRING_MULTILINE = (
    r'"{3}([^"]|\\"|""(?!")|"(?!"))*("{3}|' + _STRING_CB.format("STR_MT") + ")"
)
_STRING = r'"(\\\n|\\"|\\\\|[^"]|.\n])*("|' + _STRING_CB.format("STR") + ")"
_REGEX_STRING = _STRING_MULTILINE + "|" + _STRING
STRING = r"(?P<STRING>" + _REGEX_STRING + ")"

# char regex
_CHAR_CB = r"(?P<ERROR_{}>\Z)"  # catastrofic backtracking if a string is not closed
_REGEX_CHAR = (
    r"'(\\(\\|'|\"|\?|a|b|f|n|r|t|v|[0-9]{1,3}|x[a-fA-F0-9]+)|\s|\w){0,1}('|"
    + _CHAR_CB.format("CHR")
    + ")"
)
CHAR = r"(?P<CHAR>" + _REGEX_CHAR + ")"

FULL_JAVAREGEX = "|".join([COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME])


class JavaRegex:
    def __init__(self):

        self.regex_groups = [COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME]

    def get_full_regex(self):
        return FULL_JAVAREGEX

    def get_clean_indent_regex(self):
        return RM_INDENT

    def get_remove_doublespaces_regex(self):
        return RM_MULTIPLE_SPACES
