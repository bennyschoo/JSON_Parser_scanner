import os
import traceback

class TokenType:
    STRING = 'STR'
    NUM = 'NUM'
    BOOL = "BOOL"
    NULL = 'NULL'
    EOF = 'EOF'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    COMMA = 'COMMA'
    COLON = 'COLON'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEMICOLON = 'SEMICOLON'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        if self.type in [TokenType.NUM, TokenType.STRING, TokenType.BOOL]:
            return f'<{self.type}, {self.value}>'
        else:
            return f'<{self.value}>'
    
       
class LexerError(Exception):
    def __init__(self, position, string) -> None:
        self.position = position
        self.string = string
        super().__init__(f"'{string}' is invalid at position {position}")

class EndOfInputError(Exception):
    def __init__(self, position, string) -> None:
        super().__init__(f"Lexer reached end of input while tokenizing lexeme: {string} at position {position}\nTry adding Quotation marks at the end if it's a string.")
        
        
class Lexer: 
    def __init__(self, input) -> None:
        self.symbol_table = {}
        self.input = input
        self.current_char = self.input[self.position] if self.input else None

    def __init__(self):
        self.symbol_table = {}
        self.input = ''
        self.current_char = ''

    def advance(self):
        self.position += 1

        if self.position<len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None
            

    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()    


    def recognize_string(self):
        states={
            "START":0,
            "STRING":1,
            "END":3,
            "REJECTED":4
        }
        result = ''
        current_state = states['START']
        final_state = states['END']

        while self.current_char is not None and current_state != states['END']:
            #This if block is the entire DFA for recognizing a string
            if current_state == states["START"] and self.current_char == '"':
                current_state = states['STRING']
            elif current_state == states['STRING']:
                if self.current_char == '"':
                    current_state = states['END']
            else:
                current_state = states['REJECTED']
                
            if current_state == states['REJECTED']:
                break
            
            if self.current_char!='"':
                result+= self.current_char
            self.advance()
            
        #Check if the final state hasn't been reached
        if current_state != final_state:
            if len(result)==0:  
                raise EndOfInputError(self.position, self.current_char)
            else:
                raise EndOfInputError(self.position, result)

        self.symbol_table[result] = TokenType.STRING
        return Token(TokenType.STRING, result)
    
    
    #This method uses the number DFA given in the PDF 
    #to recognize numbers and tokenize them
    def recognize_num(self):
        result = ''
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char in ['+','-','.','e']):
            result+=self.current_char
            self.advance()
        
        return Token(TokenType.NUM, result)



    def recognize_bool(self):
        states = {
            "START":0,
            "T":1,
            "R":2,
            "U":3,
            "F":4,
            "A":5,
            "L":6,
            "S":7,
            "E":8,
            "REJECT":9
        }
        result = ''
        final_state = states['E']
        current_state = states['START']
        
        while self.current_char is not None and (self.current_char in ['t','r','u','e','f','a','l','s']):
            #Entire boolean dfa is in this if block. It checks for both true and false
            if current_state == states['START'] and self.current_char == 't':
                current_state = states['T']
            elif current_state == states['T'] and self.current_char == 'r':
                current_state = states['R']
            elif current_state == states['R'] and self.current_char == 'u':
                current_state = states['U']
            elif current_state == states['U'] and self.current_char == 'e':
                current_state = states['E']
            elif current_state == states['START'] and self.current_char == 'f':
                current_state = states['F']
            elif current_state == states['F'] and self.current_char == 'a':
                current_state = states['A']
            elif current_state == states['A'] and self.current_char == 'l':
                current_state = states['L']
            elif current_state == states['L'] and self.current_char == 's':
                current_state = states['S']
            elif current_state == states['S'] and self.current_char == 'e':
                current_state = states['E']
            else:
                current_state = states['REJECT']
                
            if current_state == states['REJECT']:
                break
            
            result+=self.current_char
            self.advance()
        
        
        #Check if the final state hasn't been reached
        if current_state != final_state:
            if len(result)==0:  
                raise LexerError(self.position, self.current_char)
            else:
                raise LexerError(self.position, result) 
                
        
        return Token(TokenType.BOOL, result)

        
    def recognize_null(self):
        states = {
            "START":0,
            "N":1,
            "U":2,
            "L1":3,
            "L2":4,
            "REJECTED":5
        }
        result = ''
        current_state = states['START']
        final_state= states['L2']
        
        while self.current_char is not None and self.current_char in ['n','u','l','l']:
            #Entire DFA for null is in this if block
            if current_state == states["START"] and self.current_char == 'n':
                current_state = states["N"]
            elif current_state == states["N"] and self.current_char =='u':
                current_state = states['U']
            elif current_state == states['U'] and self.current_char == 'l':
                current_state = states['L1']
            elif current_state == states['L1'] and self.current_char == 'l':
                current_state = states['L2']
            else:
                current_state = states['REJECTED']
                
            result += self.current_char
            self.advance()
         
        #Check if the final state hasn't been reached
        if current_state != final_state:
            if len(result)==0:  
                raise LexerError(self.position, self.current_char)
            else:
                raise LexerError(self.position, result)
            
        return Token(TokenType.NULL, result)
      
        
    def get_next_token(self):
        if self.current_char is not None:
            self.skip_white_space()
            
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{')
            if self.current_char == '"':
                return self.recognize_string()
            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':')
            if self.current_char.isdigit() or self.current_char in ['-','.','+']:
                return self.recognize_num()
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[')
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']')
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}')
            if self.current_char == 'n':
                return self.recognize_null()
            if self.current_char == 't' or self.current_char == 'f':
                return self.recognize_bool()
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';')
            
            raise LexerError(self.position, self.current_char)
        
        return Token(TokenType.EOF,TokenType.EOF)
        
    def tokenize(self, input):
        tokens = []
        self.input = input
        self.position = 0
        self.current_char = self.input[self.position] if self.input else None
        self.symbol_table = {}
        token = Token(None,None)
        while token.type != TokenType.EOF:
            token = self.get_next_token()     
            tokens.append(token)
            
        return tokens

def main():
    lexer = Lexer()
    for i in range(1, 21):
        file_name = f"ScannerInputs/ScannerInput{i:02d}.txt"
        if os.path.isfile(file_name):
            try:
                with open(file_name, 'r') as file:
                    input_string = file.read().strip()
                    tokens = lexer.tokenize(input_string)
                with open(f'ParserInputs/ScannerOutput{i:02d}.txt', 'w') as f:
                    output_string = ''
                    for token in tokens:
                        output_string += token.__repr__() +'\n'
                    f.write(output_string)
            except Exception as e:
                with open(f'ParserInputs/ScannerOutput{i:02d}.txt', 'w') as f:
                    output_string = traceback.format_exc()
                    f.write(output_string)
        else:
            print(f"{file_name}: File not found")

if __name__ == "__main__":
    main()
