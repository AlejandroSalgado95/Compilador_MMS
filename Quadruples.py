
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



    def printContents(self):
        for quadruple in self.quadruples:
            tempName1 = None
            tempName2 = None

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

            print ("(", quadruple[0],',', str(tempName1), ',' ,str(tempName2), ',',quadruple[3].name,')')


