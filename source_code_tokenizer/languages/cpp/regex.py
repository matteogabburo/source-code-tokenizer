LIST_KEYWORDS = [
    "_Pragma",
    r"__has_cpp_attribute",
    r"__has_include",
    r"alignas",
    r"alignof",
    r"and_eq",
    r"and",
    r"asm",
    r"atomic_cancel",
    r"atomic_commit",
    r"atomic_noexcept",
    r"auto",
    r"bitand",
    r"bitor",
    r"bool",
    r"break",
    r"case",
    r"catch",
    r"char16_t",
    r"char32_t",
    r"char8_t",
    r"char",
    r"class",
    r"co_await",
    r"co_return",
    r"co_yield",
    r"compl",
    r"concept",
    r"const_cast",
    r"consteval",
    r"constexpr",
    r"constinit",
    r"const",
    r"continue",
    r"decltype",
    r"default",
    r"defined",
    r"define",
    r"delete",
    r"double",
    r"do",
    r"dynamic_cast",
    r"elif",
    r"else",
    r"endif",
    r"enum",
    r"error",
    r"explicit",
    r"export",
    r"extern",
    r"false",
    r"final",
    r"float",
    r"for",
    r"friend",
    r"goto",
    r"ifdef",
    r"ifndef",
    r"if",
    r"import",
    r"include",
    r"inline",
    r"int",
    r"line",
    r"long",
    r"module",
    r"mutable",
    r"namespace",
    r"new",
    r"noexcept",
    r"not_eq",
    r"not",
    r"nullptr",
    r"operator",
    r"or_eq",
    r"or",
    r"override",
    r"pragma",
    r"private",
    r"protected",
    r"public",
    r"reflexpr",
    r"register",
    r"reinterpret_cast",
    r"requires",
    r"return",
    r"short",
    r"signed",
    r"sizeof",
    r"static_assert",
    r"static_cast",
    r"static",
    r"struct",
    r"switch",
    r"synchronized",
    r"template",
    r"this",
    r"thread_local",
    r"throw",
    r"transaction_safe_dynamic",
    r"transaction_safe",
    r"true",
    r"try",
    r"typedef",
    r"typeid",
    r"typename",
    r"undef",
    r"union",
    r"unsigned",
    r"using",
    r"virtual",
    r"void",
    r"volatile",
    r"wchar_t",
    r"while",
    r"xor_eq",
    r"xor",
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
_STRING_PREFIX = r"(L|u8|u|U|R)?"
_REGEX_STRING = _STRING_PREFIX + r'"(\\\n|\\"|\\\\|[^"]|.\n])*"'
STRING = r"(?P<STRING>" + _REGEX_STRING + ")"

# char regex
_REGEX_CHAR = r"'(\\(\\|'|\"|\?|a|b|f|n|r|t|v|[0-9]{1,3}|x[a-fA-F0-9]+)|\w)'"
CHAR = r"(?P<CHAR>" + _REGEX_CHAR + ")"

FULL_CPPREGEX = "|".join([COMMENT, STRING, CHAR, KEYWORD, NUMBER, OP, NAME])


class CPPRegex:
    def __init__(self):

        self.regex_groups = [STRING, COMMENT, KEYWORD, NUMBER, OP, NAME]

    def get_full_regex(self):
        return FULL_CPPREGEX

    def get_clean_indent_regex(self):
        return RM_INDENT

    def get_remove_doublespaces_regex(self):
        return RM_MULTIPLE_SPACES
