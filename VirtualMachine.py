import sys

from parser import funcDirec
from parser import quadruples
from parser import dirAddresses
from Tools import determineAddressTableBasedOnVAdress

IP = quadruples.getQuadruple(0)[3]
lastIP = len(quadruples.quadruples)



while IP < len(quadruples.quadruples):
	actualQuadruple = quadruples.getQuadruple(IP)
	if (actualQuadruple[0] == '='):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  

		asignOpVA = actualQuadruple[3].vAddress
		asignOpType = actualQuadruple[3].type
		asignOpTA = determineAddressTableBasedOnVAdress(asignOpVA)
		dirAddresses[asignOpTA].saveAddressData(asignOpVA, op1Val, asignOpType)

	elif (actualQuadruple[0] == '+'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val + op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '-'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val - op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '*'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val * op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '/'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		
		if (actualQuadruple[1].type == "int") and (actualQuadruple[2].type == "int"):
			resultValue = int(op1Val / op2Val)
		else:
			resultValue = op1Val/op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '>'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val > op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '<'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val < op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '=='):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val == op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '!='):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val != op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)


	elif (actualQuadruple[0] == '&&'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val and op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '||'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		op2Val = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val or op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		dirAddresses[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == "gotoF"):
		newIP = actualQuadruple[3]
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		#print ("OP1TA: " + op1TA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]

		if (op1Val == False):
			IP = newIP -1


	elif (actualQuadruple[0] == "goto"):
		newIP = actualQuadruple[3]
		IP = newIP -1


	elif (actualQuadruple[0] == "print"):
		op1VA = actualQuadruple[3].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		#print ("OP1TA: " + op1TA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]
		print (str(op1Val)) 

	elif (actualQuadruple[0] == "read"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		Op1Type = actualQuadruple[1].type
		newValue = input('Enter your input for variable ' + actualQuadruple[1].name + ": ")
		if (Op1Type == "int"):
			newValue = int(newValue)
		elif (Op1Type == "float"):
			newValue = float(newValue)
		elif (Op1Type == "char"):
			newValue = char(newValue)
		dirAddresses[op1TA].saveAddressData(op1VA, newValue, Op1Type) 


	IP += 1






	