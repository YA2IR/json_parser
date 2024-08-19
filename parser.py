from enum import Enum


t = Enum("token_t", ["ILLEGAL","LCUR", "RCUR", "LBRACK", "RBRACK", "DQUOTE",
                    "STR", "NUM","TRUE", "FALSE", "NULL", "COLON", "COMMA", "EOF"])


class Token:

    def __init__(self, literal: str, token_t) -> None:
        self.literal = literal
        self.type = token_t

    def __str__(self) -> str:
        return f"<{self.type}  '{self.literal}' )>"

    def __eq__(self, token_t) -> bool:
        return self.type == token_t


class Lexer:

    def __init__(self, inpt: str) -> None: 
        self.inpt = inpt.replace('\\n', '\n')\
                        .replace('\\t', '\t')\
                        .replace('\\"', '"')\
                        .replace('\\\\', '\\') # TODO: Find a better way to do this

        self.curr_pos: int = 0
        self.next_pos: int = 0
        self.char: str = None
        self.read_char()

    def read_char(self) -> None:
        # Better than boundary checking imo 
        try:
            self.char = self.inpt[self.next_pos]
            self.curr_pos = self.next_pos
            self.next_pos += 1
        except IndexError:
            self.char = '\0'

    def next_token(self) -> Token:        

        self.consume_ws()

        match self.char:
            case '"':                
                self.read_char()            
                s = self.tokenize_str()
                tok = Token(s, t.STR)
                return tok
            case ',':
               tok = Token(self.char, t.COMMA)
            case ':':
                tok = Token(self.char, t.COLON)
            case "{":
                tok = Token(self.char, t.LCUR)
            case "}":
                tok = Token(self.char, t.RCUR)
            case "[":
               tok = Token(self.char, t.LBRACK)
            case "]":
                tok = Token(self.char, t.RBRACK)    
            case '\0':
                tok = Token(self.char, t.EOF) 

            case _:
                if self.char.isnumeric():
                    s = self.char
                    self.read_char()
                    while self.char != "," and self.char != "}" and self.char != "]":
                        s += self.char
                        self.read_char()
                    return Token(s, t.NUM)
                else:
                    tok = Token(self.char, t.ILLEGAL)

        self.read_char()
        return tok

    def tokenize_str(self) -> str:
        pos = self.curr_pos

        while self.char != '"':
            try:
                self.char = self.inpt[self.next_pos]
                self.next_pos += 1
            except IndexError:
                self.char = '\0'
                self.next_pos -= 1
                break

        self.read_char()

        return self.inpt[pos:self.curr_pos - 1]

    def consume_ws(self) -> None:
        while self.char == ' ' or self.char == '\n' or\
                self.char == '\t' or self.char == '\r':
            self.read_char()


class Parser:    

    def __init__(self, inpt:str):
        self.l = Lexer(inpt)
        self.curr_tok: Token = self.l.next_token()
        self.peek_tok: Token = self.l.next_token()
        self.json = {}

    def loads(inpt:str):
        p = Parser(inpt)
        return p.parse_value()

    def parse_value(self):
        match self.curr_tok.type:
            case t.LCUR:
                return self.parse_obj()
            case t.NUM: 
                return self.parse_num() 
            case t.LBRACK:
                return self.parse_arr()
            case t.STR:
                return self.parse_str()
            case t.ILLEGAL:
                raise Exception("Illegal Token")
            case t.EOF:
                return None
            case _:
                raise Exception(f"ERROR {self.curr_tok}")

    def parse_obj(self):
        obj = {}
        self.expect(t.LCUR, curr=True) 
        if self.peek_tok != t.RCUR:
            while self.curr_tok != t.RCUR: 
                # parsing whatever value (including nested objects) until you find a closing curly bracket
                self.expect(t.STR) 
                key = self.parse_str()
                self.expect(t.COLON)
                self.next_token()

                obj[key] = self.parse_value()

                if self.peek_tok == t.COMMA:
                    self.next_token()
                else: 
                    break

        self.expect(t.RCUR)
        return obj

    def parse_arr(self):
        self.expect(t.LBRACK, curr=True)
        l = []
        self.next_token()
        while self.curr_tok != t.RBRACK:
            l.append(self.parse_value()) 
            self.next_token() # next token after the value prased
            if self.curr_tok == t.COMMA: 
                self.next_token() 
            else:
                break

        self.expect(t.RBRACK, curr=True)
        return l
    
    
    def expect(self, token_t, curr=False): 
        """'curr' is an option to check the *current* token rather than the *next* one"""
        if not curr:
            self.next_token()
        if self.curr_tok != token_t:
            raise Exception(f"Expected {token_t} got {self.curr_tok}")

    def next_token(self):
       self.curr_tok = self.peek_tok
       self.peek_tok: Token = self.l.next_token() 

    def parse_str(self):
        return self.curr_tok.literal

    def parse_num(self):
        return eval(self.curr_tok.literal.strip())
