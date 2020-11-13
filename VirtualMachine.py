import sys

from parser import funcDirec
from parser import quadruples
from parser import dirAddresses
from Tools import determineAddressTableBasedOnVAdress
from Tools import determineMemoryChunkBasedOnName
from Tools import determineGlobalMemoryChunkFromType
from EmptyTempMemoryInstantiator import EmptyTempMemoryInstantiator
import turtle


IP = quadruples.getQuadruple(0)[3]
PendingIPList = []
lastIP = len(quadruples.quadruples)
pen = turtle.Turtle() 

funcCalled = ""
funcCalledIndexQuadruple = ""

globalMemory = { 
"globalInt" : dirAddresses["globalInt"],
"globalFloat" : dirAddresses["globalFloat"],
"globalChar" : dirAddresses["globalChar"]
}

constMemory = {
"constInt" : dirAddresses["constInt"],
"constFloat" : dirAddresses["constFloat"],
"constChar" : dirAddresses["constChar"],
"constString" : dirAddresses["constString"]
}

tempMemory = {
#Variables locales
"localInt" : dirAddresses["localInt"],
"localFloat" : dirAddresses["localFloat"],
"localChar" : dirAddresses["localChar"],
#Resultados temporales
"tempInt" : dirAddresses["tempInt"],
"tempFloat" : dirAddresses["tempFloat"],
"tempChar" : dirAddresses["tempChar"],
"tempBool" : dirAddresses["tempBool"]
}



tempMemoryStack = []
funcCallStack = []

actualtempMemory = tempMemory
previoustempMemory = ""

while IP < len(quadruples.quadruples):
	actualQuadruple = quadruples.getQuadruple(IP)
	if (actualQuadruple[0] == '='):

		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		op1Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		asignOpVA = actualQuadruple[3].vAddress
		asignOpType = actualQuadruple[3].type
		asignOpTA = determineAddressTableBasedOnVAdress(asignOpVA)
		memoryChunk2 =  determineMemoryChunkBasedOnName(asignOpTA,constMemory,globalMemory,actualtempMemory)
		memoryChunk2[asignOpTA].saveAddressData(asignOpVA, op1Val, asignOpType)
		



	elif (actualQuadruple[0] == '+'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  


		resultValue = op1Val + op2Val
		#print ("op1Val: " + str(op1Val) + ", op2Val: " + str(op2Val))
		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 = determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '-'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val - op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '*'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val * op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '/'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = ""

		if (actualQuadruple[1].type == "int") and (actualQuadruple[2].type == "int"):
			resultValue = int(op1Val / op2Val)
		else:
			resultValue = op1Val/op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '>'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val > op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '<'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val < op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '=='):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val == op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '!='):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val != op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)


	elif (actualQuadruple[0] == '&&'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val and op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == '||'):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		resultValue = op1Val or op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == "gotoF"):
		newIP = actualQuadruple[3]
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		op1Val = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op1Val == False):
			IP = newIP -1


	elif (actualQuadruple[0] == "goto"):
		newIP = actualQuadruple[3]
		IP = newIP -1


	elif (actualQuadruple[0] == "print"):
		op1VA = actualQuadruple[3].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[3].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		print (str(op1Val)) 

	elif (actualQuadruple[0] == "read"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		Op1Type = actualQuadruple[1].type
		newValue = input('Enter your input for variable ' + actualQuadruple[1].name + ": ")
		if (Op1Type == "int"):
			newValue = int(newValue)
		elif (Op1Type == "float"):
			newValue = float(newValue)
		elif (Op1Type == "char"):
			newValue = char(newValue)
		memoryChunk1[op1TA].saveAddressData(op1VA, newValue, Op1Type) 


	elif (actualQuadruple[0] == "point"):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		xCor = ""
		yCor = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			xCor = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			xCor = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			yCor = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			yCor = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		pen.home()
		pen.goto(xCor,yCor)
		pen.dot()


	elif (actualQuadruple[0] == "circle"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		radius = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			radius = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			radius = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		radius = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
		pen.circle(radius)

	elif (actualQuadruple[0] == "penup"):
		pen.penup()

	elif (actualQuadruple[0] == "pendown"):
		pen.pendown()

	elif (actualQuadruple[0] == "color"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		color = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
		pen.pencolor(color.strip('"'))

	elif (actualQuadruple[0] == "clear"):
		pen.clear()

	elif (actualQuadruple[0] == "size"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		size = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			size = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			size = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		pen.pensize(size)

	elif (actualQuadruple[0] == "return"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		returnValue = ""
		returnType = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			returnValue = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
			returnType = memoryChunk1[op1TA].getAddressData(op1VA)["type"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			returnValue = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
			returnType = memoryChunk1[op1TA].getAddressData(op1VA)["type"]


		typeOfGMemory = ""
		if (returnType == "int"):
			typeOfGMemory = "globalInt"
		elif (returnType == "char"):
			typeOfGMemory = "globalChar"
		elif (returnType == "float"):
			typeOfGMemory = "globalFloat"

		globalMemory[typeOfGMemory].saveAddressData(funcCalled, returnValue, returnType)




	elif (actualQuadruple[0] == "era"):
		funcCalled = actualQuadruple[1]
		funcCallStack.append(funcCalled)
		print(funcCallStack)
		funcCalledIndexQuadruple = funcDirec.getQuadrupleIndexOfFunc(funcCalled)
		tempMemoryStack.append(actualtempMemory)
		previoustempMemory = actualtempMemory
		actualtempMemory = EmptyTempMemoryInstantiator().InstateEmptyTempMemory()

	elif (actualQuadruple[0] == "parameter"):
		#Saca el address donde esta registrado el parametro como variable local de la funcion
		paramName = actualQuadruple[3].name
		paramNum = int(paramName[len(paramName)-1])
		paramAddressesList = funcDirec.getParamAddressesOfFunc(funcCalled)
		actualParamAddress = paramAddressesList[paramNum]

		#Saca el valor del parametro del operando
		op2VA = actualQuadruple[3].vAddress
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk2 = ""
		paramNewValue = ""
		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[3].type)
			memoryChunk2 = globalMemory
			paramNewValue = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			paramNewValue = memoryChunk2[op2TA].getAddressData(op2VA)
			#es un id local que se quedo en la memoria anterior, antes de hacer la llamada a la nueva funcion y crear otra tabla de temporales y locales
			if (isinstance(paramNewValue,str)):
				paramNewValue = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				paramNewValue = paramNewValue["value"]



		#Mete el valor dentro del address real del parametro 
		op1TA = determineAddressTableBasedOnVAdress(actualParamAddress)
		memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		memoryChunk1[op1TA].saveAddressData(actualParamAddress, paramNewValue, actualQuadruple[3].type)
		#print("Saving " + str(paramNewValue) + "in address " + str(actualParamAddress) )
		#print("Address saved in " + str(actualParamAddress) + " : " + str(memoryChunk1[op1TA].getAddressData(actualParamAddress)["value"]) )

	elif (actualQuadruple[0] == "endfunc"):
		retrievedTempMemoryChunk = tempMemoryStack.pop()
		actualtempMemory = retrievedTempMemoryChunk
		IP = PendingIPList.pop()
		funcCallStack.pop()
		if (len(funcCallStack) > 0):
			funcCalled = funcCallStack[-1]

	elif (actualQuadruple[0] == "gosub"):
		PendingIPList.append(IP) 
		IP = funcCalledIndexQuadruple - 1


	IP += 1






	