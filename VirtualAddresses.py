
class VirtualAdresses():
    def __init__(self,startVAddress,finalVAddress, tableName):
        self.table = {}
        self.start= startVAddress
        self.final = finalVAddress
        self.actualVAddress = self.start
        self.tableName = tableName


    def getAddressData(self,vAddress):

        if (vAddress >= self.start) and (vAddress <= self.final):
            if vAddress in self.table:
                return self.table[vAddress]
            else:
                return "Failed operation. No data stored in vAddress " + vAddress + " inside of vaddress table " + self.tableName
        else: 
            return "Failed operation. No vAddress " + vAddress + " available in the range of this vaddress table: " + self.tableName

    def saveAddressData(self, vAddress, varValue, varType):
        
        if (vAddress >= self.start) and (vAddress <= self.final):
            self.table[vAddress] = {
                "value" : varValue,
                "type" : varType 
             }
        else: 
            return "Failed operation. No vAddress " + vAddress + " available in the range of this vaddress table: " + self.tableName


    def getAnAddress(self):
        self.actualVAddress += 1
        return self.actualVAddress - 1


    def deleteAllContent(self):
    	self.table = {}
    	self.actualVAddress = self.start
