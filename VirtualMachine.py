import sys

from parser import funcDirec
from parser import quadruples
from parser import dirAddresses
from Tools import determineAddressTableBasedOnVAdress
from Tools import determineMemoryChunkBasedOnName
from EmptyTempMemoryInstantiator import EmptyTempMemoryInstantiator
import turtle


IP = quadruples.getQuadruple(0)[3]
PendingIP = IP
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

actualtempMemory = tempMemory

while IP < len(quadruples.quadruples):
	actualQuadruple = quadruples.getQuadruple(IP)
	if (actualQuadruple[0] == '='):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
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
		memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
		op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
		op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		resultValue = op1Val + op2Val

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
		memoryChunk1 = determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		#print(memoryChunk1)
		op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		#op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
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


	elif (actualQuadruple[0] == "point"):
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		xCor = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		yCor = dirAddresses[op2TA].getAddressData(op2VA)["value"]
		pen.home()
		pen.goto(xCor,yCor)
		pen.dot()


	elif (actualQuadruple[0] == "circle"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		radius = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		pen.circle(radius)

	elif (actualQuadruple[0] == "penup"):
		pen.penup()

	elif (actualQuadruple[0] == "pendown"):
		pen.pendown()

	elif (actualQuadruple[0] == "color"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		color = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		pen.pencolor(color.strip('"'))

	elif (actualQuadruple[0] == "clear"):
		pen.clear()

	elif (actualQuadruple[0] == "size"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		size = dirAddresses[op1TA].getAddressData(op1VA)["value"]  
		pen.pensize(size)

	elif (actualQuadruple[0] == "era"):
		funcCalled = actualQuadruple[1]
		funcCalledIndexQuadruple = funcDirec.getQuadrupleIndexOfFunc(funcCalled)
		tempMemoryStack.append(actualtempMemory)
		actualtempMemory = EmptyTempMemoryInstantiator().InstateEmptyTempMemory()

	elif (actualQuadruple[0] == "parameter"):
		#Saca el address donde esta registrado el parametro como variable local de la funcion
		paramName = actualQuadruple[3].name
		paramNum = int(paramName[len(paramName)-1])
		print("param num: " + str(paramNum))
		paramAddressesList = funcDirec.getParamAddressesOfFunc(funcCalled)
		print("param list: " + str(paramAddressesList))
		actualParamAddress = paramAddressesList[paramNum]

		#Saca el valor del parametro del operando
		op2VA = actualQuadruple[3].vAddress
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
		paramNewValue = memoryChunk2[op2TA].getAddressData(op2VA)["value"]  

		#Mete el valor dentro del address real del parametro 
		op1TA = determineAddressTableBasedOnVAdress(actualParamAddress)
		memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		memoryChunk1[op1TA].saveAddressData(actualParamAddress, paramNewValue, actualQuadruple[3].type)
		print("Saving " + str(paramNewValue) + "in address " + str(actualParamAddress) )
		print("Address saved in " + str(actualParamAddress) + " : " + str(memoryChunk1[op1TA].getAddressData(actualParamAddress)["value"]) )

	elif (actualQuadruple[0] == "endfunc"):
		retrievedTempMemoryChunk = tempMemoryStack.pop()
		actualtempMemory = retrievedTempMemoryChunk
		IP = PendingIP

	elif (actualQuadruple[0] == "gosub"):
		PendingIP = IP 
		IP = funcCalledIndexQuadruple - 1


	IP += 1






	