import sys

from parser import funcDirec
from parser import quadruples
from parser import dirAddresses
from Tools import determineAddressTableBasedOnVAdress

IP = quadruples.getQuadruple(0)[3]
lastIP = len(quadruples.quadruples)

for IP in range(IP, lastIP):
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




	elif (actualQuadruple[0] == "print"):
		op1VA = actualQuadruple[3].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		#print ("OP1TA: " + op1TA)
		op1Val = dirAddresses[op1TA].getAddressData(op1VA)["value"]
		print (str(op1Val)) 






	