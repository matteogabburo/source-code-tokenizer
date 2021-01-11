# source-code-tokenizer


### Installation:

#### pip + git

```
pip install git+https://github.com/matteogabburo/source-code-tokenizer.git
```


### Supported languages:

- Python
- C
- C++
- Java
- JS

### Usage:

#### Python Tokenizer

```.py
# Import the right module
from source_code_tokenizer import PythonTokenizer

# Instantiate the tokeizer
tokenizer = PythonTokenizer()

code_example =  """
                    # the hello world program
            
                    print("Hello World!")
                """

# Tokenize the Python source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```

#### C Tokenizer

```.py
# Import the right module
from source_code_tokenizer import CTokenizer

# Instantiate the tokeizer
tokenizer = CTokenizer()

code_example =  """
                    // the hello world program

                    #include <stdio.h>
                    main ()
                    {
                        printf("Hello World!");
                    }
                """

# Tokenize the C source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```

#### C++ Tokenizer

```.py
# Import the right module
from source_code_tokenizer import CPPTokenizer

# Instantiate the tokeizer
tokenizer = CPPTokenizer()

code_example =  """
                    // the hello world program
                    
                    #include <iostream>
                    int main() {
                        std::cout << "Hello World!";
                        return 0;
                    }
                """

# Tokenize the C++ source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```

#### Java Tokenizer

```.py
# Import the right module
from source_code_tokenizer import JavaTokenizer

# Instantiate the tokeizer
tokenizer = JavaTokenizer()

code_example =  """ 
                    // the hello world program

                    class HelloWorld {
                        public static void main(String[] args) {
                            System.out.println("Hello World!"); 
                        }
                    }
                """

# Tokenize the Java source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```

#### JS Tokenizer

```.py
# Import the right module
from source_code_tokenizer import JSTokenizer

# Instantiate the tokeizer
tokenizer = JSTokenizer()

code_example =  """
                    // the hello world program

                    console.log('Hello World!');
                """

# Tokenize the JS source-code given as example
tokenized = tokenizer.tokenize(code_example)

print(tokenized)
```