#A00513221
#Alejandro A. Salgado G.

import ply.yacc as yacc
from lexer import tokens
import sys

from FunctionDirectory import FuncDirec
from Quadruples import Quadruples
from SemanticCube import SC
from Operand import Operand
from VirtualAddresses import VirtualAdresses
from Tools import determineTypeAddressTable


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
gotoList = []
paramsCallCounter = 0
funcCall = ""

#Variables globales
dirAddresses = {
"globalInt" : VirtualAdresses(15000, 15099),
"globalFloat" : VirtualAdresses(15100, 15199),
"globalChar" : VirtualAdresses(15200, 15299),
#Variables locales
"localInt" : VirtualAdresses(15300, 15399),
"localFloat" : VirtualAdresses(15400, 15499),
"localChar" : VirtualAdresses(15500, 15599),
#Resultados temporales
"tempInt" : VirtualAdresses(15600, 15699),
"tempFloat" : VirtualAdresses(15700, 15799),
"tempChar" : VirtualAdresses(15800, 15899),
"tempBool" : VirtualAdresses(15900, 15998),
#Constantes temporales
"constInt" : VirtualAdresses(16000, 16099),
"constFloat" : VirtualAdresses(16100, 16199),
"constChar" : VirtualAdresses(16200, 16299),
"constString" : VirtualAdresses(16300, 16399)
}




precedence = (
    ('left', 'and', 'or'),
    ('left', '>', '<', 'equals', 'not_equals'),
    ('left', 'minus', '+'),
    ('left', '*', '/')
)


############################################SYNTACTIC RULES########################################
def p_programa(p):
    '''
     PROGRAMA : SEM_ADD_GOTO_MAIN program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PROGRAMA_OPTS PRINCIPAL 
               | SEM_ADD_GOTO_MAIN program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PRINCIPAL 
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
    PRINCIPAL :   SEM_FILL_GOTO_ANYKIND SEM_MAIN_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
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
    FUNCS :  FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE   SEM_ENDFUNC
           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC 
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC 
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC 
           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE  SEM_ENDFUNC 

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
  global funcDirec
  global varType
  global dirAddresses

  scope = "local"
  varName = p[1]
  addressTableKey = determineTypeAddressTable(scope,varType,None,False)
  vAddress = dirAddresses[addressTableKey].getAnAddress()
  funcDirec.addLocalVariableToFunc(funcName, varName, varType , True, vAddress)

def p_variable_fix(p):
    '''
    VARIABLE_FIX : id '[' cte_i ']' 
                  | id
    '''
    global varName
    global varType
    global funcDirec
    global dirAddresses
    global funcName

    scope = "local"

    if (funcName == "global"):
      scope = "global"

    varName = p[1]
    addressTableKey = determineTypeAddressTable(scope,varType,None,False)
    vAddress = dirAddresses[addressTableKey].getAnAddress()
    result = funcDirec.addLocalVariableToFunc(funcName, varName, varType, False, vAddress)

    if isinstance(result,str):
      errorQueue.append("Error: " + result)
      print("Error: ", result)




def p_variable(p):
    '''
    VARIABLE : id '[' EXPRESION ']' 
              | id
    '''
    global varName
    global funcDirec
    global operandsList
    global funcDirec
    global dirAddresses
    global funcName


    varName = p[1]
    retrievedVar = funcDirec.getVariableInFunc(funcName, varName)
    if isinstance(retrievedVar, str):
      errorQueue.append("Error: " + retrievedVar)
      print("Error: ", retrievedVar)
    else:
      operandsList.append( Operand(varName, None, retrievedVar["varType"], retrievedVar["vAddress"]) )
      

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
    global dirAddresses
    global funcName


    cteValue = p[1]
    if isinstance(p[1],int):
      cteType = "int"
    elif isinstance(p[1],float):
      cteType = "float"
    elif isinstance(p[1],str):
      cteType = "char"

    addressTableKey = determineTypeAddressTable(None,cteType,cteValue,None)
    vAddress = dirAddresses[addressTableKey].getAnAddress()

    consOperand = Operand(None, cteValue, cteType, vAddress)
    operandsList.append( consOperand )
    



def p_llamada(p):
    '''
    LLAMADA :   SEM_VERIFY_FUNC_CALL '(' LLAMADA_OPTS SEM_RESET_PARAM_COUNT ')' SEM_ADD_GOSUB
             |  SEM_VERIFY_FUNC_CALL '(' ')' SEM_ADD_GOSUB
    '''

def p_llamada_opts(p):
    '''
    LLAMADA_OPTS : LLAMADA_OPTS ',' EXPRESION SEM_VERIFY_PARAM
                 | EXPRESION SEM_VERIFY_PARAM
    '''

def p_asignacion(p):
    '''
    ASIGNACION : VARIABLE '=' SEM_ADD_EQUALS EXPRESION SEM_PENDING_ASSIGNATION_OP
    '''

def p_condicion(p):
    '''
    CONDICION : if '(' EXPRESION ')' SEM_ADD_GOTOF then BLOQUE SEM_FILL_GOTO_ANYKIND 
               | if '(' EXPRESION ')' SEM_ADD_GOTOF then BLOQUE else SEM_ADD_GOTO_SIMPLE BLOQUE SEM_FILL_GOTO_ANYKIND
    '''

def p_while(p):
    '''
    WHILE : while  SEM_ADD_COND_INDEX '(' EXPRESION ')' SEM_ADD_GOTOF do BLOQUE SEM_ADD_GOTO_SIMPLE SEM_FILL_GOTO_COND_INDEX
    '''

def p_for(p):
    '''
    FOR : for ASIGNACION to SEM_ADD_COND_INDEX EXPRESION SEM_ADD_GOTOV do BLOQUE SEM_ADD_GOTO_SIMPLE SEM_FILL_GOTO_COND_INDEX
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

#Crea un cuadruplo gotof que recibe de argumento un operando de la pila, y 
#guarda el index del cuadruplo gotof creado para rellenarlo despues con 
#el index del cuadruplo al cual debe saltar
def p_sem_add_gotof(p):
  '''
  SEM_ADD_GOTOF : 
  '''
  global gotoList
  global operandsList
  global quadruples

  operand = operandsList.pop()
  result = quadruples.addGoToCuadruple(operand,"gotoF")
  if isinstance(result,str):
    errorQueue.append("Error: " + result)
    print("Error: ", result)
  else:
    gotoCuadrupleIndex = len(quadruples.quadruples) - 1
    gotoList.append(gotoCuadrupleIndex)

#Rellena ya sea un cuadruplo goto o un cuadruplo gotof con el index del 
#cuadruplo siguiente
def p_sem_fill_goto_anykind(p):
  '''
  SEM_FILL_GOTO_ANYKIND : 
  '''
  global gotoList
  global quadruples

  gotoIndex = gotoList.pop()
  directionIndex = len(quadruples.quadruples) +1 
  quadruples.fillGoToCuadruple(gotoIndex,directionIndex)

#Rellena el cuadruplo gotof anteriormente guardado con destino a un index
#mayor al index del cuadruplo goto que se va a insertar,
#y luego se inserta el cuadruplo goto, guardando en la pila de saltos
#el index del goto incompleto al cual le falta su direccion de ida
def p_sem_add_goto_simple(p):
  '''
  SEM_ADD_GOTO_SIMPLE : 
  '''
  global gotoList
  global quadruples

  gotoIndex = gotoList.pop()
  directionIndex = len(quadruples.quadruples) + 2
  quadruples.fillGoToCuadruple(gotoIndex,directionIndex)

  quadruples.addGoToCuadruple(None,"goto")
  gotoCuadrupleIndex = len(quadruples.quadruples) - 1
  gotoList.append(gotoCuadrupleIndex)



#Añade index del cuadruplo donde ira la condicion del loop
def p_sem_add_cond_index(p):
  '''
  SEM_ADD_COND_INDEX : 
  '''
  global gotoList

  condIndex = len(quadruples.quadruples) + 1
  gotoList.append(condIndex)


#Rellena el goto pendiente con el index donde comienzan los cuadruplos
# de la condicion para un loop que se repite
def p_sem_fill_goto_cond_index(p):
  '''
  SEM_FILL_GOTO_COND_INDEX : 
  '''
  global gotoList
  global quadruples
  goToIndex = gotoList.pop()
  condIndex  = gotoList.pop()
  quadruples.fillGoToCuadruple(goToIndex,condIndex)


def p_sem_add_gotov(p):
  '''
  SEM_ADD_GOTOV : 
  '''
  global gotoList
  global quadruples
  operand = operandsList.pop()
  result = quadruples.addGoToCuadruple(operand,"gotoV")
  if isinstance(result,str):
    errorQueue.append("Error: " + result)
    print("Error: ", result)
  else:
    gotoCuadrupleIndex = len(quadruples.quadruples) - 1
    gotoList.append(gotoCuadrupleIndex)



def p_sem_add_goto_main(p):
  '''
  SEM_ADD_GOTO_MAIN : 
  '''
  global gotoList
  global quadruples
  quadruples.addGoToCuadruple(None,"goto")
  gotoCuadrupleIndex = len(quadruples.quadruples) - 1
  gotoList.append(gotoCuadrupleIndex)


def p_sem_endfunc(p):
  '''
  SEM_ENDFUNC : 
  '''
  global quadruples
  global dirAddresses
  quadruples.addEndFuncQuadrupple()
  for dirTableName in dirAddresses:
    if not "global" in dirTableName:
      dirAddresses[dirTableName].deleteAllContent()



def p_sem_verify_func_call(p):
    '''
    SEM_VERIFY_FUNC_CALL : id 
    '''
    global funcDirec
    global funcCall
    global quadruples

    result = funcDirec.verifyFuncCall(p[1])
    if isinstance(result, str):
        errorQueue.append("Error: " + result)
        print("Error: ", result)
    else:
      funcCall = p[1]
      quadruples.addEraFuncQuadruple(funcCall)


def p_sem_verify_param(p):
    '''
    SEM_VERIFY_PARAM :
    '''  
    global funcDirec
    global funcCall
    global quadruples
    global operandsList
    global paramsCallCounter
    global dirAddresses
    
    funcCallFirm = funcDirec.getFunctionFirm(funcCall)

    if isinstance(funcCallFirm, str):
        errorQueue.append("Error: " + result)
        print("Error: ", result)
    else:
      param = operandsList.pop()
      if param.type != funcCallFirm[paramsCallCounter]:
        errorMessage =  "Type missmatch. Function " + funcCall + " requires " + funcCallFirm[paramsCallCounter] + " for argument " + str(paramsCallCounter) + ". Type provided was " + param.type
        errorQueue.append("Error: "  + errorMessage)
        print("Error: ", errorMessage)
      else:
        quadruples.addParamFuncQuadruple( param, paramsCallCounter)
        paramsCallCounter += 1

def p_sem_reset_param_count(p):
    '''
    SEM_RESET_PARAM_COUNT :
    '''  
    global paramsCallCounter
    paramsCallCounter = 0

  
def p_sem_add_gosub(p):
    '''
    SEM_ADD_GOSUB :
    '''  
    global funcCall
    global quadruples
    quadruples.addGosubFuncQuadruple(funcCall)







def p_sem_pending_expa_op(p):
  '''
  SEM_PENDING_EXPA_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruples
  global dirAddresses
  global funcName
  global funcDirec

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if topOp == '+' or topOp == '-':
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand,dirAddresses)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)
      funcDirec.addTempVarCountInFunc(funcName,resultOperand.type)


def p_sem_pending_termino_op(p):
  '''
  SEM_PENDING_TERMINO_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruples
  global dirAddresses
  global funcName
  global funcDirec

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if topOp == '*' or topOp == '/':
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand,dirAddresses)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)
      funcDirec.addTempVarCountInFunc(funcName,resultOperand.type)



def p_sem_pending_assignation_op(p):
  '''
  SEM_PENDING_ASSIGNATION_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruples

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
  global quadruples
  global errorQueue
  global dirAddresses
  global funcName
  global funcDirec

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if (topOp == ">") or (topOp == "<") or (topOp == "==") or (topOp == "!="):
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand,dirAddresses )
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)
      funcDirec.addTempVarCountInFunc(funcName,resultOperand.type)



def p_sem_pending_logic_op(p):
  '''
  SEM_PENDING_LOGIC_OP : 
  '''
  global operatorsList
  global operandsList
  global quadruples
  global errorQueue
  global dirAddresses
  global funcName
  global funcDirec

  topOp = ""

  if len(operatorsList) > 0 :
    topOp = operatorsList[-1]
  if (topOp == "&&") or (topOp == "||"):
    topOp = operatorsList.pop()
    rOperand = operandsList.pop()
    lOperand = operandsList.pop()
    resultOperand = quadruples.addExpressionCuadruple(topOp,lOperand,rOperand,dirAddresses)
    if isinstance(resultOperand,str):
      errorQueue.append("Error: " + resultOperand)
      print("Error: ", resultOperand)
    else: 
      operandsList.append(resultOperand)
      funcDirec.addTempVarCountInFunc(funcName,resultOperand.type)





######################################################PARSER EXECUTION##############################

#Parse a given file

parser = yacc.yacc()

filename = sys.argv[1]

f = open(filename,'r')
data = f.read()
f.close()

parser.parse(data, tracking=True)
