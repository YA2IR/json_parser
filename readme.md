## About
This is a JSON parser that:
- Tokenizes a JSON file 
- Parses the resulting tokens
- Returns a python object representing the JSON data (dict, for example)

You can find JSON examples in the **examples** directory, and you can find a test in **test_parser.py**, where it asserts that "**parser.loads(data) == json.loads(data)**" for the JSON example files.

<br>

## Details
**parser.py** contains three classes:
- Token 
    - the class that represents a single token, which is a pair of:
        - the token type (for example: left bracket) 
    and 
        - a literal (for example: "[")
- Lexer
    - the class that is responsible for generating these tokens
- Parser
    - the class that is responsible for parsing the tokens, i.e., making sure they are syntactically correct and converting them into a Python representation

## Limitation
-It lacks a more specific error handling (no detailed exceptions)
