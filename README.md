# SPRINT 7

## Description
This release performs: 
* The lexical and syntactical analysis of an input text, and determines whether the given text is valid within the rules of the “MMS” language
* The semantical analysis and storage of the functions within a given input text, as well as its local, global variables, needed memory adressses, among other useful data
* All the neccesary semantical checks found so far, such as: function type and return type must be the same, void functions must not have return staments while non void functions should do, a given value must be of the same type as the variable its trying to get saved in, etc.
* Error handlings for most of the semantical checks performed
* The quadruples generation for all posible actions
* Temporal and global Memory managing based on function calls memory stacking on run time
* The virtual machine that interprets all the quadruple actions in runtime
* Displaying on console of the runtime execution of an accepted input text
* Unidimensional Arrays as data structures where you can create, asign or modify any part of it
* Graphical displays via the built-in library Turtle

## Installation 
1.Install python3: brew install python3

2.Install python3 package manager: python3 -m pip install --upgrade virtualenv

3.Install ply: pip3 install ply

4.Run parser: python3 memyselfcompiler.py [file name]
 

## About

### Author
* A00513221, Alejandro Alfredo Salgado Gaspar

## Notes
### This release includes:
* Handwritten evidence of the lexical and syntactic rules. These are found at the “Documentacion” folder
* Source code for the lexer and parser, written on python and runnable through the console. These are found at the “Codigo” folder
* Source code (semanticcube.py) for the semantic cube
* Source code (functiondirectory.py)for the functions directory and the variables table every function includes
* Source code (quadruples.py) for the quadruple generation of all possible actions
* Source code (virtualAdresses.py) for the virtual memory managing and functions needed memory calculation
* Source code (virtualmachine.py) for the virtual machine that interprets the quadruples actions
* Source code (tools.py) for a file that contains a repertory of functions used many times, used for the author in order to avoid rewriting his own code many times 
* Source code (operand.py) used for the operands included within each generated quadruple
* Source code (EmtpyTempMemoryInstance.py) used for instanciating new temporal memory
* Documentation of the compiler design process and its design itself
* User manual which documents basic usage of the designed language 
* Two firmed documents to agree everything that's is being included is original and created by its author (A00513221)
* one quick reference video

### Pending:
* So far there is no unary operator ‘-‘, only its binary version is available (subtraction operation)

### Bugs:
* Unary operator - is not available, in order to specify a negative number you must do it like this: i = 0 - 5 (to provide -5 as value) instead of i = -5
* Due to ambiguity issues, a "/" must be added in order to call functions as statements (void functions that is) rather than expressions (non void functions that is), for example: /example(5)

### Overdue:
* Nothing (Up-to-date) 

### Doubts:
* Should the assignation precedence and association, which is right associative, also be written in code like the other operators?
