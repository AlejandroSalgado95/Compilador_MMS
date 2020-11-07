# SPRINT 4

## Description
This release performs: 
* The lexical and syntactical analysis of an input text, and determines whether the given text is valid within the rules of the “MMS” language
* The semantical analysis and storage of the functions within a given input text, as well as its local and global variables
* Semantical type checks between the operands of an expression, and the expression itself depending on the requiring statement
* The quadruples generation for several statements, including: expressions (aritmetic,relational,logical), and non-linear statements (if-else, for, while)
* Virtual addresses managing (storing, retrieving and deleting) and calculation of the memory size needed for the functions

## Installation 
1.Install python3: brew install python3

2.Install python3 package manager: python3 -m pip install --upgrade virtualenv

3.Install ply: pip3 install ply

4.Run parser: python3 parser.py [file name]
 

## About

### Author
* A00513221, Alejandro Alfredo Salgado Gaspar

## Notes
### This release includes:
* Handwritten evidence of the lexical and syntactic rules. These are found at the “Documentacion” folder
* Source code for the lexer and parser, written on python and runnable through the console. These are found at the “Codigo” folder
* Source code for the semantic cube
* Source code for the functions directory and the variables table every function includes
* Source code for the quadruple generation of linear and non linear statements
* Source code for the virtual memory managing and functions needed memory calculation

### Pending:
* Everything related to the special functions ARC and LINE is pending (tokenization, rules, code,etc.)
* So far there is no unary operator ‘-‘, only its binary version is available (subtraction operation)
* No semantics checking has been added for the return statement of a function

### Overdue:
* Source code for the virtual machine 

### Doubts:
* Should the assignation precedence and association, which is right associative, also be written in code like the other operators?
