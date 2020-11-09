
from Operand import Operand
from SemanticCube import SC
from Tools import determineTypeAddressTable

class Quadruples():
    def __init__(self):
    	self.quadruples = []
    	self.resultsCounter = 0
      
    #Permite añadir cuadruplos que son producto una operacion binaria, como: +, - , && >, etc
    #1. Revisa si la operacion a realizar es semanticamente correcta entre los dos operandos recibidos
    #2. Crea un nuevo operando para el resultado de la operacion binaria, y le asigna una memoria
    #3. Se crea el cuadruplo con la informacion del operador y los 3 operandos
    #4. Regresa al parser el operando resultante de la operacion binaria para ser guardado en la pila de operandos,
    #   pues este operando, que es un resultado intermedio, sera utilizado por otras operaciones para generar otros cuadruplos
    #   con este operando resultante
    def addExpressionCuadruple(self, operator, leftOperand, rightOperand, dirAddresses):
        result_type = SC[leftOperand.type][rightOperand.type][operator]
        if result_type == "error":
            return "Failed operation. type missmatch: cannot do " + operator + " operation between " + leftOperand.type + " and " + rightOperand.type
        else:
            self.resultsCounter += 1
            resultName = "result" + str(self.resultsCounter) 
            addressTableKey = determineTypeAddressTable(None,result_type,None,True)
            vAddress = dirAddresses[addressTableKey].getAnAddress()
            resultOperand = Operand(resultName, None, result_type, vAddress)
            self.quadruples.append( (operator, leftOperand, rightOperand, resultOperand) )
            return resultOperand

    #Permite añadir un cuadruplo de una operacion de asignacion
    #1. Revisa si la operacion a realizar es semanticamente correcta entre los dos operandos recibidos
    #2. Crea el cuadruplo de asignacion
    def addAssignationCuadruple(self,operand, resultOperand):
        result_type = SC[resultOperand.type][operand.type]["="]
        if result_type == "error":
            return "Failed operation. type missmatch: cannot do =" + " operation between " + resultOperand.type + " and " + operand.type
        else:
            self.quadruples.append( ("=", operand, None, resultOperand) )
            return True

    #Se crea un cuadruplo de cualquier tipo de goto
    #1. Si es un gotoV o un gotoF, se revisa que el operando recibido sea 
    #   correcto semanticamente (un bool esperado). Si el operando es 
    #   semanticamente correcto, se crea el gotoF o gotoV que evalua
    #   el operando recibido
    #2. Si es un goto, el quadruplo simplemente se crea
    def addGoToCuadruple(self,operand,gotoKind):
        if gotoKind == "gotoF" or gotoKind == "gotoV":
            if operand.type == "bool":
                self.quadruples.append( (gotoKind,operand,None,None) )
            else:
                return "Failed operation. Cannot evaluate " + operand.type + " expression, boolean expression required"
        elif gotoKind == "goto":
            self.quadruples.append( ("goto", None, None, None) )
            return True

    #Rellena cualquier tipo de cuadruplo goto con la dirección de destino faltante
    #1.se busca el cuadruplo goto pendiente de rellenar por medio de un index recibido
    #2 se rellena el cuadruplo goto pendiente con la direccion de destino faltante por medio de un index recibido
    def fillGoToCuadruple(self,gotoIndex,directionIndex):
        incompleteGoTo = self.quadruples[gotoIndex]
        newGoto = (incompleteGoTo[0],incompleteGoTo[1],incompleteGoTo[2], directionIndex )
        #self.quadruples[gotoIndex][3] = directionIndex
        self.quadruples[gotoIndex] = newGoto

    def addEndFuncQuadrupple(self):
        self.quadruples.append( ("endfunc", None, None, None) )

    #Crea un cuadruplo que le permite que etiquetar como "parametro de una funcion" a un operando
    #1. Se crea un operando cuyo nombre es el numero del parametro de la funcion, y 
    #   su dirección virtual es exactamente la misma que el operando 
    #   recibido, de esta manera haciendo alucion a que no se esta creando un 
    #   operando nuevo ni asignandole nueva memoria a ese operando nuevo, sino
    #   que simplemente se esta referenciando un operando que ya existe 
    #   en memoria, pero dentro del cuadruplo se le esta etiquetando a ese
    #   operando con otro nombre (parametro1, por ejemplo)
    #2. Se genera el cuadruplo
    def addParamFuncQuadruple(self, param, paramsCounter):
        resultName = "param" + str(paramsCounter) 
        resultOperand = Operand(resultName, None, param.type, param.vAddress)
        self.quadruples.append( ("parameter", param, None, resultOperand) )


    def addEraFuncQuadruple(self, funcName):
        self.quadruples.append( ("era", funcName, None, None) )


    def addGosubFuncQuadruple(self, funcName):
        self.quadruples.append( ("gosub", funcName, None, None) )


     #Se crea el cuadruplo de return de una funcion
     #1. Se crea un operando nuevo a partir del operando recibido ( el cual
     #   contiene toda la informacion necesaria del resultado de la funcion).
     #   El operando nuevo, a diferencia del recibido, se llamara igual
     #   la funcion a la que pertenece el return, y se le asignara una 
     #   memoria global (tambien con el mismo nombre de la funcion)
     #2. Se devuelve el operando creado para ser guardado en la pila de 
     #   operandos dentro del parser, pues el operando creado (el valor 
     #   de retorno de la funcion) sera utilizado por alguna otra operacion
     #   que genere otro cuadruplo
    def addReturnCuadruple(self,funcName, operand, dirAddresses):
        #addressTableKey = determineTypeAddressTable("global",operand.type,None,None)
        #vAddress = dirAddresses[addressTableKey].getAnAddress()
        resultOperand = Operand(funcName, None, operand.type, funcName)
        self.quadruples.append( ("return", operand, None, resultOperand) )
        return resultOperand


    def addPrintCuadruple(self,operand):
        self.quadruples.append(("print",None,None,operand))



    def getQuadruple(self,index):
        if self.quadruples[index]:
            return self.quadruples[index]



    def printContents(self):
        quadrupleCounter = 0

        for quadruple in self.quadruples:
            tempName1 = None
            tempName2 = None
            tempName3 = None

            if not quadruple[1] == None:
                if isinstance(quadruple[1],str):
                    tempName1 = quadruple[1]
                elif quadruple[1].name == None:
                    tempName1 = str(quadruple[1].value) + "/" + str(quadruple[1].vAddress)
                else: 
                    tempName1 = str(quadruple[1].name) + "/" + str(quadruple[1].vAddress)

            if not quadruple[2] == None:
                if quadruple[2] and quadruple[2].name == None:
                    tempName2 = str(quadruple[2].value) + "/" + str(quadruple[2].vAddress)
                else:
                    tempName2 = str(quadruple[2].name) + "/" + str(quadruple[2].vAddress)

            if not quadruple[3] == None:
                if isinstance(quadruple[3],int):
                    tempName3 = str(quadruple[3])
                elif quadruple[3].name == None:
                    tempName3 = str(quadruple[3].value) + "/" + str(quadruple[3].vAddress)
                else:
                    tempName3 = str(quadruple[3].name) + "/" + str(quadruple[3].vAddress)

            print (quadrupleCounter, ". (", quadruple[0],',', tempName1 , ',' ,tempName2, ',', tempName3,')')
            quadrupleCounter += 1

