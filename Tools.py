
def determineTypeAddressTable(scopeVar,typeVar,value,fromQuadruple):
	if (scopeVar == "local") :
		if typeVar == "int":
			return "localInt"
		elif typeVar == "float":
			return "localFloat"
		elif typeVar == "char":
			return "localChar"
	elif (scopeVar == "global"):
		if typeVar == "int":
			return "globalInt"
		elif typeVar == "float":
			return "globalFloat"
		elif typeVar == "char":
			return "globalChar"
	elif not value == None:
		if typeVar == "int":
			return "constInt"
		elif typeVar == "float":
			return "constFloat"
		elif  typeVar == "char":
			return "constChar"
		elif typeVar == "string":
			return "constString"
	elif fromQuadruple == True:
		if typeVar == "int":
			return "tempInt"
		elif typeVar == "float":
			return "tempFloat"
		elif typeVar == "char":
			return "tempChar" 
		elif typeVar == "bool":
			return  "tempBool"


def determineAddressTableBasedOnVAdress(vAddress):
	if not( isinstance(vAddress,str)):
		if (vAddress >= 15000 ) and (vAddress <= 15099):
			return "globalInt"
		elif (vAddress >= 15100 ) and (vAddress <= 15199):
			return "globalFloat"
		elif (vAddress >= 15200 ) and (vAddress <= 15299):
			return "globalChar"
		elif (vAddress >= 15300 ) and (vAddress <= 15399):
			return "localInt"
		elif (vAddress >= 15400 ) and (vAddress <= 15499):
			return "localFloat"
		elif (vAddress >= 15500 ) and (vAddress <= 15599):
			return "localChar"
		elif (vAddress >= 15600 ) and (vAddress <= 15699):
			return "tempInt"
		elif (vAddress >= 15700 ) and (vAddress <= 15799):
			return "tempFloat"
		elif (vAddress >= 15800 ) and (vAddress <= 15899):
			return "tempChar"
		elif (vAddress >= 15900 ) and (vAddress <= 15998):
			return "tempBool"
		elif (vAddress >= 16000 ) and (vAddress <= 16099):
			return "constInt"
		elif (vAddress >= 16100 ) and (vAddress <= 16199):
			return "constFloat"
		elif (vAddress >= 16200 ) and (vAddress <= 16299):
			return "constChar"
		elif (vAddress >= 16300 ) and (vAddress <= 16399):
			return "constString"
	else:
		return "isGlobalReturnValue"
	

def deleteAddressesOfFunc(funcName, varTable, dirAddresses):
	
	for varName, contents in reversed(varTable.table.items()):
		if (contents["scope"] != "global"):
			vAddress = contents["vAddress"]
			arraySize = None
			if (contents["isArray"]):
				arraySize =  contents["arraySize"]
			ATname = determineAddressTableBasedOnVAdress(vAddress)
			dirAddresses[ATname].deleteDataFromAddress(vAddress,arraySize);

def determineMemoryChunkBasedOnName(ATname,constMemory,globalMemory,tempMemory):
	if ("const" in ATname):
		return constMemory
	elif ("global" in ATname):
		return globalMemory
	elif ("temp" in ATname):
		return tempMemory
	elif ("local" in ATname):
		return tempMemory

def determineGlobalMemoryChunkFromType(varType):
	if (varType == "int"):
		return "globalInt"
	elif (varType == "float"):
		return "globalFloat"
	elif (varType == "char"):
		return "globalChar"


