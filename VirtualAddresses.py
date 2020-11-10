
class VirtualAdresses():
    def __init__(self,startVAddress,finalVAddress, tableName):
        self.table = {}
        self.start= startVAddress
        self.final = finalVAddress
        self.actualVAddress = self.start
        self.tableName = tableName


    def getAddressData(self,vAddress):

        if (vAddress >= self.start) and (vAddress <= self.final):
            if str(vAddress) in self.table:
                return self.table[str(vAddress)]
            else:
                return "Failed operation. No data stored in vAddress " + str(vAddress) + " inside of vaddress table " + self.tableName
        else: 
            return "Failed operation. No vAddress " + str(vAddress) + " available in the range of this vaddress table: " + self.tableName

    def saveAddressData(self, vAddress, varValue, varType):
        
        if (vAddress >= self.start) and (vAddress <= self.final):
            self.table[str(vAddress)] = {
                "value" : varValue,
                "type" : varType 
             }
        else: 
            return "Failed operation. No vAddress " + str(vAddress) + " available in the range of this vaddress table: " + self.tableName


    def getAnAddress(self):
        self.actualVAddress += 1
        return self.actualVAddress - 1

    def getAnAdressForArray(self,arraySize):
        availableAddress = self.actualVAddress
        self.actualVAddress += arraySize
        return availableAddress


    def deleteAllContent(self):
    	self.table = {}
    	self.actualVAddress = self.start
