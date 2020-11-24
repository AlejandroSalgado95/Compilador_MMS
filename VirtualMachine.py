import sys

from parser import funcDirec
from parser import quadruples
from parser import dirAddresses
from Tools import determineAddressTableBasedOnVAdress
from Tools import determineMemoryChunkBasedOnName
from Tools import determineGlobalMemoryChunkFromType
from EmptyTempMemoryInstantiator import EmptyTempMemoryInstantiator
import turtle

#Inicializar el apuntador en donde comienzan los cuadruplos del main
IP = quadruples.getQuadruple(0)[3] 
PendingIPList = []
#Cantidad de cuadruplos que hay en el la lista
lastIP = len(quadruples.quadruples)
pen = False 

#Anotacion para saber cual es la llamada activa
funcCalled = ""
funcCalledIndexQuadruple = ""

#Anotacion para saber el estado (up o down) del lapiz de python turtle 
penIsUp = False
addedArrayAddress = False

ArrayToChangeFound = False
ArrayToChangeQuadruple = ""

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


#copia de la memoria guardada antes de cambiar de contexto
tempMemoryStack = []
#stack de llamdas a funciones, utiles para hacer funciones anidadas y saber a que función regresar una vez se ha completado la llamada mas profunda, hasta llegar a la mas superficial
#como el nombre de la funcion es el mismo que el de la variable de retorno, este stack nos permite recordar en que funcion ibamos para saber que valor de retorno entregar (aquel que se llama igual que el nombre de  la funcion reuperada)
funcCallStack = []

#La memoria actual comienza vacia
actualtempMemory = tempMemory

#La memoria anterior comienza sin inicializar
previoustempMemory = ""

print("ACCEPTED")
#funcDirec.printContents(True)
quadruples.printContents()
print("amount of cuadruples: " + str( len(quadruples.quadruples) ) )
for operand in operandsList:
	print("Name: " + str(operand.name), "Value: " + str(operand.value), "Type: " + str(operand.type))
for operator in operatorsList:
    print ("operator: " + operator)
for error in errorQueue:
    print(error)




while IP < len(quadruples.quadruples):
	actualQuadruple = quadruples.getQuadruple(IP)
	if (actualQuadruple[0] == '='):

		#leer la dirección del operando
		op1VA = actualQuadruple[1].vAddress
		#Determinar a que segmento de memoria pertenece la direccion obtenida (local int, global int, etc?)
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		op1Val = ""
		#Busca en la memoria global si la direccion no es numerica, sino el id de retorno de una funcion
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"] 
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		#Obten la direccion y tipo de dato del operando
		asignOpVA = actualQuadruple[3].vAddress
		asignOpType = actualQuadruple[3].type
		#Determina a que segmento de memoria pertenece la direccion
		asignOpTA = determineAddressTableBasedOnVAdress(asignOpVA)
		memoryChunk2 =  determineMemoryChunkBasedOnName(asignOpTA,constMemory,globalMemory,actualtempMemory)
		#Guarda en el segmento de memoria, en la direccion del operando, el resultado de la operacion
		memoryChunk2[asignOpTA].saveAddressData(asignOpVA, op1Val, asignOpType)
		#print ("value: ",op1Val)



	elif (actualQuadruple[0] == '+'):
		#leer la dirección del operando
		op1VA = actualQuadruple[1].vAddress
		op2VA = actualQuadruple[2].vAddress
		#Determinar a que segmento de memoria pertenece la direccion obtenida (local int, global int, etc?)
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		op2TA = determineAddressTableBasedOnVAdress(op2VA)
		memoryChunk1 = ""
		memoryChunk2 = ""
		op1Val = ""
		op2Val = ""
		#Busca en la memoria global si la direccion no es numerica, sino el id de retorno de una funcion
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			#Si hubo un cambio de contexto, busca en el segmento de memoria adecuado de la tabla de memoria anterior al cambio de contexto
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA) 
			if (isinstance(op1Val,str)):
				#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
				op1Val = op1Val["value"]

		#Busca en la memoria global si la direccion no es numerica, sino el id de retorno de una funcion
		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			#Si hubo un cambio de contexto, busca en el segmento de memoria adecuado de la tabla de memoria anterior al cambio de contexto
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				#A sabiendas del segmento de memoria al que pertenece la direccion, recupera su valor guardado
				op2Val = op2Val["value"]
 

		#Realiza la operacion correspondiente con los dos valores extraidos		
		resultValue = op1Val + op2Val
		#print ("op1Val: " + str(op1Val) + ", op2Val: " + str(op2Val))

		#Obten la direccion y tipo de dato del operando
		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		#Determina a que segmento de memoria pertenece la direccion
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 = determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		#Guarda en el segmento de memoria, en la direccion del operando, el resultado de la operacion
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)


#########################################Notas###################################################
#La mayor parte del codigo depués de esta sección repiten exactamente el mismo algoritmo descrito
# anteriormente, el cual consiste en lo siguiente: 
# 1) Lectura de las direcciones de los operandos,
# 2) Identificación del segmento de memoria al que pertenecen a partir de su direccion y tipo de dato
# 3) recuperación de la información guardada en la dirección del segmento de memoria correcto
# 4) realización de la operación descrita por el cuadruplo con los valores recuperados
# 5) Repetición del paso 1 y el paso 2 para el operando resultante
# 6) Guarda en la dirección del segmento de memoria correcto el valor resultante de la operacion realizada entre los valores recuperados
######################################################################################################


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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)  
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]


		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"]


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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]


		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)  
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"]



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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"] 

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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]  

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"]

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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA) 
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)  
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"]

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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			#print ("weirdness: ", op1Val)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"] 

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"]

		resultValue = op1Val != op2Val
		#print("value of array index = ", str(op1Val), " at address = ", op1VA, " at fakeAddress = ", str(actualQuadruple[1].fakeAddress))


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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"] 

		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"] 

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
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"]


		if (op2TA == "isGlobalReturnValue"):
			op2TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk2 = globalMemory
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)["value"]
		else:
			memoryChunk2 =  determineMemoryChunkBasedOnName(op2TA,constMemory,globalMemory,actualtempMemory)
			op2Val = memoryChunk2[op2TA].getAddressData(op2VA)
			if (isinstance(op2Val,str)):
				op2Val = previoustempMemory[op2TA].getAddressData(op2VA)["value"]
			else:
				op2Val = op2Val["value"] 

		resultValue = op1Val or op2Val

		tempOperandVA = actualQuadruple[3].vAddress
		tempOpType = actualQuadruple[3].type
		tempOpAddressTable = determineAddressTableBasedOnVAdress(tempOperandVA)
		memoryChunk3 =  determineMemoryChunkBasedOnName(tempOpAddressTable,constMemory,globalMemory,actualtempMemory)
		memoryChunk3[tempOpAddressTable].saveAddressData(tempOperandVA, resultValue, tempOpType)

	elif (actualQuadruple[0] == "gotoF"):
		#Extrae el indice al cual se debe realizar el salto
		newIP = actualQuadruple[3]
		#Extrae de memoria el operando que contiene la expresion condicional
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

		#Si la expresion condicional es falsa, hay salto
		if (op1Val == False):
			IP = newIP -1


	elif (actualQuadruple[0] == "gotoV"):
		#Extrae el indice al cual se debe realizar el salto
		newIP = actualQuadruple[3]
		#Extrae de memoria el operando que contiene la expresion condicional
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
		
		#Si la expresion condicional es verdadera, hay salto
		if (op1Val == True):
			IP = newIP -1


	elif (actualQuadruple[0] == "goto"):
		#Extrae el indice al cual se debe realizar el salto, y haz el salto
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

		#Si python no ha sido inicializado, inicializalo
		if (pen == False):
			pen = turtle.Turtle()
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
		if (pen == False):
			pen = turtle.Turtle() 
		pen.circle(radius)


	elif (actualQuadruple[0] == "line"):
		#Obten los operandos que representan al punto1 y el punto 2
		point1 = actualQuadruple[1]
		point2 = actualQuadruple[2]

		#Extrae el valor de la coordenada x, del punto 1
		op1VA = point1.vAddress[0]
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		x1 = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(point1.type[0])
			memoryChunk1 = globalMemory
			x1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			x1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		x1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  


		#Extrae el valor de la coordenada y, del punto 1
		op1VA = point1.vAddress[1]
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		y1 = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(point1.type[1])
			memoryChunk1 = globalMemory
			y1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			y1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		y1 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  


		#Extrae el valor de la coordenada x, del punto 2
		op1VA = point2.vAddress[0]
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		x2 = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(point2.type[0])
			memoryChunk1 = globalMemory
			x2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			x2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		x2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  


		#Extrae el valor de la coordenada y, del punto 2
		op1VA = point2.vAddress[1]
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		y2 = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(point2.type[1])
			memoryChunk1 = globalMemory
			y2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			y2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		y2 = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (pen == False):
			pen = turtle.Turtle()

		pen.up()
		pen.home()
		pen.goto(x1,y1)
		if (penIsUp):
			pen.up()
		else:
			pen.down()
		pen.goto(x2,y2)

	
	elif (actualQuadruple[0] == "arc"):
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


		op1VA = actualQuadruple[2].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		angle = ""
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[2].type)
			memoryChunk1 = globalMemory
			angle = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			angle = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		angle = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  

		if (pen == False):
			pen = turtle.Turtle()

		pen.circle(radius,angle)



	elif (actualQuadruple[0] == "penup"):
		if (pen == False):
			pen = turtle.Turtle()
		pen.penup()
		penIsUp = True

	elif (actualQuadruple[0] == "pendown"):
		if (pen == False):
			pen = turtle.Turtle()
		pen.pendown()
		penIsUp = False

	elif (actualQuadruple[0] == "color"):
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		color = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
		if (pen == False):
			pen = turtle.Turtle()
		pen.pencolor(color.strip('"'))

	elif (actualQuadruple[0] == "clear"):
		if (pen == False):
			pen = turtle.Turtle()
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
		
		if (pen == False):
			pen = turtle.Turtle()
		pen.pensize(size)

	elif (actualQuadruple[0] == "return"):
		#obten la dirección del operando de retorno
		op1VA = actualQuadruple[1].vAddress
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		returnValue = ""
		returnType = ""
		#En base al tipo y direccion del operando, determina a que segmento de memoria pertenece
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			#Recupera la información del operando de retorno
			returnValue = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
			returnType = memoryChunk1[op1TA].getAddressData(op1VA)["type"]

		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			#Recupera la información del operando de retorno
			returnValue = memoryChunk1[op1TA].getAddressData(op1VA)["value"]  
			returnType = memoryChunk1[op1TA].getAddressData(op1VA)["type"]


		#En base al tipo del operando de retorno, determina en que segmento de memoria global guardar su informacion de retorno
		typeOfGMemory = ""
		if (returnType == "int"):
			typeOfGMemory = "globalInt"
		elif (returnType == "char"):
			typeOfGMemory = "globalChar"
		elif (returnType == "float"):
			typeOfGMemory = "globalFloat"

		#Guarda la información del operando de retorno de la funcion en el segmento de memoria global correcto
		globalMemory[typeOfGMemory].saveAddressData(funcCalled, returnValue, returnType)




	elif (actualQuadruple[0] == "era"):
		#Obten el nombre de la función que se esta llamando
		funcCalled = actualQuadruple[1]
		#Añadelo a la pila de llamadas para saber el nombre de la  funcion que se quedó pendiente terminar
		funcCallStack.append(funcCalled)

		#print(funcCallStack)

		#Obten en donde se encuentra el inicio del cuadruplo de la funcion llamada
		funcCalledIndexQuadruple = funcDirec.getQuadrupleIndexOfFunc(funcCalled)
		#guarda la memoria actual en el stack de memoria 
		tempMemoryStack.append(actualtempMemory)
		#haz una copia de la memoria actial, ahora siendo la memoria anterior
		previoustempMemory = actualtempMemory
		#crea una nueva instanciacion de memoria para el nuevo contexto, es decir, para la llamada a la funcion que se esta realizando
		actualtempMemory = EmptyTempMemoryInstantiator().InstateEmptyTempMemory()

	elif (actualQuadruple[0] == "parameter"):
		#El parametro de la funcion ya tiene una memoria asignada, pero su valor inicial se encuentra actualmente en otra dirección de memoria,
		#la del ultimo operado de este cuadruplo; hay que pasar el inicial del parametro de la dirección del operando a la dirección del parametro de la funcion

		#saca la direccion del k-esimo parametro
		paramName = actualQuadruple[3].name
		paramNum = int(paramName[len(paramName)-1])
		paramAddressesList = funcDirec.getParamAddressesOfFunc(funcCalled)
		actualParamAddress = paramAddressesList[paramNum]

		#Saca el valor inicial del parametro de la direccion del parametro
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

		#print("New param value:" , paramNewValue)

		#Mete el valor inicial del parametro que se extrajo del operando, hacia adentro de la direccion del parametro 
		op1TA = determineAddressTableBasedOnVAdress(actualParamAddress)
		memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
		memoryChunk1[op1TA].saveAddressData(actualParamAddress, paramNewValue, actualQuadruple[3].type)
		#print("Saving " + str(paramNewValue) + "in address " + str(actualParamAddress) )
		#print("Address saved in " + str(actualParamAddress) + " : " + str(memoryChunk1[op1TA].getAddressData(actualParamAddress)["value"]) )

	elif (actualQuadruple[0] == "endfunc"):
		#Recupera el contexto anterior o tambien llamada memoria temporal, y guardala como la memoria actual
		#lo que significa que al terminar una función, se puede desechar de ejecución a su memoria temporal 
		retrievedTempMemoryChunk = tempMemoryStack.pop()
		actualtempMemory = retrievedTempMemoryChunk
		#Salta al quadruplo que se quedo pendiente antes de hacer la llamada a la funcion
		IP = PendingIPList.pop()
		#Saca de la pila de llamadas pendientes a la llamada actual
		funcCallStack.pop()
		if (len(funcCallStack) > 0):
			#obten la llamada actual, la cual estaba pendiente antes de llamar a la funcion
			funcCalled = funcCallStack[-1]

	elif (actualQuadruple[0] == "gosub"):
		#Añade a la pila de apuntadores a quadruplos el cuadruplo en el que te quedaste pendiente antes de hacer una llamada
		#y luego salta a la direccion de inicio de cuadruplo de la función
		PendingIPList.append(IP) 
		IP = funcCalledIndexQuadruple - 1


	elif (actualQuadruple[0] == "arrayindex"):
		#get the real address of the  array index
		#print ("IP: ", IP)

		#el operando guardado representa la informacion basica del arreglo pendiente de indexar
		#en base a su información basica se recupera del directorio de funciones otra informacion adicional
		# como lo es la direccion limite del arreglo y su dirección base
		#En el operando guardado tambien se encuentra la dirección que tiene guardada la direccion verdadera de indexamiento del arreglo (es un pointer basicamente)
		#Esta información está guardada en fakeaddress
		baseAdress = funcDirec.getVariableInFunc(actualQuadruple[1].value, actualQuadruple[1].name)["vAddress"] #Just for this once, funcname was stored inside the value attribute of the quadruple
		limitAddress = funcDirec.getVariableInFunc(actualQuadruple[1].value, actualQuadruple[1].name)["sLimit"]
		op1VA = actualQuadruple[1].vAddress	
		fakeAddress = op1VA
		op1TA = determineAddressTableBasedOnVAdress(op1VA)
		memoryChunk1 = ""
		op1Val = ""
		#recupera la información de fakeaddress, o el apuntador, ya sea que su direccion de memoria este en un segmento global o local
		if (op1TA == "isGlobalReturnValue"):
			op1TA = determineGlobalMemoryChunkFromType(actualQuadruple[1].type)
			memoryChunk1 = globalMemory
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)["value"]
		else:
			memoryChunk1 =  determineMemoryChunkBasedOnName(op1TA,constMemory,globalMemory,actualtempMemory)
			op1Val = memoryChunk1[op1TA].getAddressData(op1VA)
			if (isinstance(op1Val,str)):
				op1Val = previoustempMemory[op1TA].getAddressData(op1VA)["value"]
			else:
				op1Val = op1Val["value"] #this is real address of the array index

		#print ("op1Val: ", op1Val)
		#print ("baseaddress: ", baseAdress)
		#print ("limitAddress: ", limitAddress)

		#El valor obtenido del apuntador es el valor de indexamiento del arreglo. Verifica que el valor
		#de indexamiente este entre los rangos permitidos del arreglo
		if (op1Val < baseAdress) or (op1Val > limitAddress):  
	         	print("Error: array index out of bounds")

		#Get the operand that represents the array whose index address was missing, and fill it 
		tempIP = IP + 1;
		tempQuadruple = ""
		#En los cuadruplos siguientes se encuentra aquel operando que representa el arreglo que no ha sido indexado
		#apropiadamente aun. Buscalo entre los cuadruplos siguientes, y ya que lo encuentres asignale su dirección virtual
		#verdadera
		while tempIP < len(quadruples.quadruples):
			tempQuadruple = quadruples.getQuadruple(tempIP)
			#print ("tempip:", tempIP)

			if tempQuadruple[1]:
				#print("tempuadruple1.vadress = ", tempQuadruple[1].vAddress, " fakeAddress =", fakeAddress)
				if tempQuadruple[1].fakeAddress == fakeAddress:
					tempQuadruple[1].vAddress = op1Val
					quadruples.updateQuadruple(tempIP,tempQuadruple)
					#print ("tempIP modificado :",tempIP)
					tempIP += len(quadruples.quadruples)

			if tempQuadruple[2]:
				if tempQuadruple[2].fakeAddress == fakeAddress:
					tempQuadruple[2].vAddress = op1Val
					quadruples.updateQuadruple(tempIP,tempQuadruple)
					#print ("tempIP modificado :",tempIP)
					tempIP += len(quadruples.quadruples)


			if tempQuadruple[3]:
				#print ("Operand:",str(tempQuadruple[3]), "on quadruple " + str(tempIP))
				if not (isinstance(tempQuadruple[3],int)):
					if tempQuadruple[3].fakeAddress == fakeAddress:
						tempQuadruple[3].vAddress = op1Val
						quadruples.updateQuadruple(tempIP,tempQuadruple)
						#print ("tempIP modificado :",tempIP)
						tempIP += len(quadruples.quadruples)

			tempIP += 1


		#quadruples.printContents()
	IP += 1






	