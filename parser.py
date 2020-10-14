#A00513221
#Alejandro A. Salgado G.

import ply.yacc as yacc
from lexer import tokens
import sys

from CuboSemantico import CS


precedence = (
    ('left', 'and', 'or'),
    ('left', '>', '<', 'equals', 'not_equals'),
    ('left', 'minus', '+'),
    ('left', '*', '/')
)

def p_programa(p):
    '''
     PROGRAMA : program id ';' PROGRAMA_OPTS PRINCIPAL 
               | program id ';' PRINCIPAL 
    '''
    print("ACCEPTED")


def p_programa_opts(p):
    '''
    PROGRAMA_OPTS :  DEC_V FUNCS
                    | DEC_V 
                    | FUNCS
    '''


def p_principal(p):
    '''
    PRINCIPAL : main '(' ')' BLOQUE
    '''

def p_dec_v(p):
    '''
    DEC_V : DEC_V var  TIPO_SIMPLE ':' LISTA_VAR ';' 
            | var TIPO_SIMPLE ':' LISTA_VAR ';'
    '''




#GENERABA CONFLICTOS Y NO TERMINABA EL PARSEO (FAILED)
#def p_dec_v(p):
    '''
    DEC_V : var DEC_V_LOOP
    '''
#GENERABA CONFLICTOS Y NO TERMINABA EL PARSEO (FAILED)
#def p_dec_v_loop(p):
    '''
    DEC_V_LOOP : DEC_V_LOOP TIPO_SIMPLE ':' LISTA_VAR ';' 
                | TIPO_SIMPLE ':' LISTA_VAR ';'
    '''




def p_lista_var(p):
    '''
    LISTA_VAR : LISTA_VAR ',' VARIABLE_FIX
               | VARIABLE_FIX
    '''

def p_tipo_simple(p):
    '''
    TIPO_SIMPLE : int 
                 | float 
                 | char
    '''


def p_funcs(p):
    '''
    FUNCS :  FUNCS FUNC_TYPES module id '(' ')' BLOQUE
           | FUNCS FUNC_TYPES module id '(' PARAMS ')' BLOQUE
           | FUNCS FUNC_TYPES module id '(' PARAMS ')' DEC_V BLOQUE 
           | FUNCS FUNC_TYPES module id '(' ')' DEC_V BLOQUE
           | FUNC_TYPES module id '(' ')' BLOQUE
           | FUNC_TYPES module id '(' PARAMS ')' BLOQUE
           | FUNC_TYPES module id '(' PARAMS ')' DEC_V BLOQUE
           | FUNC_TYPES module id '(' ')' DEC_V BLOQUE

    '''

def p_func_types(p):
    '''
    FUNC_TYPES : TIPO_SIMPLE 
                 | void
    '''


def p_params(p):
    '''
    PARAMS : PARAMS ',' TIPO_SIMPLE id 
            | TIPO_SIMPLE id
    '''

def p_variable_fix(p):
    '''
    VARIABLE_FIX : id '[' cte_i ']' 
                  | id
    '''

def p_variable(p):
    '''
    VARIABLE : id '[' EXPRESION ']' 
              | id
    '''

def p_bloque(p):
    '''
    BLOQUE : '{' LOOP_ESTATUTO return EXPRESION ';' '}' 
              | '{' LOOP_ESTATUTO '}' 
              | '{' return EXPRESION ';' '}' 
              | '{' '}'
    '''

def p_loop_estatuto(p):
    '''
    LOOP_ESTATUTO : LOOP_ESTATUTO ESTATUTO 
                    | ESTATUTO
    '''

def p_expresion(p):
    '''
    EXPRESION :  EXPRESION and EXP_R
                | EXPRESION or EXP_R
                | EXP_R
    '''

def p_exp_r(p):
    '''
    EXP_R :  EXP_A '>' EXP_A 
            | EXP_A '<' EXP_A 
            | EXP_A equals EXP_A  
            | EXP_A not_equals EXP_A 
            | EXP_A
    '''

def p_exp_a(p):
    '''
    EXP_A :  EXP_A '+' TERMINO 
            | EXP_A minus TERMINO 
            | TERMINO
    '''

def p_termino(p):
    '''
    TERMINO : TERMINO '*' FACTOR 
             | TERMINO '/' FACTOR 
             | FACTOR
    '''

def p_estatuto(p):
    '''
    ESTATUTO : ASIGNACION ';' 
              | CONDICION 
              | WHILE 
              | FOR 
              | LLAMADA ';' 
              | LECTURA ';'  
              | ESCRITURA ';' 
              | LLAMADA_BI ';'
    '''

def p_factor(p):
    '''
    FACTOR : LLAMADA 
            | CTE  
            | VARIABLE 
            | '(' EXPRESION ')' 
    '''

def p_cte(p):
    '''
    CTE : cte_i 
         | cte_f 
         | cte_c
    '''

def p_llamada(p):
    '''
    LLAMADA : id '(' LLAMADA_OPTS ')' 
             | id '(' ')'
    '''

def p_llamada_opts(p):
    '''
    LLAMADA_OPTS : LLAMADA_OPTS ',' EXPRESION 
                 | EXPRESION 
    '''

def p_asignacion(p):
    '''
    ASIGNACION : VARIABLE '=' EXPRESION
    '''

def p_condicion(p):
    '''
    CONDICION : if '(' EXPRESION ')' then BLOQUE 
               | if '(' EXPRESION ')' then BLOQUE else BLOQUE
    '''

def p_while(p):
    '''
    WHILE : while '(' EXPRESION ')' do BLOQUE
    '''

def p_for(p):
    '''
    FOR : for ASIGNACION to EXPRESION do BLOQUE
    '''

def p_lectura(p):
    '''
    LECTURA : read '(' LECTURA_OPTS ')'
    '''

def p_lectura_opts(p):
    '''
    LECTURA_OPTS : LECTURA_OPTS ',' id 
                  | id
    '''

def p_escritura(p):
    '''
    ESCRITURA : write '(' ESCRITURA_OPTS ')'
    '''

def p_escritura_opts(p):
    '''
    ESCRITURA_OPTS :   ESCRITURA_OPTS ',' cte_s
                       | ESCRITURA_OPTS ',' EXPRESION 
                       | cte_s 
                       | EXPRESION
    '''

def p_llamada_bi(p):
    '''
    LLAMADA_BI :   POINT 
                 | CIRCLE
                 | PENUP
                 | PENDOWN 
                 | COLOR 
                 | SIZE 
                 | CLEAR
    '''

def p_clear(p):
    '''
    CLEAR : clear '(' ')'
    '''

def p_point(p):
    '''
    POINT : point '(' EXPRESION ',' EXPRESION ')'
    '''

def p_circle(p):
    '''
    CIRCLE : circle '(' EXPRESION ')' 
    '''

def p_penup(p):
    '''
    PENUP : penup '(' ')'
    '''

def p_pendown(p):
    '''
    PENDOWN : pendown '(' ')'
    '''

def p_color(p):
    '''
    COLOR : color '(' cte_s ')' 
    '''

def p_size(p):
    '''
    SIZE : size '(' EXPRESION ')' 
    '''


def p_error(p):
    if p:
        print("Syntax error at '%s' " % p.value, " on line '%s'" % p.lineno)
    else:
        print("Syntax error at EOF")



#Parse a given file

parser = yacc.yacc()

filename = sys.argv[1]

f = open(filename,'r')
data = f.read()
f.close()

parser.parse(data, tracking=True)
