#### Parser with Semantic Analysis Made by Ben Schoonhoven

## Warning
The Scanner has not been updated to accept numbers with scientific notation, numbers with leading 0s, or numbers with a leading + sign. Do not try using the scanner to produce tokens with scientific notation, numbers with a + sign, or numbers with leading 0s. If you'd like to use the scanner to speed up the testing process for numbers, do so by first inputting a regular integer or float number in the ScannerInput file, run the scanner, then edit the desired tokens in the ScannerOutput file before running the parser. 

## How to Use
To input tokens into the parser, put the desired input in the ScannerOutput##.txt files where ## is the number of the file. The output of the parser will be saved in the ParserOutput##.txt files where ## is the same number that ScannerOutput file that the input came from. 
The first 10 ScannerOutput and ParserOutput files have been editted to include pre-made tests. The first 7 files test each semantic error with the number of the file being accociated directly with the type of semantic error it is trying produce. The last 3 files provided (08, 09, 10) are testing semantically correct input.


## Format
Token in the input files are to be put on their individual lines. No two tokens should be on the same line. The Parser will use the line number that a token is on to identify where the token is located in error outputs. The accepted types of tokens are as follows, where value is the stored value for that token:<STR, value>, <NUM, value>, <BOOL, value>, <null\>, <EOF\>, <{>, <}>, <[>, 
<]>, <,>, <;>, <:>. Tokens in any other format or with the token type named differently will not be accepted.

## Parser Error Handling and Recovery
The Error handling from part 2 has not been changed apart from the semantic error handling. Be aware the error handling from part 2 may show up in your tests and alter the expected output. Refer to the Parser Readme for the error handling capabilities.