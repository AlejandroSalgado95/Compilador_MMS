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
from Tools import deleteAddressesOfFunc


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
pendingReturnOperand = ""
hasReturn = False
mustBeVoidCall = False

#Variables globales
dirAddresses = {
"globalInt" : VirtualAdresses(15000, 15099,"globalInt"),
"globalFloat" : VirtualAdresses(15100, 15199,"globalFloat"),
"globalChar" : VirtualAdresses(15200, 15299,"globalChar"),
#Variables locales
"localInt" : VirtualAdresses(15300, 15399,"localInt"),
"localFloat" : VirtualAdresses(15400, 15499,"localFloat"),
"localChar" : VirtualAdresses(15500, 15599,"localChar"),
#Resultados temporales
"tempInt" : VirtualAdresses(15600, 15699,"tempInt"),
"tempFloat" : VirtualAdresses(15700, 15799,"tempFloat"),
"tempChar" : VirtualAdresses(15800, 15899,"tempChar"),
"tempBool" : VirtualAdresses(15900, 15998,"tempBool"),
#Constantes temporales
"constInt" : VirtualAdresses(16000, 16099,"constInt"),
"constFloat" : VirtualAdresses(16100, 16199,"constFloat"),
"constChar" : VirtualAdresses(16200, 16299,"constChar"),
"constString" : VirtualAdresses(16300, 16399,"constString")
}




precedence = (
    ('left', 'and', 'or'),
    ('left', '>', '<', 'equals', 'not_equals'),
    ('left', 'minus', '+'),
    ('left', '*', '/')
)


############################################SYNTACTIC RULES########################################

# Al finalizar la ejecucion del programa se hacen los prints necesarios para 
# debuggear los contenidos de diferentes estructuras de datos, como: los quadruplos, la pila de operandos, la informacion completa de cada funcion (sus contadores y su tabla de variables), etc
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
    PRINCIPAL :   SEM_FILL_MAIN_GOTO SEM_MAIN_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE
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
  funcDirec.addParamAddressOfFunc(funcName, vAddress)




#Se declaran variables locales o globales (NUNCA PARAMETROS NI OPERANDOS DENTRO EXPRESIONES) y se les asigna una direccion virtual, mas no se guarda nada en esa direccion virtual aun, pues las variables no tienen valor inicial
#1. Si la funcion activa es la funcion global, a las variables se les asignara direcciones en tablas de memoria global; de lo contrario, se les asignaran direcciones en tablas de memoria local
#3. La informacion relevante de la variable (nombre, tipo, direccion virtual asignada) es guardada en la tabla de variables de la funcion actual. Si la operacion es exitosa
#   el contador de variables apropiado dentro de la funcion aumentara, y la informacion de la variable habra quedado guardada en la tabla de variables 

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

    #es un arreglo
    if len(p) > 2:
      
      varName = p[1]
      arraySize = p[3]
      addressTableKey = determineTypeAddressTable(scope,varType,None,False)
      vAddress = dirAddresses[addressTableKey].getAnAdressForArray(arraySize)
      result = funcDirec.addLocalArrayToFunc(funcName, varName, varType, vAddress, arraySize)
     
      if isinstance(result,str):
        errorQueue.append("Error: " + result)
        print("Error: ", result)

     
    #es un id
    else:

      varName = p[1]
      addressTableKey = determineTypeAddressTable(scope,varType,None,False)
      vAddress = dirAddresses[addressTableKey].getAnAddress()
      result = funcDirec.addLocalVariableToFunc(funcName, varName, varType, False, vAddress)

      if isinstance(result,str):
        errorQueue.append("Error: " + result)
        print("Error: ", result)
    


#Verifica que una variable/identificador usada en una expresion sea valida semanticamente
#1. Se revisa que el id de la variable este declarada en la tabla de variables 
#   de la funcion activa (sea como variable local o global). Si la variable es valida
#   en ese sentido semantico, se recupera la informacion de la variable y se crea un operando con sus datos, y este operando
#   se agrega a la pila de operandos para que futuras expresiones trabajen con el (generando cuadruplos por ejemplo)
def p_variable(p):
    '''
    VARIABLE : SEM_ID_FOR_ARRAY '[' EXPRESION SEM_CHECK_ARRAY ']' 
              | id
    '''
    global varName
    global funcDirec
    global operandsList
    global funcDirec
    global dirAddresses
    global funcName

    #es una variable en una expresion, no un arreglo
    if len(p) < 3:
      varName = p[1]
      retrievedVar = funcDirec.getVariableInFunc(funcName, varName)
      if isinstance(retrievedVar, str):
        errorQueue.append("Error: " + retrievedVar)
        print("Error: ", retrievedVar)
      else:
        operandsList.append( Operand(varName, None, retrievedVar["varType"], retrievedVar["vAddress"]) )

def p_sem_id_for_array(p):
  '''
  SEM_ID_FOR_ARRAY : id
  '''
  global varName
  varName = p[1]


def p_sem_check_array(p):
  '''  
  SEM_CHECK_ARRAY : 
  '''
  global varName
  global funcDirec
  global operandsList
  global funcDirec
  global dirAddresses
  global funcName
  
  #checa si existe el arreglo
  retrievedArrayData = funcDirec.getVariableInFunc(funcName, varName)
  if isinstance(retrievedArrayData, str):
      errorQueue.append("Error: " + retrievedArrayData)
      print("Error: ", retrievedArrayData)
  else:
    arrayIndexExpression = operandsList.pop()
    actualAddress = retrievedArrayData["vAddress"] + arrayIndexExpression.value
    #checa que el index del arreglo sea tipo int
    if arrayIndexExpression.type != "int":
      errorQueue.append("Error: Failed operation. Int type index expected for array " + varName + ". " + arrayIndexExpression.type + "type was received instead.")
      print("Error: ", retrievedVar)
    #checa que el index tipo int del arreglo se encuentre en el rango de direcciones validas para el arreglo
    elif (actualAddress < retrievedArrayData["vAddress"]) or (actualAddress > retrievedArrayData["sLimit"]):  
      errorQueue.append("Error: Failed operation. Index " + arrayIndexExpression.value + " is out of bounds for array " + varname  )
      print("Error: ", retrievedVar)
    else:
      operandsList.append( Operand(varName, None, retrievedArrayData["varType"], actualAddress) )



#Un bloque puede venir con estatuto de return o no
#1. Si el bloque viene con return, debe verificarse que haya un operando guardado
#   en la lista de operandos cuyo tipo sea igual al valor de retorno de la funcion
#   en la que se encuentra el return
def p_bloque(p):
    '''
    BLOQUE : '{' LOOP_ESTATUTO return EXPRESION SEM_VERIFY_RETURN_FUNC ';' '}' 
              | '{' LOOP_ESTATUTO '}' 
              | '{' return EXPRESION SEM_VERIFY_RETURN_FUNC ';' '}' 
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
              |  '/' SEM_MUST_BE_VOID_CALL LLAMADA ';' 
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


#Para la constante leida, se crea un operando que guarde su informacion relevante, le asigna una memoria
# Y GUARDA SU VALOR EN MEMORIA (a diferencia de cuando se crea un operando para un id)
#1. En base a la informacion disponible, se revisa a que tabla de direcciones debe ir el operando
#2. Conocida la tabla de direcciones correcta, se solicita una direccion virtual a la tabla para que se le sea asignada al  operando
#3. Se crea el operando de la constante leida con toda su informacion
#4. Se guarda en la memoria asignada al operando la informacion relevante de este, PARTICULARMENTE SU VALOR
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
    dirAddresses[addressTableKey].saveAddressData(vAddress, cteValue, cteType)
    #print (str(vAddress) + " : " + str(dirAddresses[addressTableKey].getAddressData(vAddress)["value"]))
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
    LECTURA_OPTS : LECTURA_OPTS ',' VARIABLE SEM_ADD_READ
                  |  VARIABLE SEM_ADD_READ
    '''

def p_escritura(p):
    '''
    ESCRITURA : write '(' ESCRITURA_OPTS ')'
    '''

def p_escritura_opts(p):
    '''
    ESCRITURA_OPTS :   ESCRITURA_OPTS ',' SEM_ADD_PRINT_CTE_S
                       | ESCRITURA_OPTS ',' EXPRESION SEM_ADD_PRINT
                       | SEM_ADD_PRINT_CTE_S 
                       | EXPRESION SEM_ADD_PRINT
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
    CLEAR : clear '(' ')' DO_CLEAR
    '''

def p_point(p):
    '''
    POINT : point '(' EXPRESION ',' EXPRESION ')' DRAW_POINT
    '''

def p_circle(p):
    '''
    CIRCLE : circle '(' EXPRESION ')' DRAW_CIRCLE
    '''

def p_penup(p):
    '''
    PENUP : penup '(' ')' DO_PENUP
    '''

def p_pendown(p):
    '''
    PENDOWN : pendown '(' ')' DO_PENDOWN
    '''

def p_color(p):
    '''
    COLOR : color '(' DO_COLOR ')' 
    '''

def p_size(p):
    '''
    SIZE : size '(' EXPRESION ')' DO_SIZE
    '''


def p_error(p):
    if p:
        print("Syntax error at '%s' " % p.value, " on line '%s'" % p.lineno)
    else:
        print("Syntax error at EOF")


################################################INBETWEEN RULES####################################





###########################################SEMANTIC RULES#########################################

# Hace que la funcion activa actual sea la funcion global, lo cual permite que las primeras declaraciones de variables
# se guarden en direcciones de tablas de memoria global
def p_sem_global_name(p):
  '''
    SEM_GLOBAL_NAME : id
  '''
  global funcName
  global funcType
  funcName = "global"
  funcType = "void"

# Hace que la funcion activa actual sea la funcion main, lo cual permite conocer a que cuadruplo debe hacer el salto
# el goto inicial de la lista de cuadruplos
def p_sem_main_name(p):
  '''
    SEM_MAIN_NAME : main
  '''
  global funcName
  global funcType
  funcName = p[1]
  funcType = "void"


# Cambia el nombre de la funcion activa actual por el del id encontrado
def p_sem_func_name(p):
  '''
    SEM_FUNC_NAME : id
  '''
  global funcName
  funcName = p[1]

#Añade la función activa actual al directorio de funciones
def p_sem_add_func(p):
  '''
  SEM_ADD_FUNC : 
  '''
  global funcName
  global quadruples
  quadruplesIndex = len(quadruples.quadruples)
  funcDirec.addFunc(funcName, funcType)
  funcDirec.addQuadrupleIndexToFunc(funcName,quadruplesIndex)

# Al terminar de compilar una funcion, añade a su tabla de variables todas las variables globales guardadas, lo
# cual es simplemente copiar la tabla de variables de la funcion global a la tabla de variables de la funcion actual
def p_sem_add_global_variables(p):
  '''
  SEM_ADD_GLOBAL_VARIABLES : 
  '''
  funcDirec.addGlobalVariablesToFunc(funcName)

#LAS SIGUIENTES REGLAS SOLO AÑADEN EL OPERADOR CORRESPONDIENTE A LA LISTA DE OPERADORES (NO DE OPERANDOS)
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

#Rellena ya sea un cuadruplo goto o un cuadruplo gotof que estaba pendiente (para ello sacando un index de la pila de saltos, el cual es el index del cuadruplo goto o gotof pendiente), con el index del 
#cuadruplo siguiente
def p_sem_fill_goto_anykind(p):
  '''
  SEM_FILL_GOTO_ANYKIND : 
  '''
  global gotoList
  global quadruples

  gotoIndex = gotoList.pop()
  directionIndex = len(quadruples.quadruples) + 0 
  quadruples.fillGoToCuadruple(gotoIndex,directionIndex)


#Rellena el cuadruplo goto que hace salto al main, con la informacion que le falta:
#el index del cuadruplo donde empieza el main
def p_sem_fill_main_goto(p):
  '''
    SEM_FILL_MAIN_GOTO : 
  '''
  global gotoList
  global quadruples

  gotoIndex = gotoList.pop()
  directionIndex = len(quadruples.quadruples) 
  quadruples.fillGoToCuadruple(gotoIndex,directionIndex)




#Rellena el cuadruplo gotof anteriormente guardado con destino a un index
#mayor al index del cuadruplo goto que se va a insertar,
#y luego se inserta el cuadruplo goto, guardando en la pila de saltos
#el index de este goto incompleto al cual le falta su direccion de ida
def p_sem_add_goto_simple(p):
  '''
  SEM_ADD_GOTO_SIMPLE : 
  '''
  global gotoList
  global quadruples

  gotoIndex = gotoList.pop()
  directionIndex = len(quadruples.quadruples) + 1
  quadruples.fillGoToCuadruple(gotoIndex,directionIndex)

  quadruples.addGoToCuadruple(None,"goto")
  gotoCuadrupleIndex = len(quadruples.quadruples) - 1
  gotoList.append(gotoCuadrupleIndex)



#Añade a la pila de saltos el index del cuadruplo donde empieza la condicion del loop
def p_sem_add_cond_index(p):
  '''
  SEM_ADD_COND_INDEX : 
  '''
  global gotoList

  condIndex = len(quadruples.quadruples) 
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

#Añade un cuadruplo gotoV a la lista de cuadruplos junto con el operando que va a evaluar, pero sin incluir en el cuadruplo la direccion del salto
#1. Se recibe un operando, y si el operando es bool, se crea el cuadruplo gotoV
#   pues sera el valor de ese operando (true o false) el que se utilizara para determinar si se realiza o no el salto gotoV.
#   De otra manera, si el operando no es bool, el quadruplo no se crea
#2. Se añade el cuadruplo creado a la lista de saltos para posteriormente rellenarlo con la direccion de su salto
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


#Crea un primer cuadruplo goto y añadelo a la lista de quadruplos.
#Este cuadruplo goto espera ser rellenado con el index del cuadruplo
#donde empieza el main 
def p_sem_add_goto_main(p):
  '''
  SEM_ADD_GOTO_MAIN : 
  '''
  global gotoList
  global quadruples
  quadruples.addGoToCuadruple(None,"goto")
  gotoCuadrupleIndex = len(quadruples.quadruples) - 1
  gotoList.append(gotoCuadrupleIndex)

#Al terminar de compilar una funcion, destruye el contenido de todas las tablas de memoria,
#menos las tablas de memoria para constantes y las tablas de memoria global.
#Ademas, verifica que si la funcion no es void, haya habido efectivamente un return statement 
def p_sem_endfunc(p):
  '''
  SEM_ENDFUNC : 
  '''
  global quadruples
  global dirAddresses
  global hasReturn 
  global funcName
  global funcDirec

  quadruples.addEndFuncQuadrupple()

  varsTable = funcDirec.getVariablesTableOfFunc(funcName)
  deleteAddressesOfFunc(funcName,varsTable, dirAddresses)
  #funcDirec.printContents(True)

  if  (funcDirec.getFuncReturnType(funcName) != "void") and (hasReturn == False):
      errorMessage = "Function " + funcName + " is expecting a return value of type " + funcType
      errorQueue.append("Error: " + errorMessage)
      print("Error: ", errorMessage)

  hasReturn = False



def p_sem_verify_func_call(p):
    '''
    SEM_VERIFY_FUNC_CALL : id 
    '''
    global funcDirec
    global funcCall
    global quadruples
    global mustBeVoidCall

    result = funcDirec.verifyFuncCall(p[1], mustBeVoidCall)
    if isinstance(result, str):
        errorQueue.append("Error: " + result)
        print("Error: ", result)
    else:
      funcCall = p[1]
      quadruples.addEraFuncQuadruple(funcCall)

    mustBeVoidCall = False


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
    global funcName
    
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
        funcDirec.addParamAddressOfFunc(funcCall, param.vAddress)
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
    global operandsList
    global funcDirec
    quadruples.addGosubFuncQuadruple(funcCall)
    funcCallType = funcDirec.getFuncReturnType(funcCall)
    
    if not funcCallType =="void":
      operandsList.append( Operand(funcCall,None,funcCallType,funcCall) )

#Verifica que al haber un return statement, el ultimo operando sacado de la pila
# sea del mismo tipo que el tipo de retorno de la funcion activa; si lo es, se guarda
# el cuadruplo del return, y no es necesario guardar el operando resultante (el resultado de la funcion)
# en la lista de operandos, pues esta no es una llamada a una funcion (donde si seria necesario el operando resultante o valor de retorno),
# sino la compilacion de una funcion. Lo que se hace es simplemente, dejar en memoria global 
# la direccion donde deberia de estar el operando de retorno (valor de retorno) al sí hacer la llamada
# a la funcion. Nota: también habra type missmatch si la funcion es tipo void, sea cual sea el tipo de valor del operando sacado de la pila
def p_sem_verify_return_func(p):
    '''
    SEM_VERIFY_RETURN_FUNC :
    '''  
    global funcDirec
    global operandsList
    global funcName
    global dirAddresses
    global quadruples
    global pendingReturnOperand
    global hasReturn 

    hasReturn = True
    rOperand = operandsList.pop()
    result = funcDirec.compareWithFuncReturnType(funcName,rOperand.type)
    if isinstance(result,str):
      errorQueue.append("Error: " + result)
      print("Error: ", result)
    else: 
      resultOperand = quadruples.addReturnCuadruple(funcName,rOperand,dirAddresses)

#Bandera que se usa para verificar semanticamente las llamadas a funciones como estatuto, y las
# llamadas a funciones como expresion. Las llamadas a funciones como estatuto deben ser void, y las
# llamadas a funciones como expresion, NO deben ser void
def p_sem_must_be_void_call(p):
    '''
    SEM_MUST_BE_VOID_CALL :
    '''  
    global mustBeVoidCall
    mustBeVoidCall = True


def p_sem_add_print(p):
    '''
    SEM_ADD_PRINT :
    '''  
    global operandsList
    global quadruples

    operand = operandsList.pop()
    quadruples.addPrintCuadruple(operand)

#Se crea un operando (valor,tipo,direccion) para una constante string recibida como parametro EN EL METODO WRITE
#1.Se consigue la tabla de direcciones de donde debe obtenerse una direccion libre
#2.Se consigue una direccion de la tabla de direcciones correcta (en este caso, constantes string)
#3.Se crea el operando para la constante string con la información necesaria
#4.Se crea el cuadruplo print incluyendo el operando creado
#5.Como es una constante (hay un valor), se guarda en la memoria asignada el valor del operando
def p_sem_add_print_cte_s(p):
    '''
    SEM_ADD_PRINT_CTE_S : cte_s
    '''  
    global operandsList
    global quadruples

    global dirAddresses
    global funcName

    cteValue = p[1]
    cteType = "string"
    addressTableKey = determineTypeAddressTable(None,cteType,cteValue,None)
    vAddress = dirAddresses[addressTableKey].getAnAddress()
    consOperand = Operand(None, cteValue, cteType, vAddress)
    dirAddresses[addressTableKey].saveAddressData(vAddress, cteValue, cteType)
    quadruples.addPrintCuadruple(consOperand)


def p_sem_add_read(p):
    '''
    SEM_ADD_READ : 
    '''  
    global varName
    global funcDirec
    global dirAddresses
    global funcName
    global quadruples
    global operandsList

    operand = operandsList.pop()
    quadruples.addReadQuadruple(operand)





# LAS SIGUIENTES REGLAS SON PARA REALIZAR OPERACIONES BINARIAS, LAS CUALES
# EXTRAEN DOS OPERADORES, VERIFICA SEMANTICAMENTE QUE LA OPERACION ENTRE AMBOS PUEDA
# HACERSE; SI SE PUEDE HACER, SE GUARDA EL CUADRUPLO. AL CREAR EL CUADRUPLO, FUE DEVUELTO 
# UN RESULTADO TEMPORAL, ESTE GUARDADO EN UN OPERANDO, EL CUAL ES AGREGADO A LA PILA DE OPERADORES
# PARA SU FUTURO USO INMEDIATO. ADEMAS, DE ACUERDO AL TIPO DE TEMPORAL CREADO, SE AUNMENTA EL CONTADOR
# CORRECTO DE VARIABLES TEMPORALES EN LA FUNCION ACTIVA

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




#LAS SIGUIENTES SON REGLAS QUE TIENEN QUE VER CON EL MANEJO DE INPUTS GRAFICOS 

def p_draw_point(p):
  '''
  DRAW_POINT :
  '''
  global operandsList
  global quadruples
  yOperand = operandsList.pop()
  xOperand = operandsList.pop()
  
  if ((yOperand.type != "int") and (yOperand.type != "float")) or ((xOperand.type != "int") and (xOperand.type != "float")):
    errorQueue.append("Error: " + "Failed operation, int or float type parameters expected. " + xOperand.type + " and " +  yOperand.type + " were provided.")
    print("Error: " + "Failed operation, int or float type parameters expected. " + xOperand.type + " and " +  yOperand.type + " were provided.")
  else:
    quadruples.addDrawPointQuadruple(xOperand,yOperand)


def p_draw_circle(p):
  '''
  DRAW_CIRCLE :
  '''
  global operandsList
  global quadruples
  radiusOperand = operandsList.pop()
  if (radiusOperand.type != "int") and (radiusOperand.type != "float"):
    errorQueue.append("Error: " + "Failed operation, int or float type parameter expected. " + radiusOperand.type + " was provided.")
    print("Error: " + "Failed operation, int or float type parameter expected. " + radiusOperand.type + " was provided.")
  else:
    quadruples.addDrawCircleQuadruple(radiusOperand)

def p_do_penup(p):
  '''
  DO_PENUP :
  '''
  global quadruples
  quadruples.addPenupQuadruple()

def p_do_pendown(p):
  '''
  DO_PENDOWN :
  '''
  global quadruples
  quadruples.addPendownQuadruple()

def p_do_color(p):
  '''
  DO_COLOR : cte_s
  '''

  global dirAddresses
  global operandsList
  global quadruples

  cteValue = p[1]
  cteType = "string"
  addressTableKey = determineTypeAddressTable(None,cteType,cteValue,None)
  vAddress = dirAddresses[addressTableKey].getAnAddress()
  colorOperand = Operand(None, cteValue, cteType, vAddress)
  dirAddresses[addressTableKey].saveAddressData(vAddress, cteValue, cteType)
  quadruples.addColorQuadruple(colorOperand)

def p_do_clear(p):
  '''
  DO_CLEAR :
  '''
  global quadruples
  quadruples.addClearQuadruple()



def p_do_size(p):
  '''
  DO_SIZE :
  '''
  global operandsList
  global quadruples
  sizeOperand = operandsList.pop()
  if (sizeOperand.type != "int") and (sizeOperand.type != "float"):
    errorQueue.append("Error: " + "Failed operation, int or float type parameter expected. " + sizeOperand.type + " was provided.")
    print("Error: " + "Failed operation, int or float type parameter expected. " + sizeOperand.type + " was provided.")
  else:
    quadruples.addSizeQuadruple(sizeOperand)



######################################################PARSER EXECUTION##############################

#Parse a given file

parser = yacc.yacc()

filename = sys.argv[1]

f = open(filename,'r')
data = f.read()
f.close()

parser.parse(data, tracking=True)
