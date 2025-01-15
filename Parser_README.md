#### Parser Made by Ben Schoonhoven

## How to Use
To input tokens into the parser, put the desired input in the ScannerOutput##.txt files where ## is the number of the file. The output of the parser will be saved in the ParserOutput##.txt files where ## is the same number that ScannerOutput file that the input came from.

## Format
Token in the input files are to be put on their individual lines. No two tokens should be on the same line. The Parser will use the line number that a token is on to identify where the token is located in error outputs. The accepted types of tokens are as follows, where value is the stored value for that token:<STR, value>, <NUM, value>, <BOOL, value>, <null\>, <EOF\>, <{>, <}>, <[>, 
<]>, <,>, <;>, <:>

Tokens in any other format or with the token type named differently will not be accepted.

## Error Handling
There are 4 types of Errors that get thrown to the user, which get printed in the ParserOutput files.
The first error is the TokenStreamError, and gets thrown thrown when the token scanner comes across a line where it couldn't recognize any token. The second Error, UnexpectedTokenError, gets thrown when a token is found instead of the expected token and the error couldn't be recovered from. The last 2 errors, EmptyDictionaryError and EmptyListError, get thrown when an empty dictionary or list is encountered, which is not allowed in the CFL we are supposed to follow for JSON.

## Error Recovery
There are 4 seperate errors that I've developed a recovery method for. The first is if no value is given for a pair in a dictionary, the value is assumed to be null. For the second recovery, if a semi-colon is accidentally given instead of a colon in a pair, the parser accepts it anyways. For the last 2 recoveries, in both lists and dictionaries, if any extra commas are given before or after any values, they will be ignored and no values will be recorded by the parser. 