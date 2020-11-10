
class VarTable():
    def __init__(self):
        self.table = {}


    def addLocalVariable(self, varName, varType, actualScope, isParam, vAddress):
        if not varName in self.table:
            self.table[varName] = {
                "varType": varType ,
                "scope": actualScope,
                "isParam": isParam,
                "vAddress": vAddress,
                "isArray": False,
                "arraySize": None,
                "sLimit" : None
            }
            return True
        else:
            return False


    def addLocalArray(self, varName, varType, actualScope, vAddress, arraySize):
        if not varName in self.table:
            self.table[varName] = {
                "varType": varType ,
                "scope": actualScope,
                "isParam": False,
                "vAddress": vAddress,
                "isArray": True,
                "arraySize": arraySize,
                "sLimit" : vAddress + arraySize - 1
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
                "vAddress": globalVarContent["vAddress"],
                "isArray": globalVarContent["isArray"],
                "arraySize": globalVarContent["arraySize"],
                "sLimit" : globalVarContent["sLimit"]
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


   # Añade una variable local (paramatro o variable local) a la tabla de variables de una funcion,
   # e incrementa el contador respectivo de variables locales. Sin embargo, solo si se trata de la
   # funcion global, entonces incrementa el contador respectivo de variables globales para la funcion global,
   # y agrega a su tabla de variables dichas variables pero no como locales, sino como globales
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


    def addLocalArrayToFunc(self, funcName, varName, varType, vAddress, arraySize):
        if funcName in self.directory:
            actualScope = "local"
            if funcName == "global":
                actualScope = "global"
            result = self.directory[funcName]["varTable"].addLocalArray(varName, varType, actualScope, vAddress, arraySize)
            if (result):
                if not funcName == "global":
                    if (varType == "int"):
                        self.directory[funcName]["LIntQ"] += arraySize
                    elif (varType == "float"):
                        self.directory[funcName]["LFloatQ"] += arraySize
                    elif (varType == "char"):
                        self.directory[funcName]["LCharQ"] += arraySize
                elif funcName == "global":
                    if (varType == "int"):
                        self.directory[funcName]["GIntQ"] += arraySize
                    elif (varType == "float"):
                        self.directory[funcName]["GFloatQ"] += arraySize
                    elif (varType == "char"):
                        self.directory[funcName]["GCharQ"] += arraySize

                return True
            else:
                return "Failed operation. Array name " +  varName + " already exists"

        else:
            return "Failed operation. Function name not found"



    def addGlobalVariablesToFunc(self, funcName):
        globalVariables = self.directory["global"]["varTable"].table
        if funcName in self.directory:
            for globalVarName, globalVarContent in globalVariables.items():
                result = self.directory[funcName]["varTable"].addGlobalVariable(globalVarName,globalVarContent)
                if (result):
                    if not globalVarContent["isArray"]:
                        if (globalVarContent["varType"] == "int"):
                            self.directory[funcName]["GIntQ"] += 1
                        elif (globalVarContent["varType"] == "float"):
                            self.directory[funcName]["GFloatQ"] += 1
                        elif (globalVarContent["varType"] == "char"): 
                            self.directory[funcName]["GCharQ"] += 1
                    else:
                        if (globalVarContent["varType"] == "int"):
                            self.directory[funcName]["GIntQ"] += globalVarContent["arraySize"]
                        elif (globalVarContent["varType"] == "float"):
                            self.directory[funcName]["GFloatQ"] += globalVarContent["arraySize"]
                        elif (globalVarContent["varType"] == "char"): 
                            self.directory[funcName]["GCharQ"] += globalVarContent["arraySize"]



        else:
            return "Failed operation. Function name not found"


    def getVariableInFunc(self, funcName, varName):
        if funcName in self.directory:
            result = self.directory[funcName]["varTable"].getVariable(varName)
            if result != False:
                return result
            else:
                return "Failed operation. var or array " + varName + " not found " + " in scope of " + funcName
        else:
            return "Failed operation. Function " + funcName + " not found"


    def deleteVarTableInFunc(self,funcName):
        if funcName in self.directory:
            self.directory[funcName]["varTable"] = VarTable()
        else:
            return "Failed operation. Function " + funcName + " not found"


    #Añade a una funcion el index cuadruplo en el cual empieza su ejecucion
    def addQuadrupleIndexInFunc(self, funcName, quadrupleIndex):
        if funcName in self.directory:
            self.directory[funcName]["quadrupleIndex"] = quadrupleIndex
        else:
            return "Failed operation. Function " + funcName + " not found"

    #Al realizar cuadruplos dentro de una funcion activa, se generan variables temporales; estas
    # no se guardan dentro de la tabla de variables de la funcion, pero sí deben contabilizarse
    # en el directorio de la funcion activa segun el tipo de variable temporal generada
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

    #Verifica que la llamada a una funcion sea semanticamente correcta. No se puede llamar a una funcion
    #void dentro de una expresion, ni tampoco se puede llamar a una funcion non-void como un statement aislado
    def verifyFuncCall(self,funcName, mustBeVoidCall):
        if funcName in self.directory:
            funcType = self.directory[funcName]["funcType"]
            if (mustBeVoidCall == True and funcType == "void") or ( mustBeVoidCall == False and funcType != "void") :
                return True
            else :
                return "Failed operation. Cannot call " + funcName + " , non-void calls as statements and  void calls within expressions are prohibitted"
        else:
            return "Failed operation. Cannot make a call to function " + funcName + ". Function not found"


    #Devuelve el arreglo que contiene los tipos de datos que se espera que cada uno de los parametros de una funcion sean
    def getFunctionFirm(self, funcName):
        if funcName in self.directory:
            return self.directory[funcName]["funcFirm"]
        else:
            return "Failed operation. Cannot get function firm, function" + funcName +" not found"

    #Compara si el tipo de dato de una variable es el mismo que el tipo de valor de retorno que una funcion. Esta llamada es util para verificar semanticamente el valor de retorno de una funcion (es decir, que haga match con el tipo de valor de retorno de la funcion)
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







