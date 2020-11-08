
class VarTable():
    def __init__(self):
        self.table = {}


    def addLocalVariable(self, varName, varType, actualScope, isParam, vAddress):
        if not varName in self.table:
            self.table[varName] = {
                "varType": varType ,
                "scope": actualScope,
                "isParam": isParam,
                "vAddress": vAddress
            }
            return True
        else:
            return False

    def getVariable(self, varName):
        if varName in self.table:
            return self.table[varName]
        else: 
            return False


    def addGlobalVariable(self, globalVarName, globalVarContent):
        if not globalVarName in self.table:
            self.table[globalVarName] = {
                "varType": globalVarContent["varType"] ,
                "scope": "global",
                "isParam": False,
                "vAddress": globalVarContent["vAddress"]
            }
            return True
        else:
            return False

           

    def printContents(self):
        for varName,content in self.table.items():
            print("Variable name: " + varName + ". Variable type: " + content["varType"])
            print("Variable scope: " + content["scope"] + ". Variable is param: " + str(content["isParam"]))
            print("Variable vAddress: " + str(content["vAddress"]))














class FuncDirec():
    def __init__(self):
        self.directory = {}


    def addFunc(self, funcName, funcType):
        if not funcName in self.directory:
            self.directory[funcName] = {
                "funcType": funcType,
                "varTable": VarTable(),
                "quadrupleIndex" : None,
                "funcFirm" : [],
                "ParamsQ" : 0, 
                "LIntQ" : 0,   
                "LFloatQ" : 0, 
                "LCharQ" : 0,  
                "GIntQ"  : 0,  
                "GFloatQ" : 0, 
                "GCharQ"  : 0, 
                "TIntQ"  : 0,  
                "TFloatQ" : 0, 
                "TCharQ" : 0,  
                "TBoolQ" : 0  
            }
            return "Sucessful operation. Added function"
        else:
            return "Failed operation. Function name already stored"


    def addLocalVariableToFunc(self, funcName, varName, varType, isParam, vAddress):
        if funcName in self.directory:
            actualScope = "local"
            if funcName == "global":
                actualScope = "global"
            result = self.directory[funcName]["varTable"].addLocalVariable(varName, varType, actualScope, isParam, vAddress)
            if (result):
                if (isParam):
                    self.directory[funcName]["ParamsQ"] += 1
                    self.directory[funcName]["funcFirm"].append(varType)
                elif not funcName == "global":
                    if (varType == "int"):
                        self.directory[funcName]["LIntQ"] += 1
                    elif (varType == "float"):
                        self.directory[funcName]["LFloatQ"] += 1
                    elif (varType == "char"):
                        self.directory[funcName]["LCharQ"] += 1
                elif funcName == "global":
                    if (varType == "int"):
                        self.directory[funcName]["GIntQ"] += 1
                    elif (varType == "float"):
                        self.directory[funcName]["GFloatQ"] += 1
                    elif (varType == "char"):
                        self.directory[funcName]["GCharQ"] += 1

                return True
            else:
                return "Failed operation. Variable name " +  varName + " already exists"

        else:
            return "Failed operation. Function name not found"


    def addGlobalVariablesToFunc(self, funcName):
        globalVariables = self.directory["global"]["varTable"].table
        if funcName in self.directory:
            for globalVarName, globalVarContent in globalVariables.items():
                result = self.directory[funcName]["varTable"].addGlobalVariable(globalVarName,globalVarContent)
                if (result):
                    if (globalVarContent["varType"] == "int"):
                        self.directory[funcName]["GIntQ"] += 1
                    elif (globalVarContent["varType"] == "float"):
                        self.directory[funcName]["GFloatQ"] += 1
                    elif (globalVarContent["varType"] == "char"): 
                        self.directory[funcName]["GCharQ"] += 1

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


    def deleteVarTableInFunc(self,funcName):
        if funcName in self.directory:
            self.directory[funcName]["varTable"] = VarTable()
        else:
            return "Failed operation. Function " + funcName + " not found"



    def addQuadrupleIndexInFunc(self, funcName, quadrupleIndex):
        if funcName in self.directory:
            self.directory[funcName]["quadrupleIndex"] = quadrupleIndex
        else:
            return "Failed operation. Function " + funcName + " not found"


    def addTempVarCountInFunc(self,funcName, tempVarType):
        if funcName in self.directory:
            if (tempVarType == "int"):
                self.directory[funcName]["TIntQ"] += 1
            elif (tempVarType == "float"):
                self.directory[funcName]["TFloatQ"] += 1
            elif (tempVarType == "char"):
                self.directory[funcName]["TCharQ"] += 1
            elif (tempVarType == "bool"):
                self.directory[funcName]["TBoolQ"] += 1
        else:
            return "Failed operation. Function " + funcName + " not found"

    
    def verifyFuncCall(self,funcName, mustBeVoidCall):
        if funcName in self.directory:
            funcType = self.directory[funcName]["funcType"]
            if (mustBeVoidCall == True and funcType == "void") or ( mustBeVoidCall == False and funcType != "void") :
                return True
            else :
                return "Failed operation. Cannot call " + funcName + " , non-void calls as statements and  void calls within expressions are prohibitted"
        else:
            return "Failed operation. Cannot make a call to function " + funcName + ". Function not found"


    def getFunctionFirm(self, funcName):
        if funcName in self.directory:
            return self.directory[funcName]["funcFirm"]
        else:
            return "Failed operation. Cannot get function firm, function" + funcName +" not found"

    def compareWithFuncReturnType(self,funcName, varType):
        if funcName in self.directory:
            if  varType ==  self.directory[funcName]["funcType"]:
                return True
            else:
                return "Failed operation. Return type missmatch in " +  funcName + ", " + self.directory[funcName]["funcType"] + " expected, " + varType + " received"
        else:
            return "Failed operation. Cannot get return type, function" + funcName +" not found"


    def getFuncReturnType(self,funcName):
        if funcName in self.directory:
            return  self.directory[funcName]["funcType"]
        else:
            return "Failed operation. Cannot get return type, function" + funcName +" not found"


    def printContents(self, varTableToo):
        for funcName,content in self.directory.items():
            print("Function name: " + funcName + ". Function type: " + content["funcType"])
            print ("Function firm:" + str(content["funcFirm"]).strip('[]') + ". Function Quadruple Index: "  + str(content["quadrupleIndex"]) )
            print ("Memory needed: " + 
                    " ParamsQ - " + str(content["ParamsQ"]), 
                    ", LIntQ - " + str(content["LIntQ"]),   
                    ", LFloatQ - " + str(content["LFloatQ"]), 
                    ", LCharQ - " + str(content["LCharQ"]),  
                    ", GIntQ - "  + str(content["GIntQ"]),  
                    ", GFloatQ - " + str(content["GFloatQ"]), 
                    ", GCharQ -"  + str(content["GCharQ"]), 
                    ", TIntQ - "  + str(content["TIntQ"]),  
                    ", TFloatQ - " + str(content["TFloatQ"]), 
                    ", TCharQ - " + str(content["TCharQ"]),  
                    ", TBoolQ - " + str(content["TBoolQ"]) )
            if varTableToo:
                content["varTable"].printContents()
            else:
                print("\n")
            

    #def copyGlobalVariablesIntoTable()







