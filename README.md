# source-code-tokenizer


### Installation:

#### pip + git

```
pip install git+https://github.com/matteogabburo/sourcecode-tokenizer.git
```


### Supported languages:

- Python


### Usage:

#### Python Tokenizer

```.py
# Import the right module
from source_code_tokenizer import PythonTokenizer

# Instantiate the tokeizer
tokenizer = PythonTokenizer()

code_example """i = 10
                i = 1 + i
                for j in range(i):
                    print(j * i)"""

# Tokenize the Python source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```