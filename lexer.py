#A00513221
#Alejandro A. Salgado G.

import ply.lex as lex

import sys


#Tokens, literals, and reserved words list

reserved = {

'program' : 'program',
'main' : 'main',
'module' : 'module',
'void' : 'void',
'null' : 'null',
'var' : 'var',
'int' :'int',
'float' : 'float',
'char' : 'char',
'if' : 'if',
'then' : 'then',
'else' : 'else',
'return': 'return',
'do' :'do',
'while' : 'while',
'for' : 'for',
'to' : 'to',
'read' :'read',
'write' : 'write',
'clear' : 'clear',
'point' : 'point',
'circle' : 'circle',
'penup' : 'penup',
'pendown' : 'pendown',
'color' : 'color',
'size' : 'size',
'global' : 'global',
"line" : "line",
"arc" : "arc"

}

tokens = [
    'cte_s',
    'cte_i',
    'cte_f',
    'cte_c',
    'id',
    'equals',
    'not_equals',
    'and',
    'or',
    'minus'
] + list(reserved.values())


literals = [ '+','*','/','{','}','(',')',';',',',':','>','<','=','[',']' ] #single-character literals




#Token rules
t_minus = r'\-'
t_equals = r'\=\='
t_not_equals = r'\!\='
t_and = r'\&\&'
t_or = r'\|\|'

def t_cte_f(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_cte_i(t):
    r'\d+'
    t.value = int(t.value)
    return t


#Debe ir primero la evaluacion de char antes que la de string, o sino un char siempre lo interpretara como string
def t_cte_c(t):
    r'(\‘[a-zA-z_0-9]\’) | (\'[a-zA-z_0-9]\')'
    t.value = str(t.value) #its being casted to string instead of char, is this alright?
    return t

def t_cte_s(t):
    r' (\“[a-zA-z_0-9\s\,\=]*\”) | (\"[a-zA-z_0-9\s\,\=]*\")'
    t.value = str(t.value)
    return t

def t_id(t):
    r'[a-zA-Z0-9]+'
    t.type = reserved.get(t.value, 'id')
    return t




#Lex operations

t_ignore = " \t" 

def t_error(t):
    print("Illegal characters:", t.value[0], ", on line: ", t.lexer.lineno)
    t.lexer.skip(1)


def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)




#Lexer construction
lexer = lex.lex()


# # Give the lexer some input
#lexer.input()

# # Tokenize
#while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)
