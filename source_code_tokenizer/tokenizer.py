import sys
import abc
import re
import random
from source_code_tokenizer.languages.python.regex import PYREGEX

class CodeTokenizer:

    def __init__(self):
        self.TOKENIZED = None
        self.setup_regex()

    @abc.abstractmethod
    def get_groups(self):
        r"""Return the list of groups tokenized by the tokenizer.
        """
        return sorted([k for k, v in self.TOKENIZED.groupindex.items()])

    @abc.abstractmethod
    def setup_regex(self):
        r"""This is the right place to initialize the self.TOKENIZED regular expression.

            example:
                self.TOKENIZED = re.compile(PYREGEX, re.MULTILINE)
        """

    @abc.abstractmethod
    def tokenize(self, text):
        """This method must take a string and return a list of tuples (value, type)
        """

class PythonTokenizer(CodeTokenizer):

    def setup_regex(self):

        # each regex should be a group
        self.TOKENIZED = re.compile(PYREGEX, re.MULTILINE)

    def tokenize(self, text):

        # identation and deidentation
        identation_size = None
        indent_tab = False
        indent_spaces = False
        last_indent_size = 0
        tokenized = []
        for tok in self.TOKENIZED.finditer(text):

            v, k = (tok.group(), tok.lastgroup)

            if k == "INDENT" and identation_size is None:

                if v[0] == '\t':
                    identation_size = 1
                    indent_tab = True
                elif v[0] == ' ':
                    identation_size = len(v)
                    indent_spaces = True
                else:
                    raise ValueError("Identation error. Value not recognized (must be a space or \\t).")

            if k == "INDENT" :
                
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

            # replace NEWLINE with \n
            if k == "NEWLINE" or k == "NL":
                v = "\n"
            
            tokenized.append((v, k))

        return tokenized