#### Scanner and Parser Project Made by Ben Schoonhoven

## Overview
This is a 3 part project, having 3 seperate ReadMe files for each part. There is a ReadMe for the Scanner, which was created before the parser
and semantic analysis portions were created. Because of this, there may be some discontinuities between the ReadMe files.

## About the project
This project consists of a scanner and a parser. When ran, each scanner input file is first read by the scanner and the JSON tokens are extracted from the input.
Each token is then outputted into the scanner output files, which can be found in the "ParserInputs" directory. See the example files to see the tokens' output format.
Once the Scanner has been run, the parser can be ran on the outputted tokens from the scanner. The Parser walks through the files in the "ParserInputs" folder for the token stream,
catching semtanic errors and outputting an abstract syntax tree if no errors were found.
Examples of errors can be found in the first few parser output files.

## More Information on the project can be found in the other ReadMe Files