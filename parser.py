#A00513221
#Alejandro A. Salgado G.

import ply.yacc as yacc
from lexer import tokens
import sys

from FunctionDirectory import FuncDirec
from Quadruples import Quadruples
from SemanticCube import SC
from Operand import Operand


#python variables
funcDirec = FuncDirec()
funcName = ""
funcType = ""
varType = ""
varName = ""
cteValue = ""
cteType = ""
operandsList = []
operatorsList = []
quadruples = Quadruples()
errorQueue = []




precedence = (
    ('left', 'and', 'or'),
    ('left', '>', '<', 'equals', 'not_equals'),
    ('left', 'minus', '+'),
    ('left', '*', '/')
)


############################################SYNTACTIC RULES########################################
def p_programa(p):
    '''
     PROGRAMA : program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PROGRAMA_OPTS PRINCIPAL 
               | program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PRINCIPAL 
    '''
    global operandsList
    global errorQueue
    print("ACCEPTED")
    funcDirec.printContents(True)
    quadruples.printContents()
    print("amount of cuadruples: " + str( len(quadruples.quadruples) ) )
    for operand in operandsList:
        print("Name: " + str(operand.name), "Value: " + str(operand.value), "Type: " + str(operand.type))
    for operator in operatorsList:
        print ("operator: " + operator)
    for error in errorQueue:
        print(error)



def p_programa_opts(p):
    '''
    PROGRAMA_OPTS :  DEC_V FUNCS
                    | DEC_V
                    | FUNCS
    '''


def p_principal(p):
    '''
    PRINCIPAL : SEM_MAIN_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
    '''

def p_dec_v(p):
    '''
    DEC_V : DEC_V var  TIPO_SIMPLE ':' LISTA_VAR ';' 
            | var TIPO_SIMPLE ':' LISTA_VAR ';'
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
    global varType 

    varType = p[1]


def p_funcs(p):
    '''
    FUNCS :  FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE 
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE

    '''

def p_func_types(p):
    '''
    FUNC_TYPES :  char
                 | float 
                 | int
                 | void
    '''
    global funcType

    funcType = p[1]


def p_params(p):
    '''
    PARAMS : PARAMS ',' TIPO_SIMPLE PARAM_NAME
            | TIPO_SIMPLE PARAM_NAME
    '''
    
def p_param_name(p):
  '''
  PARAM_NAME : id
  '''
  global varName

  varName = p[1]
  funcDirec.addLocalVariableToFunc(funcName, varName, varType, True)

def p_variable_fix(p):
    '''
    VARIABLE_FIX : id '[' cte_i ']' 
                  | id
    '''
    global varName
    global varType
    global funcDirec

    varName = p[1]
    funcDirec.addLocalVariableToFunc(funcName, varName, varType, False)



def p_variable(p):
    '''
    VARIABLE : id '[' EXPRESION ']' 
              | id
    '''
    global varName
    global funcDirec
    global operandsList

    varName = p[1]
    retrievedVar = funcDirec.getVariableInFunc(funcName, varName)
    if isinstance(retrievedVar, str):
      errorQueue.append("Error: " + retrievedVar)
      print("Error: ", retrievedVar)
    else:
      operandsList.append( Operand(varName, None, retrievedVar["varType"]) )
      

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
    EXPRESION :  EXPRESION SEM_PENDING_LOGIC_OP  and  SEM_ADD_AND  EXP_R  SEM_PENDING_LOGIC_OP
                | EXPRESION SEM_PENDING_LOGIC_OP  or  SEM_ADD_OR   EXP_R  SEM_PENDING_LOGIC_OP
                | EXP_R
    '''

def p_exp_r(p):
    '''
    EXP_R :  EXP_A '>' SEM_ADD_GREATER_THAN   EXP_A   SEM_PENDING_REL_OP
            | EXP_A '<' SEM_ADD_LESS_THAN   EXP_A   SEM_PENDING_REL_OP
            | EXP_A equals SEM_ADD_EQUALS_TO   EXP_A    SEM_PENDING_REL_OP
            | EXP_A not_equals SEM_ADD_NOT_EQUALS_TO   EXP_A   SEM_PENDING_REL_OP
            | EXP_A
    '''

def p_exp_a(p):
    '''
    EXP_A :  EXP_A SEM_PENDING_EXPA_OP '+' SEM_ADD_PLUS TERMINO SEM_PENDING_EXPA_OP
            | EXP_A SEM_PENDING_EXPA_OP minus SEM_ADD_MINUS TERMINO SEM_PENDING_EXPA_OP
            | TERMINO
    '''

def p_termino(p):
    '''
    TERMINO : TERMINO SEM_PENDING_TERMINO_OP '*' SEM_ADD_TIMES  FACTOR  SEM_PENDING_TERMINO_OP
             | TERMINO SEM_PENDING_TERMINO_OP '/' SEM_ADD_DIVISION  FACTOR  SEM_PENDING_TERMINO_OP
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
            | '(' SEM_ADD_FONDO_FALSO EXPRESION ')' SEM_REMOVE_FONDO_FALSO
    '''

def p_cte(p):
    '''
    CTE : cte_i 
         | cte_f 
         | cte_c
    '''
    global cteValue
    global cteType
    global operandsList

    cteValue = p[1]
    if isinstance(p[1],int):
      cteType = "int"
    elif isinstance(p[1],float):
      cteType = "float"
    elif isinstance(p[1],str):
      cteType = "char"

    consOperand = Operand(None, cteValue, cteType)
    operandsList.append( consOperand )
    





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
    ASIGNACION : VARIABLE '=' SEM_ADD_EQUALS EXPRESION SEM_PENDING_ASSIGNATION_OP
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


################################################INBETWEEN RULES####################################





###########################################SEMANTIC RULES#########################################

def p_sem_global_name(p):
  '''
    SEM_GLOBAL_NAME : id
  '''
  global funcName
  global funcType
  funcName = "global"
  funcType = "void"

def p_sem_main_name(p):
  '''
    SEM_MAIN_NAME : main
  '''
  global funcName
  global funcType
  funcName = p[1]
  funcType = "void"



def p_sem_func_name(p):
  '''
    SEM_FUNC_NAME : id
  '''
  global funcName
  funcName = p[1]


def p_sem_add_func(p):
  '''
  SEM_ADD_FUNC : 
  '''
  funcDirec.addFunc(funcName, funcType)


def p_sem_add_global_variables(p):
  '''
  SEM_ADD_GLOBAL_VARIABLES : 
  '''
  funcDirec.addGlobalVariablesToFunc(funcName)


def p_sem_add_plus(p):
  '''
  SEM_ADD_PLUS : 
  '''
  global operatorsList
  operatorsList.append("+")


def p_sem_add_minus(p):
  '''
  SEM_ADD_MINUS : 
  '''
  global operatorsList
  operatorsList.append("-")
  print

def p_sem_add_times(p):
  '''
  SEM_ADD_TIMES : 
  '''
  global operatorsList
  operatorsList.append("*")

def p_sem_add_division(p):
  '''
  SEM_ADD_DIVISION : 
  '''
  global operatorsList
  operatorsList.append("/")


def p_sem_add_equals(p):
  '''
  SEM_ADD_EQUALS : 
  '''
  global operatorsList
  operatorsList.append("=")


def p_sem_add_fondo_falso(p):
  '''
  SEM_ADD_FONDO_FALSO : 
  '''
  global operatorsList
  operatorsList.append("(")


def p_sem_remove_fondo_falso(p):
  '''
  SEM_REMOVE_FONDO_FALSO : 
  '''
  global operatorsList
  operatorsList.pop()


def p_sem_add_greater_than(p):
  '''
  SEM_ADD_GREATER_THAN : 
  '''
  global operatorsList
  operatorsList.append('>')


def p_sem_add_less_than(p):
  '''
  SEM_ADD_LESS_THAN : 
  '''
  global operatorsList
  operatorsList.append('<')


def p_sem_add_equals_to(p):
  '''
  SEM_ADD_EQUALS_TO : 
  '''
  global operatorsList
  operatorsList.append('==')


def p_sem_add_not_equals_to(p):
  '''
  SEM_ADD_NOT_EQUALS_TO : 
  '''
  global operatorsList
  operatorsList.append('!=')


def p_sem_add_and(p):
  '''
  SEM_ADD_AND : 
  '''
  global operatorsList
  operatorsList.append('&&')


def p_sem_add_or(p):
  '''
  SEM_ADD_OR : 
  '''
  global operatorsList
  operatorsList.append('||')


def p_sem_pending_expa_op(p):
  '''
  SEM_PENDING_EXPA_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruplesList

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if topOp == '+' or topOp == '-':
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)


def p_sem_pending_termino_op(p):
  '''
  SEM_PENDING_TERMINO_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruplesList

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if topOp == '*' or topOp == '/':
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)


def p_sem_pending_assignation_op(p):
  '''
  SEM_PENDING_ASSIGNATION_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruplesList

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if topOp == "=":
    topOp = operatorsList.pop()
    operand = operandsList.pop()
    resultOperand = operandsList.pop()
    result = quadruples.addAssignationCuadruple(operand,resultOperand)
    if isinstance(result,str):
      errorQueue.append("Error: " + result)
      print("Error: ", result)


def p_sem_pending_rel_op(p):
  '''
  SEM_PENDING_REL_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruplesList
  global errorQueue

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if (topOp == ">") or (topOp == "<") or (topOp == "==") or (topOp == "!="):
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)


def p_sem_pending_logic_op(p):
  '''
  SEM_PENDING_LOGIC_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruplesList
  global errorQueue

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if (topOp == "&&") or (topOp == "||"):
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)




######################################################PARSER EXECUTION##############################

#Parse a given file

parser = yacc.yacc()

filename = sys.argv[1]

f = open(filename,'r')
data = f.read()
f.close()

parser.parse(data, tracking=True)
