
class VirtualAdresses():
    def __init__(self,startVAddress,finalVAddress):
    	self.table = {}
    	self.start= startVAddress
    	self.final = finalVAddress
    	self.actualVAddress = self.start


    def getAddressData(self,vAddress):
        return self.table[vAddress]

    def saveAddressData(self, vAddress, varValue, varType):

    	self.table[vAddress] = {
    		"value" : varValue,
  			"type" : varType 
    	}

    def getAnAddress(self):
        self.actualVAddress += 1
        return self.actualVAddress - 1


    def deleteAllContent(self):
    	self.table = {}
    	self.actualVAddress = self.start
