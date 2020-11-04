
from Operand import Operand
from SemanticCube import SC

class Quadruples():
    def __init__(self):
    	self.quadruples = []
    	self.resultsCounter = 0
        
    def addExpressionCuadruple(self, operator, leftOperand, rightOperand ):
        result_type = SC[leftOperand.type][rightOperand.type][operator]
        if result_type == "error":
            return "Failed operation. type missmatch: cannot do " + operator + " operation between " + leftOperand.type + " and " + rightOperand.type
        else:
            self.resultsCounter += 1
            resultName = "result" + str(self.resultsCounter)
            resultOperand = Operand(resultName, None, result_type)
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
        


    def printContents(self):
        quadrupleCounter = 1

        for quadruple in self.quadruples:
            tempName1 = None
            tempName2 = None
            tempName3 = None

            if not quadruple[1] == None:
                if quadruple[1].name == None:
                    tempName1 = quadruple[1].value
                else: 
                    tempName1 = quadruple[1].name

            if not quadruple[2] == None:
                if quadruple[2] and quadruple[2].name == None:
                    tempName2 = quadruple[2].value
                else:
                    tempName2 = quadruple[2].name

            if not quadruple[3] == None:
                if isinstance(quadruple[3],int):
                    tempName3 = quadruple[3]
                else:
                    tempName3 = quadruple[3].name

            print (quadrupleCounter, ". (", quadruple[0],',', str(tempName1), ',' ,str(tempName2), ',', str(tempName3),')')
            quadrupleCounter += 1

