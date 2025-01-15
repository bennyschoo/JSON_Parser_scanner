from JsonScanner import Token, TokenType
import os
import JsonScanner

## Error that gets raised when there was an issue with scanning the tokens 
## from the token input
## Error outputs the line that it attempted to read and the location of it.
class TokenStreamError(Exception):
    def __init__(self, token_line: str, line_number: int) -> None:
        super().__init__(f"The token '{token_line}' at line {line_number+1} is not properly formatted and could not be read by the Tokenizer.")

## Error that gets thrown when the token that's expected isn't found
## Error outputs the expected tokens, the token that was found, 
## and the location of the token in the input stream
class UnexpectedTokenError(Exception):
    def __init__(self, token_types: list, given, token_num) -> None:
        output = 'Expected token(s): '
        self.given_type = given
        
        for i in token_types:
            output += i + ", "        
        
        output += f" but parser found {given} at token number {token_num}"
        super().__init__(output)

## Error that gets thrown when an empty dictionary is found by the parser
## Error outputs the location of the empty dictionary and the type of token being read when it was found
class EmptyDictionaryError(Exception):
    def __init__(self, token_location, token_type):
        super().__init__(f"Empty Dictionaries are not allowed. Found at token {token_location}, {token_type}")
        
## Error that gets thrown when an empty list is found by the parser
## Error outputs the location of the empty list and the type of token being read when it was found
class EmptyListError(Exception):
    def __init__(self, token_location, token_type):
        super().__init__(f"Empty Lists are not allowed. Found at token {token_location}, {token_type}")


## Error that gets thrown when a decimal number with the decimal at
## the start or end is given
class InvalidDecimalError(Exception):
    def __init__(self, token_value):
        super().__init__(f"Error type 1 at '{token_value}': Invalid Decimal Numbers") 

## Error that gets thrown when a pair with an empty key is given in a dictionary
class EmptyKeyError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 2 at '{token_value}': Empty Key Error")

## Error that gets thrown when a number is found in the wrong format (With a plus at the start or leading 0s)
class InvalidNumberError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 3 at '{token_value}': Invalid Number Error")

## Error that gets thrown when a reserved JSON keyword is given as a key
## in a dictionary pair
class ReservedWordAsKeyError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 4 at '{token_value}': Reserved Word as Key Error")

## Error that gets thrown when a dictionary is found with two of the same keys
class DuplicateKeyError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 5 at '{token_value}': Duplicate Key Error")

## Error that gets thrown when a list storing multiple different datatypes is found
class ListTypeError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 6 at '{token_value}': List Type Error")

## Error that gets thrown when a JSON reserved key word is used in any string
class ReservedWordError(Exception):
    def __init__(self, token_value) -> None:
        super().__init__(f"Error type 7 at '{token_value}': Reserved Word as String Error")   

## This class defines the types of possible values
## This class is used in the JSONValue class to keep track
## of what type of value an object instance is.
class ValueType:
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"
    LIST = "LIST"
    DICTIONARY = "DICTIONARY"
    BOOL = "BOOL"
    NULL = "NULL"
    
"""This is a wrapper class for all types of JSON values
JSON values can be store inside other JSON values.
for example a JSONValue list stores JSONValues
Since every value is stored in this JSONValue wrapper, I am able to
create a recursive printing function to output the tree representation
for any type of json value."""
class JSONValue:
    def __init__(self, type, value):
        ## any type of value can be stored
        self.value = value
        self.type = type
    ## returns the tree representation of this value as a string
    def __repr__(self) -> str:
        return self.recursive_print(0)
    
    """For values that aren't collections(not a list or dict), this function 
    returns a string representation of the value with an indent.
    For values such as list and dict, this method recursively formats the contained
    data as a tree structure in a string"""
    def recursive_print(self, depth):
        ## different types of indents needed for different lines
        indent = " " * (depth)
        
        ## The 4 following if statements are for non-collection values
        if self.type == ValueType.BOOL:
            return (str)(self.value).lower()
        
        if self.type == ValueType.FLOAT:
            return (str)(self.value)
        
        if self.type == ValueType.INT:
            return (str)(self.value)

        if self.type == ValueType.STRING:
            return f'"{self.value}"'
                
        if self.type == ValueType.NULL:
            return "null"
            
            
        ## if the value is a list or a dictionary, 
        ## iterate through each element and call the recursive print function on it
        if self.type == ValueType.DICTIONARY:
            output = '{\n'
            
            for key in self.value:
                output += indent + f'  {key}: '
                output += self.value[key].recursive_print(depth+4+len(key)) + '\n'
            output += indent + '}'
            return output
        
        if self.type == ValueType.LIST:
            output = '[\n'
            
            for values in self.value:
                output += indent + "  " +  values.recursive_print(depth+2) + '\n'
            output += indent + ']'
            
            return output
        
                
            
            
"""The Tokenizer class handles the scanning and storing of the input tokens"""    
class Tokenizer:
    
    ## when initialized, turn the input string of tokens into a list of token objects
    def __init__(self, input: str) -> None:
        self.input = input.split('\n')
        self.current_index = -1
        self.tokens = []
        
        ## iterating through each line in the string
        for index, token_line in enumerate(self.input):
            try:
                ## try to scan the line for a token
                token = self.tokenize_string(token_line)
                
                ##if no token is found, throw a token stream error
                if token is not None:
                    self.tokens.append(token)
                else:
                    raise TokenStreamError(token_line, index)
                
                if token.type == TokenType.EOF:
                    break
            except:
                raise TokenStreamError(token_line, index)
                
            
    def tokenize_string(self, input: str) -> Token:
        ## split the line based on the expected symbols
        ## vals should either be a list with 1 value, representing single character token
        ## or a list with 2 values, representing token type and the value with it.
        ## Only exception is the comma token, since the input is being split based on comma
        ## For the comma token, vals should be a list with 2 empty strings
        line = input
        line = line.split("<")[1]
        line = line.split(">")[0]
        vals = line.split(',',1)
        
        ## remove all whitespace preceeding the values found in each token
        for i, val in enumerate(vals):
            vals[i] = val.lstrip()
        
        ## determine the token type and value
        if len(vals)==1 or (len(vals)==2 and vals[0]=='' and vals[1]==''):
            value = vals[0]
            if value ==':':
                return Token(TokenType.COLON, value)
            if value ==';':
                return Token(TokenType.SEMICOLON, value)
            if value =='':
                return Token(TokenType.COMMA, ',')
            if value == '{':
                return Token(TokenType.LBRACE, value)
            if value == '}':
                return Token(TokenType.RBRACE, value)
            if value == '[':
                return Token(TokenType.LBRACKET, value)
            if value == ']':
                return Token(TokenType.RBRACKET, value)
            if value == 'EOF':
                return Token(TokenType.EOF, value)
            if value == 'null':
                return Token(TokenType.NULL, 'null')
            
        if len(vals)==2:
            return Token(vals[0],vals[1])
                
    ## iterate through the list of tokens, return the next token
    def next_token(self):
        self.current_index+=1
        if self.current_index<len(self.tokens):
            return self.tokens[self.current_index]
        else:
            return None


"""This class handles the parsing of all values in json"""
class Parser:
    ## initialize a tokenizer to get the tokens from the given string input
    def __init__(self, input) -> None:
        self.tokenizer = Tokenizer(input)
        self.current_token = None
    
    ## get the next token
    def next_token(self):
        current = self.current_token
        self.current_token = self.tokenizer.next_token()
        return current

    ## method used to compare the current token with the expected token.
    ## if the expected token and current token don't match, throw Unexpected token error
    ## if they do match, return the token for the value to be extracted
    def eat(self, expected_type):
        
        if self.current_token.type == expected_type:
            return self.next_token()
        else:
            raise UnexpectedTokenError([expected_type],self.current_token.type, self.tokenizer.current_index)
    
    ## beings the parsing process on the token stream
    ## the final returned value is a JSONValue object 
    ## which can be infinitely nested with other JSONValues
    def parse(self):
        self.next_token()
        parsed_value = self.parse_value()
        self.eat(TokenType.EOF)
        return parsed_value
        
    ## Determines the JSONValue to be returned based on the current token
    def parse_value(self):
        if self.current_token.type == TokenType.STRING:
            token = self.eat(TokenType.STRING)
            
            ## Raising semantic Error of type 7
            if token.value in ['true', 'false', 'null']:
                raise ReservedWordError(token.value)
            
            return JSONValue(ValueType.STRING, token.value)    
            
        elif self.current_token.type == TokenType.BOOL:
            token = self.eat(TokenType.BOOL)
            if token.value == 'true':
                return JSONValue(ValueType.BOOL, True)
            elif token.value == 'false':
                return JSONValue(ValueType.BOOL, False)
            
        elif self.current_token.type == TokenType.NUM:
            return self.parse_num()
            
        elif self.current_token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return JSONValue(ValueType.NULL, None)
        
        ## if the token is bracket or brace, call seperate method to parse dict or list
        elif self.current_token.type == TokenType.LBRACE:
            return JSONValue(ValueType.DICTIONARY, self.parse_dict())
        
        elif self.current_token.type == TokenType.LBRACKET:
            return JSONValue(ValueType.LIST, self.parse_list())
        
        ## if none of the tokens matched the expected tokens for a value, throw unexpected token error
        else:
            raise UnexpectedTokenError([TokenType.STRING, TokenType.BOOL, TokenType.NUM, TokenType.NULL, TokenType.LBRACE, TokenType.LBRACKET], self.current_token.type, self.tokenizer.current_index)
        
    
    ## method that handles the parsing of dictionaries
    def parse_dict(self):
        self.eat(TokenType.LBRACE)
        dictionary = {}
        keys = []
        
        ## get the first pair in the dictionary
        pair = self.parse_pair()
        if pair is not None:
            dictionary[pair[0]] = pair[1]
            keys.append(pair[0])
            
        ## get any following pairs seperated by a comma
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            pair = self.parse_pair()
            
            ## if the returned pair is None (no pair was given between comma's)
            ## don't add it to the dict
            if pair is not None:
                ## Raising error of type 5
                if pair[0] in keys:
                    raise DuplicateKeyError(pair[0])
                dictionary[pair[0]] = pair[1]
                keys.append(pair[0])
        
        self.eat(TokenType.RBRACE)
        
        ## cannot have empty dictionary according to grammer
        ## throw error if dictionary is empty
        if len(dictionary)==0:
            raise EmptyDictionaryError(self.tokenizer.current_index, self.current_token.type)

        return dictionary
        
    ## method that handles parsing of pairs specifically
    def parse_pair(self):
        key = self.current_token.value
        token = None
        ## (Error recovery)
        ## handling error where neither a key or value is given
        ## return empty pair
        try:
            token = self.eat(TokenType.STRING)
        except UnexpectedTokenError as e:
            if e.given_type == TokenType.RBRACE or e.given_type == TokenType.COMMA:
                return None
            else:
                raise e
        
        ## Raising semantic error of type 2
        if key.isspace() or key == '':
            raise EmptyKeyError(token.value)
        
        ## Raising semantic error of type 4
        if key in ['true', 'false', 'null']:
            raise ReservedWordAsKeyError(token.value)
        
        ## (Error recovery)
        ## handling error where a value isn't given
        ## for a pair in a dictionary.
        ## assumed to be null.
        try:
            ## (Error recovery)
            ## if colon is not found, try semicolon
            try:
                self.eat(TokenType.COLON)
            except Exception:
                self.eat(TokenType.SEMICOLON)
                
            value = self.parse_value()
        except UnexpectedTokenError as e:
            if e.given_type == TokenType.RBRACE:
                value = JSONValue(ValueType.NULL, None)
            else:
                raise e
        return (key, value)
    
    ## method that handles parsing of lists specifically
    def parse_list(self):
        self.eat(TokenType.LBRACKET)
        list = []
        type = ""
        
        ## handling common error where extra commas may be given preceeding
        ## if a comma token has been found instead of a string, skip the token and continue
        try:
            list.append(self.parse_value())
            type = list[-1].type
        except UnexpectedTokenError as e:
            if e.given_type != TokenType.COMMA and e.given_type != TokenType.RBRACKET:
                raise e
            
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            ## handling common error where extra commas may be given
            ## if a comma token has been found instead of a string, skip the token and continue
            try:
                list.append(self.parse_value())
                if type == "":
                    type = list[-1].type
                ## Raising semantic error of type 6
                elif type != list[-1].type:
                    raise ListTypeError(list[-1].value)
                
            except UnexpectedTokenError as e:
                if e.given_type != TokenType.COMMA and e.given_type != TokenType.RBRACKET:
                    raise e
                
        self.eat(TokenType.RBRACKET)
        
        ## Throw error if the list is empty, empty lists are not allowed in the given language
        if len(list)==0:
            raise EmptyListError(self.tokenizer.current_index, self.current_token.type)
        
        return list
        
    def parse_num(self):
        token = self.eat(TokenType.NUM)
        
        ## Raising semantic Error of type 1
        if token.value[0]=='.' or token.value[-1]=='.':
            raise InvalidDecimalError(token.value)
        
        ## Raising semantic Error of type 3
        if token.value[0]=='+' or (len(token.value)!=1 and token.value[0] == '0' and token.value[:2] != '0.'):
            raise InvalidNumberError(token.value)
        
        if 'e' in token.value:
            ##If the scientific value is a whole number, return as integer
            if (float)(token.value).is_integer():
                return JSONValue(ValueType.INT, (int)((float)(token.value)))
            
            return JSONValue(ValueType.FLOAT, (float)(token.value))
        elif '.' in token.value:
            return JSONValue(ValueType.FLOAT, (float)(token.value))
        
        else:
            return JSONValue(ValueType.INT, (int)(token.value))
        
        

def main():
    
    ## Comment out the line below to input your own tokens into the ScannerOutput files!
    ## if not commented, the scanner will be run each time and the ScannerOutput files
    ## will be replaced with the tokens read from ScannerInput files.
    
    JsonScanner.main()
    
    ##Go through each input file (ScannerOutput), get the parsers output,
    ##and store output in a file
    ##If parser throws error, print the error in the file and continue with the remaining files
    for i in range(1, 21):
        file_name = f"ParserInputs/ScannerOutput{i:02d}.txt"
        if os.path.isfile(file_name):
            try:
                with open(file_name, 'r') as file:
                    input_string = file.read()
                    parser = Parser(input_string)
                with open(f'ParserOutputs/ParserOutput{i:02d}.txt', 'w') as f:
                    output_string = parser.parse().__repr__()
                    f.write(output_string)
            except Exception as e:
                with open(f'ParserOutputs/ParserOutput{i:02d}.txt', 'w') as f:
                    output_string = repr(e)
                    f.write(output_string)
        else:
            print(f"{file_name}: File not found")


    

if __name__ == "__main__":
    main()