import sys
import abc
import re
import random
from source_code_tokenizer.languages.python.regex import PyRegex
from source_code_tokenizer.languages.c.regex import CRegex
from source_code_tokenizer.languages.cpp.regex import CPPRegex
from source_code_tokenizer.languages.java.regex import JavaRegex
from source_code_tokenizer.languages.js.regex import JSRegex


class CodeTokenizer:
    def __init__(self):
        self.TOKENIZED_STR = None
        self.TOKENIZED = None
        self.setup_regex()

    def get_groups(self):
        r"""Return the list of groups tokenized by the tokenizer."""
        return sorted([k for k, v in self.TOKENIZED.groupindex.items()])

    def get_regex(self):
        return self.TOKENIZED_STR

    @abc.abstractmethod
    def setup_regex(self):
        r"""This is the right place to initialize the self.TOKENIZED regular expression.

        example:
            self.TOKENIZED = re.compile(PYREGEX, re.MULTILINE)
        """

    @abc.abstractmethod
    def tokenize(self, text):
        """This method must take a string and return a list of tuples (value, type)"""

    @abc.abstractmethod
    def get_line_terminators(self, text):
        """This method return the list of line terminators of the language"""


class PythonTokenizer(CodeTokenizer):
    def __init__(self):
        super().__init__()
        self.str_headers = PyRegex().get_str_headers()

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED_STR = PyRegex().get_full_regex()
        self.TOKENIZED = re.compile(self.TOKENIZED_STR, re.MULTILINE)

    def tokenize(self, text):

        last_indent_size = 0
        tokenized = []

        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            # identation and deidentation
            """
            # dynamic tabulation size
            if k == "INDENT" and identation_size is None:

                if v[0] == '\t':
                    identation_size = 1
                    indent_tab = True
                elif v[0] == ' ':
                    identation_size = len(v)
                    indent_spaces = True
                else:
                    raise ValueError("Identation error. Value not recognized (must be a space or \\t).")
            """

            if k == "INDENT":

                """
                if v[0] == ' ' and indent_spaces:
                    pass
                elif v[0] == '\t' and indent_tab:
                    pass
                else:
                    raise Exception("Identation error: only a type of tabulation is allowed (not spaces and tabs in the same program)")

                if len(v) % identation_size > 0:
                    raise Exception("Identation error: the tabulation is inconsistent")

                # decide if it is an indentation or a deindentation
                if len(v) >= last_indent_size:
                    k = "INDENT"
                else:
                    k = "DEINDENT"
                last_indent_size = len(v)

                # add all but one tabs (it will be add at the end of the cycle)
                for _ in range(int(len(v) / identation_size)-1):
                    tokenized.append((v[0] * identation_size, k))
                """
                # decide if it is an indentation or a deindentation
                if len(v) >= last_indent_size:
                    k = "INDENT"
                else:
                    k = "DEINDENT"
                last_indent_size = len(v)

                tokenized.append((v, k))

            # replace NEWLINE with \n
            if k == "NEWLINE" or k == "NL":
                v = "\n"

            # check strings errors
            def check_strings(s):

                if k == "STRING":
                    # string must be longher than 1 and bos and eos must be in [",'] and equal
                    # WARNING: a string can also start with (b|r|u|f|br|fr)
                    to_remove = max(
                        [len(h) if s.startswith(h) else 0 for h in self.str_headers]
                    )
                    v = s[to_remove:]
                    if not (len(v) > 1 and v[0] == v[-1] and v[0] in ['"', "'"]):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING"
                        )

                if k == "STRING_M":
                    # string must be longher than 5 and bos and eos must be in [""",'''] and equal
                    # WARNING: a string can also start with (b|r|u|f|br|fr)
                    to_remove = max(
                        [len(h) if s.startswith(h) else 0 for h in self.str_headers]
                    )
                    v = s[to_remove:]
                    if not (len(v) > 5 and v[:3] == v[-3:] and v[:3] in ['"""', "'''"]):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING_M"
                        )

            check_strings(v)

            tokenized.append((v, k))

        return tokenized

    def get_line_terminators(self):
        return ["\n"]


class CTokenizer(CodeTokenizer):
    def __init__(self):
        super().__init__()
        self.RM_INDENTATION = re.compile(
            CRegex().get_clean_indent_regex(), re.MULTILINE
        )
        self.RM_SPACES = re.compile(CRegex().get_remove_doublespaces_regex())

        self.str_headers = CRegex().get_str_headers()
        self.chr_headers = CRegex().get_chr_headers()

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED_STR = CRegex().get_full_regex()
        self.TOKENIZED = re.compile(self.TOKENIZED_STR, re.MULTILINE)

    def tokenize(self, text):

        # minify the input removing all the not necessary spaces
        def remove_spaces(matchobj):
            return " " if matchobj.group(2) is not None else matchobj.group(1)

        text = self.RM_INDENTATION.sub(remove_spaces, text)
        text = self.RM_SPACES.sub(" ", text).strip()

        tokenized = []

        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            # check string and comment errors
            def check(s):

                if k == "STRING":
                    # string must be longer than 1 and bos and eos must be equal to "
                    # WARNING: a string can also start with some prefix
                    to_remove = max(
                        [len(h) if s.startswith(h) else 0 for h in self.str_headers]
                    )
                    v = s[to_remove:]
                    if not (len(v) > 1 and v[0] == v[-1] and v[0] == '"'):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING"
                        )

                if k == "CHAR":
                    # char must be longer than 1 and bos and eos must be equal to '
                    if not (len(s) > 1 and s[0] == s[-1] and s[0] == "'"):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing CHAR"
                        )

                if k == "COMMENT":
                    # if comment starts with "/*" len should be higher than 3 and it must finish with "*/"
                    if len(s) > 1 and s.startswith("/*"):
                        if not (len(s) > 3 and s[-2:] == "*/"):
                            raise Exception(
                                "Error on string delimiters occurred while tokenizing COMMENT"
                            )

            check(v)

            tokenized.append((v, k))

        return tokenized

    def get_line_terminators(self):
        return [";"]


class CPPTokenizer(CodeTokenizer):
    def __init__(self):
        super().__init__()
        self.RM_INDENTATION = re.compile(
            CPPRegex().get_clean_indent_regex(), re.MULTILINE
        )
        self.RM_SPACES = re.compile(CPPRegex().get_remove_doublespaces_regex())

        self.str_headers = CPPRegex().get_str_headers()
        self.chr_headers = CPPRegex().get_chr_headers()

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED_STR = CPPRegex().get_full_regex()
        self.TOKENIZED = re.compile(self.TOKENIZED_STR, re.MULTILINE)

    def tokenize(self, text):

        # minify the input removing all the not necessary spaces
        def remove_spaces(matchobj):
            return " " if matchobj.group(2) is not None else matchobj.group(1)

        text = self.RM_INDENTATION.sub(remove_spaces, text)
        text = self.RM_SPACES.sub(" ", text).strip()

        tokenized = []

        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            # check string and comment errors
            def check(s):

                if k == "STRING":
                    # string must be longer than 1 and bos and eos must be equal to "
                    # WARNING: a string can also start with some prefix
                    to_remove = max(
                        [len(h) if s.startswith(h) else 0 for h in self.str_headers]
                    )
                    v = s[to_remove:]
                    if not (len(v) > 1 and v[0] == v[-1] and v[0] == '"'):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING"
                        )

                if k == "CHAR":
                    # char must be longer than 1 and bos and eos must be equal to '
                    # WARNING: a char can also start with some prefix
                    to_remove = max(
                        [len(h) if s.startswith(h) else 0 for h in self.chr_headers]
                    )
                    v = s[to_remove:]
                    if not (len(v) > 1 and v[0] == v[-1] and v[0] == "'"):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing CHAR"
                        )

                if k == "COMMENT":
                    # if comment starts with "/*" len should be higher than 3 and it must finish with "*/"
                    if len(s) > 1 and s.startswith("/*"):
                        if not (len(s) > 3 and s[-2:] == "*/"):
                            raise Exception(
                                "Error on string delimiters occurred while tokenizing COMMENT"
                            )

            check(v)

            tokenized.append((v, k))

        return tokenized

    def get_line_terminators(self):
        return [";"]


class JavaTokenizer(CodeTokenizer):
    def __init__(self):
        super().__init__()
        self.RM_INDENTATION = re.compile(
            JavaRegex().get_clean_indent_regex(), re.MULTILINE
        )
        self.RM_SPACES = re.compile(JavaRegex().get_remove_doublespaces_regex())

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED_STR = JavaRegex().get_full_regex()
        self.TOKENIZED = re.compile(self.TOKENIZED_STR, re.MULTILINE)

    def tokenize(self, text):

        # minify the input removing all the not necessary spaces
        def remove_spaces(matchobj):
            return " " if matchobj.group(2) is not None else matchobj.group(1)

        text = self.RM_INDENTATION.sub(remove_spaces, text)
        text = self.RM_SPACES.sub(" ", text).strip()

        tokenized = []

        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            # check string and comment errors
            def check(s):

                if k == "STRING":
                    # string must be longer than 1 and bos and eos must be equal to "
                    if not (len(s) > 1 and s[0] == s[-1] and s[0] == '"'):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING"
                        )

                if k == "CHAR":
                    # char must be longer than 1 and bos and eos must be equal to '
                    if not (len(s) > 1 and s[0] == s[-1] and s[0] == "'"):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing CHAR"
                        )

                if k == "COMMENT":
                    # if comment starts with "/*" len should be higher than 3 and it must finish with "*/"
                    if len(s) > 1 and s.startswith("/*"):
                        if not (len(s) > 3 and s[-2:] == "*/"):
                            raise Exception(
                                "Error on string delimiters occurred while tokenizing COMMENT"
                            )

            check(v)

            tokenized.append((v, k))

        return tokenized

    def get_line_terminators(self):
        return [";"]


class JSTokenizer(CodeTokenizer):
    def __init__(self):
        super().__init__()
        self.RM_INDENTATION = re.compile(
            JSRegex().get_clean_indent_regex(), re.MULTILINE
        )
        self.RM_SPACES = re.compile(JSRegex().get_remove_doublespaces_regex())

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED_STR = JSRegex().get_full_regex()
        self.TOKENIZED = re.compile(self.TOKENIZED_STR, re.MULTILINE)

    def tokenize(self, text):

        # minify the input removing all the not necessary spaces
        def remove_spaces(matchobj):
            return " " if matchobj.group(2) is not None else matchobj.group(1)

        text = self.RM_INDENTATION.sub(remove_spaces, text)
        text = self.RM_SPACES.sub(" ", text).strip()

        tokenized = []

        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            # check string and comment errors
            def check(s):

                if k == "STRING":
                    # string must be longer than 1 and bos and eos must be in [", ', `]
                    if not (len(s) > 1 and s[0] == s[-1] and s[0] in ['"', "'", "`"]):
                        raise Exception(
                            "Error on string delimiters occurred while tokenizing STRING"
                        )

                if k == "COMMENT":
                    # if comment starts with "/*" len should be higher than 3 and it must finish with "*/"
                    if len(s) > 1 and s.startswith("/*"):
                        if not (len(s) > 3 and s[-2:] == "*/"):
                            raise Exception(
                                "Error on string delimiters occurred while tokenizing COMMENT"
                            )

            check(v)

            tokenized.append((v, k))

        return tokenized

    def get_line_terminators(self):
        return [";"]
