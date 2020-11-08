
from Operand import Operand
from SemanticCube import SC
from Tools import determineTypeAddressTable

class Quadruples():
    def __init__(self):
    	self.quadruples = []
    	self.resultsCounter = 0
        
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

    def addAssignationCuadruple(self,operand, resultOperand):
        result_type = SC[resultOperand.type][operand.type]["="]
        if result_type == "error":
            return "Failed operation. type missmatch: cannot do =" + " operation between " + resultOperand.type + " and " + operand.type
        else:
            self.quadruples.append( ("=", operand, None, resultOperand) )
            return True

    def addGoToCuadruple(self,operand,gotoKind):
        if gotoKind == "gotoF" or gotoKind == "gotoV":
            if operand.type == "bool":
                self.quadruples.append( (gotoKind,operand,None,None) )
            else:
                return "Failed operation. Cannot evaluate " + operand.type + " expression, boolean expression required"
        elif gotoKind == "goto":
            self.quadruples.append( ("goto", None, None, None) )
            return True

    def fillGoToCuadruple(self,gotoIndex,directionIndex):
        incompleteGoTo = self.quadruples[gotoIndex]
        newGoto = (incompleteGoTo[0],incompleteGoTo[1],incompleteGoTo[2], directionIndex )
        #self.quadruples[gotoIndex][3] = directionIndex
        self.quadruples[gotoIndex] = newGoto

    def addEndFuncQuadrupple(self):
        self.quadruples.append( ("endfunc", None, None, None) )

    
    def addParamFuncQuadruple(self, param, paramsCounter):
        resultName = "param" + str(paramsCounter) 
        resultOperand = Operand(resultName, None, param.type, param.vAddress)
        self.quadruples.append( ("parameter", param, None, resultOperand) )


    def addEraFuncQuadruple(self, funcName):
        self.quadruples.append( ("era", funcName, None, None) )


    def addGosubFuncQuadruple(self, funcName):
        self.quadruples.append( ("gosub", funcName, None, None) )

    def addReturnCuadruple(self,funcName, operand, dirAddresses):
        #addressTableKey = determineTypeAddressTable("global",operand.type,None,None)
        #vAddress = dirAddresses[addressTableKey].getAnAddress()
        resultOperand = Operand(funcName, None, operand.type, funcName)
        self.quadruples.append( ("return", operand, None, resultOperand) )
        return resultOperand



    def printContents(self):
        quadrupleCounter = 1

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
                else:
                    tempName3 = str(quadruple[3].name) + "/" + str(quadruple[3].vAddress)

            print (quadrupleCounter, ". (", quadruple[0],',', tempName1 , ',' ,tempName2, ',', tempName3,')')
            quadrupleCounter += 1

