
class VarTable():
    def __init__(self):
        self.table = {}


    def addVariable(self, varName, varType, scope, isParam):
        if not varName in self.table:
            self.table[varName] = {
                "varType": varType ,
                "scope": scope,
                "isParam": isParam
            }
            return True
        else:
            return False

    def getVariable(self, varName):
        if varName in self.table:
            return self.table[varName]
        else: 
            return False


    def addGlobalVariables(self, globalVariables):
        for varName,content in globalVariables.items():
            if not varName in self.table:
                self.table[varName] = {
                    "varType": content["varType"] ,
                    "scope": "global",
                    "isParam": False
                }
           

    def printContents(self):
        for varName,content in self.table.items():
            print("Variable name: " + varName)
            print("Variable type: " + content["varType"])
            print("Variable scope: " + content["scope"])
            print("Variable is param: " + str(content["isParam"]) )





class FuncDirec():
    def __init__(self):
        self.directory = {}


    def addFunc(self, funcName, funcType):
        if not funcName in self.directory:
            self.directory[funcName] = {
                "funcType": funcType,
                "varTable": VarTable(),
                "numberParams": 0
            }
            return "Sucessful operation. Added function"
        else:
            return "Failed operation. Function name already stored"


    def addLocalVariableToFunc(self, funcName, varName, varType, isParam):
        if funcName in self.directory:
            result = self.directory[funcName]["varTable"].addVariable(varName, varType, "local", isParam)
            if (result):
                if (isParam):
                    self.directory[funcName]["numberParams"] += 1
                return "Sucessful operation. Added variable"
            else:
                return "Failed operation. Variable name already exists"

        else:
            return "Failed operation. Function name not found"


    def addGlobalVariablesToFunc(self, funcName):
        globalVariables = self.directory["global"]["varTable"].table
        if funcName in self.directory:
            result = self.directory[funcName]["varTable"].addGlobalVariables(globalVariables)
            if (result):
                return "Sucessful operation. Added global variables"
            else:
                return "Failed operation. Variable name already exists"

        else:
            return "Failed operation. Function name not found"


    def getVariableInFunc(self, funcName, varName):
        if funcName in self.directory:
            result = self.directory[funcName]["varTable"].getVariable(varName)
            if result != False:
                return result
            else:
                return "Failed operation. Var " + varName + " not found " + " in scope of " + funcName
        else:
            return "Failed operation. Function " + funcName + " not found"


    def printContents(self, varTableToo):
        for funcName,content in self.directory.items():
            print("Function name: " + funcName)
            print("Function type: " + content["funcType"])
            print("Function amount of params: " + str(content["numberParams"]) )
            if varTableToo:
                content["varTable"].printContents()
            else:
                print("\n")


    #def copyGlobalVariablesIntoTable()







