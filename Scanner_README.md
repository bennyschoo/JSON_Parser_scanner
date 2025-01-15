
#### Scanner Made by Ben Schoonhoven

# How it Works

---

This Scanner program takes the txt files in the ./tests directory from test01.txt up to test99.txt and uses them as input. The program then tokenizes the input, expecting properly formatted json code. The tokenized output is stored in the ./outputs directory in files output01.txt to output99.txt respective to their test file.
if the test file is empty, the output will be empty. There is no need to use all the test files, they are just provided to give as much room for testing as possible

### How to Use

Put the test inputs in each test txt file given, the output will be placed in the output file with the same number as the input file. If you'd like to copy your own test files into the program, make sure they have the naming scheme test##.txt where ## is 01-99.



### Strings
Strings are expected to be contained with double quotation marks as they would be with proper json. The only difference from regular json strings and the strings recognized by this scanner is that there are no escape characters or symbols such as '\n' or '\t'. All characters other than double quotes will be considered part of the string.
### Numbers
Numbers will be recognized exactly as they are in json. Decimals will be accepted. If a decimal is given, there has to be a number after the point or it will not be accepted. One or more 0s preceeding any other numbers will not be accepted.
### Tokens
Tokens are outputted as tuples only if it is a string, number or boolean. Null and all single characters will be output as a single cell token. However, this is not how they are stored, all tokens are stored as tuples.

# How it's Implemented
---
The Detection of all Tokens that aren't single characters are taken care of by if statement implementation of DFAs. The functions recognize_string, recognize_bool, and recognize_null all use DFAs to operate them. recognize_num() has been changed to work around some changes in the parsers accepted input, it was more efficient to implement without using DFAs.
There are two types of errors that are thrown by the Lexer class. The first, LexerError indicates when the inputted string has incorrect characters or an incorrect sequence of characters that aren't accepted in the json language. The Second error, EndOfInputError, is thrown when the Lexer reaches the end of input while still trying to determine a string. This is caused by missing quotation marks.
All Errors are printed out into the respective output files and not thrown into the console. That way all tests run without the program stopping.