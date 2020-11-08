
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

