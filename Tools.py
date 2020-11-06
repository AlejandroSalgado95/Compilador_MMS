
def determineTypeAddressTable(scopeVar,typeVar):
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