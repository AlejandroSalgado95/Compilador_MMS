from FunctionDirectory import VarTable
class VirtualAdresses():
    def __init__(self,startVAddress,finalVAddress, tableName):
        self.table = {}
        self.start= startVAddress
        self.final = finalVAddress
        self.actualVAddress = self.start
        self.tableName = tableName


    def getAddressData(self,vAddress):
        if not (isinstance (vAddress,str)):
            if (vAddress >= self.start) and (vAddress <= self.final):
                if str(vAddress) in self.table:
                    return self.table[str(vAddress)]
                else:
                    return "Failed operation. No data stored in vAddress " + str(vAddress) + " inside of vaddress table " + self.tableName
            else: 
                return "Failed operation. No vAddress " + str(vAddress) + " available in the range of this vaddress table: " + self.tableName
        else:
            if vAddress in self.table: 
                return self.table[vAddress].pop(0)
            else:
                return "Failed operation. No vAddress " + vAddress + " available as the return value of " + vAddress

    def saveAddressData(self, vAddress, varValue, varType):
        
        if not (isinstance (vAddress,str)):
            if (vAddress >= self.start) and (vAddress <= self.final):
                    self.table[str(vAddress)] = {
                        "value" : varValue,
                        "type" : varType 
                     }
            else:
                return "Failed operation. No vAddress " + str(vAddress) + " available in the range of this vaddress table: " + self.tableName
        
        #se guardara el return de una funcion
        else:
            '''
            if not vAddress in self.table
                self.table[str(vAddress)] = { "returnStack" : []}
                self.table[str(vAddress)]["returnStack"].append((varValue,varType))
            else:
                self.table[str(vAddress)]["returnStack"].append((varValue,varType))
            '''
            if not vAddress in self.table:
                self.table[str(vAddress)] = [{ "value" : varValue, "type": varType }]
            else:
                self.table[str(vAddress)].append({"value" : varValue, "type" : varType})

    def getAnAddress(self):
        self.actualVAddress += 1
        return self.actualVAddress - 1

    def getAnAdressForArray(self,arraySize):
        availableAddress = self.actualVAddress
        vAddressCounter = availableAddress
        while vAddressCounter < (availableAddress + arraySize ):
            self.table[str(vAddressCounter)] = {
                    "value" : "null",
                    "type" : "null" 
            }
            vAddressCounter += 1

        self.actualVAddress += arraySize
        return availableAddress


    def deleteAllContent(self):
    	self.table = {}
    	self.actualVAddress = self.start

    def deleteDataFromAddress(self,vAddress, arraySize):

        if (arraySize == None):
            self.table.pop( str(vAddress), None )
            self.actualVAddress -= 1
        else:
            vAddressCounter = vAddress
            while vAddressCounter < (vAddress + arraySize - 1 ):
                self.table.pop(str(vAddressCounter), None)
                vAddressCounter += 1
            self.actualVAddress -= arraySize


